import json
import h2o
import requests

from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField
from wtforms.validators import DataRequired

from process_data import process_input

# For logging
import logging
import traceback
from logging.handlers import RotatingFileHandler
from time import strftime, time


class ClientDataForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    exposure = IntegerField('Экспозиция', validators=[DataRequired()])
    lic_age = IntegerField('Водительский стаж, мес.', validators=[DataRequired()])
    gender = SelectField('Пол', choices=[('Male', 'М'), ('Female', 'Ж')])
    mari_stat = SelectField('Семейное положение', choices=[('Alone', 'Alone'), ('Other', 'Other')])
    age = IntegerField('Возраст водителя, лет', validators=[DataRequired()])
    has_km_limit = SelectField('Ограничение пробега', choices=[('Yes', 'Есть'), ('No', 'Нет')])
    bonus_malus = IntegerField('Коэфициент бонуса-малус', validators=[DataRequired()])
    out_use_nb = IntegerField('Число out-of-use за 4 года', validators=[DataRequired()])
    risk_area = SelectField('Неизвестная зона риска', choices=[(str(i), i) for i in range(1,14)])
    veh_usage = SelectField('Использование ТС', choices=[('Private',)*2, ('Private + trip to office',)*2,
                                                        ('Professional',)*2, ('Professional run',)*2])
    socio_categ = SelectField('Социальная категория', choices=[(f'CSP{i}',)*2 for i in range(1,8)])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

# Logging
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=5)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

h2o.init()
model = h2o.load_model('GLM_model_python_1591128704532_39')

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print("@app.route('/predicted/<response>')", response)
    return render_template('predicted.html', response=response)


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
    claim_ind_front = 'Страховой случай НАСТУПИТ' if bool(claim_ind) else 'Страховой случай НЕ наступит'

    result = {
        'ID': id,
        'prob_0': prob_0,
        'prob_1': prob_1,
        'threshold_prob': THRESHOLD,
        'claim_ind': claim_ind,
        'claim_ind_front': claim_ind_front
    }

    # Response logging
    end_prediction = time()
    duration = round(end_prediction - start_prediction, 6)
    current_datetime = strftime('[%Y-%b-%d %H:%M:%S]')
    logger.info(f'{current_datetime} predicted for {duration} msec: {result}\n')

    return jsonify(result)


def send_json(data):
    url = 'http://127.0.0.1:5000/predict'
    headers = {'content-type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    if request.method == 'GET':
        form = ClientDataForm()
    elif request.method == 'POST':
        data = {'ID': request.form.get('id'),
                'Exposure': float(request.form.get('exposure')),
                'LicAge': float(request.form.get('lic_age')),
                'Gender': request.form.get('gender'),
                'MariStat': request.form.get('mari_stat'),
                'DrivAge': float(request.form.get('age')),
                'HasKmLimit': request.form.get('has_km_limit'),
                'BonusMalus': float(request.form.get('bonus_malus')),
                'OutUseNb': float(request.form.get('out_use_nb')),
                'RiskArea': float(request.form.get('risk_area')),
                'VehUsage': request.form.get('veh_usage'),
                'SocioCateg': request.form.get('socio_categ')}
        try:
            response = send_json(data)
            response = response.text
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


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


if __name__ == '__main__':
    app.run(debug=True)