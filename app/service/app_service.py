import numpy as np
import pandas as pd

import mlflow

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import optuna
from optuna.samplers import TPESampler

from app.schemas.response import People

from app.utils.app_exceptions import AppException
from app.utils.service_result import ServiceResult

from app.db.database import SessionLocal, engine, insert_data


class TrainService:
    """
    Train 서비스
    데이터 로드 / 전처리 / 분리 / 라벨링 / 최적화 / 예측 / 모델 저장 기능
    """

    def __init__(self):
        self.db = SessionLocal
        self.engine = engine

    def load_data(self):
        data = pd.read_sql_query("SELECT * FROM people_incomes;", self.engine)
        return data

    def preprocessing(self, data):
        data["native_country"] = data["native_country"].fillna("United-States")
        data.dropna(inplace=True)
        return data

    def data_split(self, data, size=0.25):
        y = data.loc[:, "target"]
        y = y.astype("int")
        X = data.drop("target", axis=1)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=size, random_state=1234, stratify=y
        )
        return X_train, X_test, y_train, y_test

    def labeling(self, data: People, newdata: People):
        nominals = [key for key, value in data.dtypes.items() if value == object]
        for ord in nominals:
            le = LabelEncoder()
            le.fit(data[ord])
            data[ord] = le.transform(data[ord])
            prev_class = list(le.classes_)
            for label in np.unique(newdata[ord]):
                if label not in prev_class:
                    prev_class.append(label)
            le.classes_ = np.array(prev_class)
            newdata[ord] = le.transform(newdata[ord])
        return data, newdata

    def rf_optimization(
        self, X_train, y_train, n_splits: int, n_trials: int, measure: str
    ):
        kfold = KFold(n_splits=n_splits, random_state=1234, shuffle=True)

        def objective(trial):
            params = {
                "criterion": trial.suggest_categorical(
                    "criterion", ["gini", "entropy"]
                ),
                "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
                "max_depth": trial.suggest_int("max_depth", 3, 5),
                "max_leaf_nodes": trial.suggest_int("max_leaf_nodes", 10, 100),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 100),
            }
            rf = RandomForestClassifier(**params, n_jobs=-1, random_state=1234)

            scores = cross_val_score(rf, X_train, y_train, cv=kfold, scoring=measure)
            acc_mean = scores.mean()
            return acc_mean

        sampler = TPESampler(**TPESampler.hyperopt_parameters())
        study = optuna.create_study(direction="maximize", sampler=sampler)
        study.optimize(objective, n_trials=n_trials)
        params = study.best_trial.params
        return params

    def model_predict(self, params, X_train, y_train):
        model = RandomForestClassifier(**params, n_jobs=-1, random_state=1234)
        model.fit(X_train, y_train)
        pred = model.predict(X_train)
        return pred

    def model_scoring(self, params, X_train, y_train, measure):
        pred = self.model_predict(params, X_train, y_train)
        scores = {}
        scores["accuracy"] = accuracy_score(y_train, pred)
        scores["recall"] = recall_score(y_train, pred)
        scores["precision"] = precision_score(y_train, pred)
        scores["f1"] = f1_score(y_train, pred)
        return scores[measure]

    def model_save(self, model, model_key, params, metrics):
        mlflow.set_tracking_uri("http://172.26.0.9:5000")
        mlflow.set_experiment("rf_test")
        mlflow.start_run()
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, "rf_model", registered_model_name=model_key)
        mlflow.end_run()

    def train(self, n_trial: int, n_split: int, model_key: str, scoring: str):
        try:
            insert_data()
            data = self.load_data()
            print(1)
            data = self.preprocessing(data)
            X_train, X_test, y_train, y_test = self.data_split(data)
            X_train, X_test = self.labeling(X_train, X_test)
            params = self.rf_optimization(
                X_train, y_train, n_trials=n_trial, n_splits=n_split, measure=scoring
            )
            print(2)
            model = RandomForestClassifier(**params, n_jobs=-1, random_state=1234)
            model.fit(X_train, y_train)
            metrics = {
                scoring: self.model_scoring(
                    params=params, X_train=X_train, y_train=y_train, measure=scoring
                )
            }
            print("metrics", metrics)
            self.model_save(model, model_key, params, metrics)
            print(4)
        except Exception as ex:
            print("train error :", ex)
            return ServiceResult(AppException.LoadModel())
        return ServiceResult({"purpose": "Train", "context": "Done"})


class PredictService:
    """
    저장된 모델을 불러와 redisai에 저장 후 불러와서 예측 함
    """

    def __init__(self, client, model_key):
        self.client = client
        self.model_key = model_key

    def load_model(self) -> bool:
        result = False
        try:
            mlflow.set_tracking_uri("http://172.26.0.9:5000")
            mlflow.set_experiment("rf_test")
            model = mlflow.sklearn.load_model(f"models:/{self.model_key}/Production")
            self.set_model_redisai(model)
            result = True
        except Exception:
            result = False
            return result
        return result

    def set_model_redisai(self, model):
        try:
            initial_type = [("input", FloatTensorType([None, 14]))]
            onx_model = convert_sklearn(model, initial_types=initial_type)
            self.client.modelstore(
                key=self.model_key,
                backend="onnx",
                device="cpu",
                data=onx_model.SerializeToString(),
            )
        except Exception as ex:
            print("=-----------=", ex)

    def model_run(self, item):
        self.client.tensorset(
            "input_tensor",
            np.array(
                [
                    [
                        item.age,
                        item.workclass,
                        item.fnlwgt,
                        item.education,
                        item.education_num,
                        item.marital_status,
                        item.occupation,
                        item.relationship,
                        item.race,
                        item.sex,
                        item.capital_gain,
                        item.capital_loss,
                        item.hours_per_week,
                        item.native_country,
                    ]
                ],
                dtype=np.float32,
            ),
        )
        self.client.modelrun(
            key=self.model_key,
            inputs=["input_tensor"],
            outputs=["output_tensor_class", "output_tensor_prob"],
        )
        self.client.expire = ("input_tensor", 1)
        return self.client.tensorget("output_tensor_class").tolist()[0]

    def predict(self, data):
        try:
            result = None
            if not self.client.exists(self.model_key):
                is_set = self.load_model()
                if not is_set:
                    return ServiceResult(AppException.LoadModel())
            try:
                result = self.model_run(data)
            except Exception:
                return ServiceResult(AppException.LoadModel())
            return ServiceResult({"target": result, "context": "Done"})
        except Exception as ex:
            print("predict", ex)
