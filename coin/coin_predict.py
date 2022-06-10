from coin.coin_service import Coin_service
from coin.config import settings

ticker = settings.ticker


def train():
    import mlflow

    cs = Coin_service()
    df = cs.data_load(ticker)
    df, scaler_y = cs.scaling(df)
    x_train, x_test, y_train, y_test = cs.split(df)
    train_data = cs.windowed_dataset(y_train, True)
    test_data = cs.windowed_dataset(y_test, False)

    y_pred, model = cs.run_model(train_data, test_data, scaler_y)

    metrics = cs.confirm_result(y_test, y_pred)
    print(metrics)

    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("coin_experiment")
    mlflow.start_run()
    mlflow.log_metrics(metrics)
    mlflow.keras.log_model(model, "coin", registered_model_name="coin")
    mlflow.end_run()
