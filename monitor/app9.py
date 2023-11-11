from flask import Flask
from prometheus_client import Counter, generate_latest
import random
import pickle
import pandas as pd

app = Flask(__name__)

zero_metric = Counter('predict', 'Zero count', ['ind'])

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/predict/<number>')
def predict(number):
        path = "dump.pkl"
        model = pickle.load(open(path, 'rb'))
        row_df = pd.DataFrame.from_dict({'tx_amount': [int(number)+random.randint(0,10)],
                'tx_time_seconds': [int(number)+random.randint(0,10)],
                'tx_time_days': [int(number)+random.randint(0,10)]})
        prediction = model.predict(row_df)

        if prediction==0:
            zero_metric.labels(ind=prediction).inc()
        return str(prediction)

if __name__ == '__main__':
    app.run(debug=True)