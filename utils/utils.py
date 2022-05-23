# import numpy as np
# import pandas as pd
# import joblib
# from skl2onnx import convert_sklearn
# from skl2onnx.common.data_types import FloatTensorType

# from sklearn.model_selection import KFold
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import cross_val_score
# from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split

# #hyperparameter tuning
# import optuna
# from optuna.samplers import TPESampler

# from schemas.response import *
# from utils.app_exceptions import AppException
# from utils.service_result import ServiceResult
# from utils.service_result import handle_result


# def save_model_redisai(client,model_key,model):
#     initial_type = [("input", FloatTensorType([None, 14]))]
#     onx_model = convert_sklearn(model, initial_types=initial_type)
#     client.modelstore(
#         key=model_key, backend="onnx", device="cpu", data=onx_model.SerializeToString()
#             )

# def load_model(client,model_key,name):
#     try:
#         model = joblib.load(f"{name}.pkl")
#         save_model_redisai(client,model_key,model)
#     except Exception as err:
#        return handle_result(ServiceResult(AppException.LoadModel()))

# def predict(client, model_key, item):
#     try:
#         client.tensorset(
#             "input_tensor",
#             np.array([[item.age, item.workclass, item.fnlwgt, item.education, item.education_num, item.marital_status, item.occupation, item.relationship,
#             item.race, item.sex,item.capital_gain,item.capital_loss,item.hours_per_week,item.native_country]], dtype=np.float32),
#         )
#         client.modelrun(
#             key=model_key,
#             inputs=["input_tensor"],
#             outputs=["output_tensor_class", "output_tensor_prob"],
#         )
#         return ServiceResult(client.tensorget("output_tensor_class").tolist()[0])
#     except:
#         return ServiceResult(AppException.ModelKey())

    

# ###############################################################
# def preprocessing(data):
#     data['native_country']=data['native_country'].fillna('United-States')
#     # data["fnlwgt"] = np.log1p(data["fnlwgt"])
#     data.dropna(inplace=True)
#     return data


# def data_split(data, size=0.25):

#     y = data.loc[:,"target"]
#     y = y.astype('int')
#     X = data.drop("target", axis = 1)
#     X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=size, random_state=1234,stratify=y)
#     return X_train, X_test, y_train, y_test


# def labeling(data, newdata):
#     nominals=[key for key, value in data.dtypes.items() if value==object] #object타입의 데이터 list
#     for ord in nominals:
#         le = LabelEncoder()
#         le.fit(data[ord])
#         data[ord] = le.transform(data[ord])#규칙적용
#         prev_class = list(le.classes_)#컬럼내 유니크한 값 list

#         for label in np.unique(newdata[ord]):
#             if label not in prev_class: #unseendata 확인 후 없으면 추가
#                 prev_class.append(label)

#         le.classes_ = np.array(prev_class)
#         newdata[ord] = le.transform(newdata[ord])#새로 수정된 규칙으로 적용
#     return data, newdata


# def rf_optimization(X_train, y_train, n_trials=10,  n_splits=5, measure='accuracy'):
#     kfold = KFold(n_splits = n_splits, random_state=1234,shuffle=True )

#     def objective(trial):
#         params = {
#             "criterion" : trial.suggest_categorical("criterion", ["gini","entropy"]),
#             "n_estimators" : trial.suggest_int("n_estimators", 100, 1000),
#             "max_depth" : trial.suggest_int("max_depth", 3, 5),
#             "max_leaf_nodes" : trial.suggest_int("max_leaf_nodes",10, 100),

#             "min_samples_leaf" :trial.suggest_int("min_samples_leaf", 1, 100)
#         }
#         rf = RandomForestClassifier(**params, n_jobs=-1, random_state=1234)

#         scores = cross_val_score(rf, X_train, y_train, cv=kfold, scoring=measure)
#         acc_mean = scores.mean()
#         return acc_mean
#     sampler = TPESampler(**TPESampler.hyperopt_parameters())
#     study = optuna.create_study(direction="maximize" ,sampler=sampler)
#     study.optimize(objective, n_trials=n_trials)
#     params=study.best_trial.params
#     return params


# def model_predict(params, X_train,y_train):
#     model=RandomForestClassifier(**params, n_jobs=-1, random_state=1234)
#     model.fit(X_train, y_train)
#     pred = model.predict(X_train)
#     return pred


# def model_scoring(params, X_train, y_train, pred, measure='accuracy'):
#     pred=model_predict(params, X_train,y_train)

#     scores={}
#     scores['accuracy']=accuracy_score(y_train, pred)
#     scores['recall']=recall_score(y_train, pred)
#     scores['precision']=precision_score(y_train, pred)
#     scores['f1']=f1_score(y_train, pred)
#     return scores[measure]

# def model_save(model):
#     joblib.dump(model, 'model.pkl',compress=3)
