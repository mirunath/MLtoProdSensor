from flask import Flask, redirect, url_for, json
from pyod.utils.data import generate_data
import numpy as np
import requests
import datetime


app = Flask(__name__)


@app.route('/')
def iot():
    X_train, X_test, y_train, y_test = generate_data(n_train=20, n_test=10, n_features=3,
                                                     contamination=0.1,  random_state=42)

    # generate the list of indices to be sampled
    array_indexes = list(range(X_test.shape[0]))

    while True:
        # get a random index
        index = np.random.choice(array_indexes)
        current = X_test[index]

        api_url = 'http://127.0.0.1:5000/sensors'
        event_data = {
            "temperature": float(current[0]),
            "humidity": float(current[1]),
            "sound-volume": float(current[2]),
        }

        response = requests.post(api_url, json=event_data)
        response_json = json.loads(response.json())

        result = str(response_json["result"])
        text = 'ANOMALOUS' if result == '1' else 'NORMAL'
        print(f"[{datetime.datetime.now()}] Wind turbine sensor status -> {text}")


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
