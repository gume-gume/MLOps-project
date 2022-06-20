import mlflow

from coin.coin_service import Coin_service


def train(ticker):
    cs = Coin_service()
    df = cs.data_load(ticker)
    df, scaler, scaler_y = cs.scaling(df)
    x_train, x_test, y_train, y_test = cs.split(df)
    train_data = cs.windowed_dataset(y_train, True)
    test_data = cs.windowed_dataset(y_test, False)
    rescaled_pred, y_pred, model = cs.run_model(train_data, test_data, scaler_y)
    metrics = cs.confirm_result(y_test, y_pred)
    print(metrics)

    mlflow.set_tracking_uri("http://172.26.0.9:5000")
    mlflow.set_experiment(f"{ticker}_experiment")
    mlflow.start_run(tags={"version": "1.0.0"})
    mlflow.log_metrics(metrics)
    mlflow.keras.log_model(model, ticker, registered_model_name=ticker)
    mlflow.keras.log_model(scaler, "scaler", registered_model_name="scaler")
    mlflow.keras.log_model(scaler_y, "scaler_y", registered_model_name="scaler_y")

    mlflow.end_run()


def predict_coin(ticker, coin_df):
    mlflow.set_tracking_uri("http://172.26.0.9:5000")
    mlflow.set_experiment(f"{ticker}_experiment")
    model = mlflow.keras.load_model(f"models:/{ticker}/Production")
    scaler = mlflow.keras.load_model("models:/scaler/Prodcution")
    scaler_y = mlflow.keras.load_model("models:/scaler_y/Prodcution")

    coin_df = scaler.transform(coin_df)

    result = model.fit(coin_df)
    return scaler_y.inverse_transform(result)
