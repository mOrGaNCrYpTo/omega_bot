import pandas as pd
import numpy as np
import logging
import os
from contextlib import contextmanager
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow import Input, Dense, LSTM
from tensorflow import Model

# Define file paths
MODEL_PATH = 'models/btc_usdt_1hr.h5'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a boolean flag for retraining
retrain = True

@contextmanager
def open_file(file_path, mode='r'):
    """Open a file and return a file object, handle errors"""
    try:
        f = open(file_path, mode)
        yield f
    except Exception as e:
        logger.error(f"Error opening {file_path}: {e}")
    finally:
        f.close()


def load_data(file_path):
    """Load data from a CSV file and pre-process it"""
    with open_file(file_path) as f:
        # Load the data into a pandas DataFrame
        data = pd.read_csv(f)

        # Convert 'openTime' column to datetime
        data['openTime'] = pd.to_datetime(data['openTime'], errors='coerce')

        # Extract features
        data['hour'] = data['openTime'].dt.hour
        data['day_of_week'] = data['openTime'].dt.dayofweek
        data['month'] = data['openTime'].dt.month

        # Convert number fields to float
        data[['openPrice', 'closePrice', 'highPrice', 'lowPrice', 'volume']] = data[['openPrice', 'closePrice', 'highPrice', 'lowPrice', 'volume']].astype(float)

        # Create a new feature representing the 'closePrice' one hour ago
        data['closePrice_lag1'] = data['closePrice'].shift(1)
        data['closePrice_lag24'] = data['closePrice'].shift(24)
        data['closePrice_lag48'] = data['closePrice'].shift(48)
        data['closePrice_lag72'] = data['closePrice'].shift(72)

        # Drop rows with NaN values
        data.dropna(inplace=True)

        return data


def prepare_data(data):
    """Split the data into training and test sets, and prepare it for training"""
    # Determine the split point for 80% of the data
    split_point = int(len(data) * 0.8)

    # Split the data into training and test sets
    train = data[:split_point]
    test = data[split_point:]

    # Separate the features (X) from the target (y)
    X_train = train.drop(['closePrice', 'openTime', 'symbol'], axis=1).values
    y_train = train['closePrice'].values
    X_test = test.drop(['closePrice', 'openTime', 'symbol'], axis=1).values
    y_test = test['closePrice'].values

    # Make sure that all of the data is of type float
    X_train = X_train.astype(np.float32)
    y_train = y_train.astype(np.float32)
    X_test = X_test.astype(np.float32)
    y_test = y_test.astype(np.float32)

    # Reshape input to be [samples, time steps, features]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    return X_train, y_train, X_test, y_test


def create_model(input_shape):
    """Create and compile an LSTM model"""
    inputs = Input(shape=input_shape)

    lstm_out = LSTM(50)(inputs)

    predictions = Dense(1)(lstm_out)

    model = Model(inputs=inputs, outputs=predictions)

    model.compile(optimizer='adam', loss='mean_squared_error')

    return model


def train_model(X_train, y_train, model_path):
    """Train and save the LSTM model"""
    model = create_model((X_train.shape[1], 1))

    model.fit(X_train, y_train, epochs=100, batch_size=32)

    # Save the trained model
    if not os.path.exists('models'):
        os.makedirs('models')
    model.save(model_path)


def load_model(model_path):
    """Load a pre-trained LSTM model"""
    return tf.keras.models.load_model(model_path)


def predict_next_hour(model, latest_data, retrain=True):
    """Predict the closing price for the next hour"""
    # Load the data and preThe `utils.py` module looks great! Here's the completed `predict_next_hour` function:
    # Prepare the data
    X_train, y_train, X_test, y_test = prepare_data(data)

    if retrain:
        logger.info('Retraining....')
        train_model(X_train, y_train, MODEL_PATH)

    # Load the pre-trained model
    model = load_model(MODEL_PATH)

    # Get the latest data
    latest_data = latest_data[-24:]

    # Add the latest data to the training set
    data = pd.concat([data, latest_data], ignore_index=True)

    # Prepare the data for prediction
    X, _, _, _ = prepare_data(data[-24:])

    # Make the prediction
    prediction = model.predict(X)

    return prediction[-1][0]