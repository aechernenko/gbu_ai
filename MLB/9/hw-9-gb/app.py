import h2o
from flask import Flask, request, jsonify

from process_data import process_input

# For logging
import logging
import traceback
from logging.handlers import RotatingFileHandler
from time import strftime, time


app = Flask(__name__)

h2o.init()
model = h2o.load_model('GLM_model_python_1591128704532_39')

# Logging
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=5)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.route("/")
def index():
    return "API for predict service"


@app.route("/predict", methods=['POST'])
def predict():
    json_input = request.json

    # Request logging
    current_datetime = strftime('[%Y-%b-%d %H:%M:%S]')
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    logger.info(f'{current_datetime} request from {ip_address}: {request.json}')
    start_prediction = time()

    # id запроса
    id = json_input['ID']

    # подготовка входных данных
    hf = process_input(json_input)

    # предсказание модели
    prediction = model.predict(hf).as_data_frame()
    # вероятности классов
    prob_0 = prediction['p0'][0]
    prob_1 = prediction['p1'][0]
    THRESHOLD = 0.58  # порог вероятности для класса 1
    claim_ind = 1 if prob_1 > THRESHOLD else 0

    result = {
        'ID': id,
        'prob_0': prob_0,
        'prob_1': prob_1,
        'threshold_prob': THRESHOLD,
        'claim_ind': claim_ind
    }

    # Response logging
    end_prediction = time()
    duration = round(end_prediction - start_prediction, 6)
    current_datetime = strftime('[%Y-%b-%d %H:%M:%S]')
    logger.info(f'{current_datetime} predicted for {duration} msec: {result}\n')

    return jsonify(result)


@app.errorhandler(Exception)
def exceptions(e):
    current_datetime = strftime('[%Y-%b-%d %H:%M:%S]')
    error_message = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                 current_datetime,
                 request.remote_addr,
                 request.method,
                 request.scheme,
                 request.full_path,
                 error_message)
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == "__main__":
    app.run(debug=True)
