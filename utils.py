import numpy as np
import pandas as pd
import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_auc_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split



def load_model(client, model_key):
    model = joblib.load("rf_income.pkl")
    initial_type = [("input", FloatTensorType([None, 16]))]
    onx_model = convert_sklearn(model, initial_types=initial_type)

    client.modelstore(
        key=model_key, backend="onnx", device="cpu", data=onx_model.SerializeToString()
    )


def predict(client, model_key, item):
    client.tensorset(
        "input_tensor",
        np.array([[item.age, item.workclass, item.fnlwgt, item.education, item.marital_status, item.occupation, item.relationship, item.race, item.sex, 
        item.hours_per_week, item.native_country, item.capital,item.high_educated,item.Marriage,item.high_income,item.family]], dtype=np.float32),
    )
    client.modelrun(
        key=model_key,
        inputs=["input_tensor"],
        outputs=["output_tensor_class", "output_tensor_prob"],
    )
    client.expire(model_key, 50)

    return client.tensorget("output_tensor_class")

###############################################################
def read_data():
    data=pd.read_csv('data/train.csv')
    return data


def Preprocessing(data):
    data['native.country']=data['native.country'].fillna('United-States')
    data['workclass'].fillna('None',inplace=True)
    data['occupation'].fillna('None',inplace=True)
    dic_occupation={}

    for i in data['education'].unique():
        dic_occupation[i]=Counter(data[data['education']==i]['occupation']).most_common()[0][0]


    dic_workclass={}

    for i in data['education'].unique():
        dic_workclass[i]=Counter(data[data['education']==i]['workclass']).most_common()[0][0]


    for i in range(0,len(data)):

        if data.iloc[i,data.columns.get_loc('occupation')]=='None':

            data.iloc[i,data.columns.get_loc('occupation')]=dic_workclass[data.iloc[i,data.columns.get_loc('education')]]
        else:
            pass

    for i in range(0,len(data)):
        if data.iloc[i,data.columns.get_loc('workclass')]=='None':

            data.iloc[i,data.columns.get_loc('workclass')]=dic_workclass[data.iloc[i,data.columns.get_loc('education')]]
            cnt+=1
        else:
            pass

    data["fnlwgt"] = np.log1p(data["fnlwgt"])

    data['capital']=data['capital.gain']-data['capital.loss']
    data=data.drop(['capital.gain','capital.loss'], axis=1)

    high_educated=['Bachelors','Masters']
    data['high_educated']=data['education'].apply(lambda x: 1 if x in high_educated else 0)

    Marriage=['Married-civ-spouse','Married-AF-spouse']
    data['Marriage']=data['marital.status'].apply(lambda x: 1 if x in Marriage else 0)

    high_income=['Exec-managerial','Prof-specialty','Sales','Tech-support','Protective-serv']

    data['high_income']=data['occupation'].apply(lambda x: 1 if x in high_income else 0)

    family=['Husband','Wife']

    data['family']=data['relationship'].apply(lambda x: 1 if x in family else 0)

    del data['education.num']

    nominals = ['workclass','education','marital.status','relationship','race','sex','native.country','occupation']

    for nominal in nominals:
        le = LabelEncoder()
        le.fit(data[nominal])
        data[nominal] = le.transform(data[nominal]) 
    return data


import optuna
from optuna.samplers import TPESampler

def RF_Optimization(n_trials=10,  n_splits=5, scoring='accuracy'):
    kfold = KFold(n_splits = n_splits, random_state=1234,shuffle=True )

    def objective(trial):
        params = {
            "criterion" : trial.suggest_categorical("criterion", ["gini","entropy"]),
            "n_estimators" : trial.suggest_int("n_estimators", 100, 1000),
            "max_depth" : trial.suggest_int("max_depth", 3, 5),
            "max_leaf_nodes" : trial.suggest_int("max_leaf_nodes",10, 100),

            "min_samples_leaf" :trial.suggest_int("min_samples_leaf", 1, 100)
        }
        rf = RandomForestClassifier(**params, n_jobs=-1, random_state=1234)

        scores = cross_val_score(rf, X_train_ps, y_train, cv=kfold, scoring=scoring)
        acc_mean = scores.mean()
        return acc_mean
    sampler = TPESampler(**TPESampler.hyperopt_parameters())
    study = optuna.create_study(direction="maximize" ,sampler=sampler)
    study.optimize(objective, n_trials=n_trials)
    RF_params=study.best_trial.params 
    
    return RF_params

