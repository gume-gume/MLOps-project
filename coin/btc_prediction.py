from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Conv1D
from tensorflow.keras.losses import Huber
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import metrics
import pandas as pd
import os

from coin.coin_service import cursor
from config import settings

ticker = settings.ticker

cursor.execute(f"""SELECT * FROM public."{ticker}";""")
data = cursor.fetchall()
scaler = MinMaxScaler()
scale_cols = ["open", "high", "low", "close", "volume", "value"]
data = pd.DataFrame(data)
data.set_index(0, inplace=True)
data.columns = scale_cols
scaled = scaler.fit_transform(data[scale_cols])
df = pd.DataFrame(scaled, columns=scale_cols)

x_train, x_test, y_train, y_test = train_test_split(
    df.drop("close", 1), df["close"], test_size=0.2, random_state=0, shuffle=False
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


WINDOW_SIZE = 240
BATCH_SIZE = 320

train_data = windowed_dataset(y_train, WINDOW_SIZE, BATCH_SIZE, True)
test_data = windowed_dataset(y_test, WINDOW_SIZE, BATCH_SIZE, False)


model = Sequential(
    [
        Conv1D(
            filters=32,
            kernel_size=5,
            padding="causal",
            activation="relu",
            input_shape=[WINDOW_SIZE, 1],
        ),
        LSTM(16, activation="tanh"),
        Dense(16, activation="relu"),
        Dense(1),
    ]
)


loss = Huber()
optimizer = Adam(0.0005)
model.compile(loss=Huber(), optimizer=optimizer, metrics=["mse"])


model.compile(
    loss="mean_squared_error",
    optimizer="sgd",
    metrics=[metrics.mae, metrics.categorical_accuracy],
)


earlystopping = EarlyStopping(monitor="val_loss", patience=10)

filename = os.path.join("tmp", "ckeckpointer.ckpt")
checkpoint = ModelCheckpoint(
    filename, save_weights_only=True, save_best_only=True, monitor="val_loss", verbose=1
)

history = model.fit(
    train_data,
    validation_data=(test_data),
    epochs=10,
    callbacks=[checkpoint, earlystopping],
)


history.history.keys()
history.history["mse"][-1]


history.history["val_loss"][-1]


model.load_weights(filename)

pred = model.predict(test_data)
