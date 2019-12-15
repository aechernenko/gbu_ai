"""
Задание 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

import requests
import json


main_link = 'https://api.rasp.yandex.net/v3.0/search'

# Авторизация через API key
# Выводит на экран 6 записей о ближайших электричках из Сергиева посада до Москвы
# s9601389 - Сергиев посад
# s2000002 - Москва (Ярославский вокзал)

params = {'apikey': '943a01bb-70ce-421f-b3e3-be032c924180',
          'from': 's9601389',
          'to': 's2000002',
          'transport_types': 'suburban',
          'limit': '6'}

response = requests.get(main_link, params=params)
data = response.json()

if response.ok:

    # Вывод списка ближайших электричек
    print('Ближайшие электрички из Сергиева Посада в Москву')
    for segment in data['segments']:
        print('*', segment['days'],
              'кроме' if bool(segment['except_days']) else '',
              segment['except_days'],
              segment['departure'],
              'в пути:', int(segment['duration']/60), 'мин.')

    # сохранение всех данных в файл .json
    with open(f'sp-msk.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
