import datetime
import sys


sys.path.append("/home/dahy949/airflow/project/coin")
import mlflow
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from coin_service import Coin_service
from app.utils import service_result
from coin.utils import get_production_model_uri
from config import settings

def make_dataset(data, label, window_size=20):
    feature_list = []
    label_list = []
    for i in range(len(data) - window_size):
        feature_list.append(np.array(data.iloc[i : i + window_size]))
        label_list.append(np.array(label.iloc[i + window_size]))
    return np.array(feature_list), np.array(label_list)


def train(ticker):
    cs = Coin_service()
    df = cs.data_load(ticker)
    df, scaler, scaler_y = cs.scaling(df)
    x_train, x_test, y_train, y_test = cs.split(df)
    train_data = cs.windowed_dataset(y_train, True)
    test_data = cs.windowed_dataset(y_test, False)
    rescaled_pred, y_pred, model = cs.run_model(train_data, test_data, scaler_y)
    metrics = cs.confirm_result(y_test, y_pred)

    mlflow.set_tracking_uri(settings.tracking_uri)
    mlflow.set_experiment(f"{ticker}_experiment")
    mlflow.start_run(tags={"version": "1.0.0"})
    mlflow.log_metrics(metrics)
    mlflow.keras.log_model(model, ticker, registered_model_name=ticker)
    mlflow.sklearn.log_model(scaler, "scaler")
    mlflow.sklearn.log_model(scaler_y, "scaler_y")
    mlflow.end_run()


def predict_coin(ticker, coin_df):
    model_uri = get_production_model_uri(ticker)
    run_id = model_uri.split("/")[-3]
    mlflow.set_tracking_uri(settings.tracking_uri)
    mlflow.set_experiment(f"{ticker}_experiment")
    model = mlflow.keras.load_model(f"models:/{ticker}/Production")
    logged_model = f"runs:/{run_id}/scaler"
    logged_model_y = f"runs:/{run_id}/scaler_y"
    scaler = mlflow.sklearn.load_model(logged_model)
    scaler_y = mlflow.sklearn.load_model(logged_model_y)
    #####################################################################

    scale_cols = ["open", "high", "low", "volume", "value"]
    coin_df[scale_cols] = scaler.fit_transform(coin_df[scale_cols])
    coin_df["close"] = scaler_y.fit_transform(coin_df["close"].values.reshape(-1, 1))

    x_train, x_test, y_train, y_test = train_test_split(
        coin_df.drop("close", 1),
        coin_df["close"],
        test_size=0.2,
        random_state=0,
        shuffle=False,
    )

    def windowed_dataset(series, window_size, batch_size, shuffle):
        series = tf.expand_dims(series, axis=-1)
        ds = tf.data.Dataset.from_tensor_slices(series)
        ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
        ds = ds.flat_map(lambda w: w.batch(window_size + 1))
        if shuffle:
            ds = ds.shuffle(1000)
        ds = ds.map(lambda w: (w[:-1], w[-1]))
        return ds.batch(batch_size).prefetch(1)

    WINDOW_SIZE = 20
    BATCH_SIZE = 32

    test_data = windowed_dataset(y_test, WINDOW_SIZE, BATCH_SIZE, False)
    pred = model.predict(test_data)
    rescaled_pred = scaler_y.inverse_transform(np.array(pred).reshape(-1, 1))
    result = rescaled_pred[-1][0]
    ft = (coin_df.index[-1] + datetime.timedelta(hours=4)).strftime("%Y년 %m월 %d일 %H시")
    return service_result.ServiceResult({"datetime": ft, "price": result})
