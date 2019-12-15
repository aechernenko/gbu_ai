"""
Задание 1. Посмотреть документацию к API GitHub, разобраться как вывести список
репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
"""

import requests
import json


# USERNAME = input()
USERNAME = 'python'

response = requests.get(f'https://api.github.com/users/{USERNAME}/repos')
repos = response.json()

if response.ok:

    # Вывод списка репозиториев с ссылками
    print('Список репозиториев пользователя', USERNAME)
    for i, repo in enumerate(repos):
        print(i+1, '\t', repo['name'], repo['html_url'])

    # сохранение всех данных в файл .json
    with open(f'{USERNAME}_repos.json', 'w', encoding='utf-8') as file:
        json.dump(repos, file, indent=4, ensure_ascii=False)

    print(f'{USERNAME}_repos.json сохранен!')
