# ЗАДАНИЕ
# 1)Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать:
# * название источника,
# * наименование новости,
# * ссылку на новость,
# * дата публикации
# 2)Сложить все новости в БД


# Для анализа кода страниц использовал Яндекс.Браузер с дополнениями:
# ChroPath for Opera - для генерации относительныз ссылок xpath для элементов страницы
# User-Agent Switcher - для загрузки страниц в мобильном виде


import requests
from lxml import html
from pprint import pprint
import time
from hashlib import sha1
import datetime as dt
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


month_dict = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12
}

MOBILE = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) '
                        'AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 '
                        'Mobile/9A334 Safari/7534.48.3'}

DESKTOP = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/78.0.3904.108 '
                         'YaBrowser/19.12.3.320 Yowser/2.5 Safari/537.36'}


def get_data(links, titles, datetimes, sources):
    """
    Формирует из входных списков с данными список словарей,
    где каждый словарь набор данных об одной новости.
    В каждом словаре добавляется поле _id, значение для
    которого расчитывается как sha1 от конкатенации строк
    с названием новости title и времени публикации datetime.
    link не учитывается, так как, например, в mail.ru ссылки
    имеют параметры со случайными значениями для одной и той же
    странцы новости.
    source тоже не учитывается, так как на разных агрегаторах
    написание названий источников может различаться
    """
    data = [{} for _ in range(len(links))]
    for i, dct in enumerate(data):
        dct['title'] = titles[i]
        dct['datetime'] = datetimes[i]
        dct['source'] = sources[i]
        dct['link'] = links[i]
        dct['_id'] = sha1((titles[i]+datetimes[i]).encode('utf-8')).hexdigest()
    return data


def mailru():
    """
    Используем мобильную версию браузера.
    На главной странице находим блок с новостями news_blocks.
    Далее находим и сохраняем названия новостей и их ссылки.
    Далее проходим по каждой ссылке с новостью, где находим и
    сохраняем данные о времени публикации и источнике.
    """
    print('Сбор на mail.ru')
    time.sleep(1)
    response = requests.get('https://mail.ru', headers=MOBILE)

    if response.ok:
        root = html.fromstring(response.text)
        news_blocks = root.xpath("//div[@id='news-0']/a[@class='list__item']")
        links, titles, datetimes, sources = [], [], [], []

        for block in news_blocks:
            link = block.xpath("./@href")[0]
            links.append(link)
            titles.append(block.xpath("./div/span/text()")[0].replace('\xa0', ' '))

            time.sleep(1)
            response = requests.get(link, headers=MOBILE)

            if response.ok:
                root = html.fromstring(response.text)
                datetimes.append(root.xpath("//time[1]/@datetime")[0])
                sources.append(root.xpath("//a[contains(@class,'article__param')]/text()")[0])
            else:
                print('Mail.ru: error')

        return get_data(links, titles, datetimes, sources)

    else:
        print('Mail.ru: error')


def yandex():
    """
    Все данные собираются с одной главной страницы яндекс новостей.
    Используется десктопный юзер-агент браузера.
    Сложность сбора данных об источнике и времени публикации заключается
    в том, что эти данные представленны в виде одной строки, а время
    публикации отражается в разных видах.
    Например:

    lenta.ru 22:30
    Газета.ru вчера в 12:55
    РБК 05 января в 23:12

    Дата-время публикации парсятся и форматируются в ISO-формат.
    Для этого используется модуль datetime и вспомогательный словарь month_dict
    """
    print('Сбор на yandex.ru/news')
    main_link = 'https://yandex.ru/news'
    time.sleep(1)
    response = requests.get(main_link, headers=DESKTOP)

    if response.ok:

        root = html.fromstring(response.text)
        # блок с главными новостями
        news_block = root.xpath("//div[@class='page-content__fixed']")[0]

        # xpath-путь к заголовкам новостей
        a_xpath = "./descendant::a[contains(@class,'link_theme_black')]"

        links = news_block.xpath(a_xpath + "/@href")
        # исправление относительных ссылок на абсолютные, так как
        # могут попадаться и абсолютные и относительные ссылки
        for i, href in enumerate(links):
            if href[0] == '/':
                links[i] = main_link + href

        titles = news_block.xpath(a_xpath + "/text()")

        sdt_xpath = "/descendant::div[@class='story__date']/text()"
        raw_str = news_block.xpath(sdt_xpath)

        # парсер данных об источнике и о дате-времени в ISO-формат
        today = dt.datetime.utcnow()
        datetimes, sources = [], []
        for raw in raw_str:
            elems = raw.split('\xa0')
            if len(elems) > 1:
                if elems[1] == 'в':
                    # вчера
                    hour, mins = [int(x) for x in elems[2].split(':')]
                    yesterday = today - dt.timedelta(days=1)
                    datetime = dt.datetime(yesterday.year, yesterday.month, yesterday.day, hour, mins, 0, 0)
                    datetimes.append(datetime.isoformat()+'+03:00')
                    sources.append(elems[0][:-6])
                else:
                    # раньше, чем вчера
                    day = int(elems[0][-3:])
                    month = month_dict[elems[1]]
                    hour, mins = [int(x) for x in elems[3].split(':')]
                    datetime = dt.datetime(today.year, month, day, hour, mins, 0, 0)
                    datetimes.append(datetime.isoformat()+'+03:00')
                    sources.append(elems[0][:-3])
            else:
                # сегодня
                hour, mins = [int(x) for x in elems[0][-5:].split(':')]
                datetime = dt.datetime(today.year, today.month, today.day, hour, mins, 0, 0)
                datetimes.append(datetime.isoformat()+'+03:00')
                sources.append(elems[0][:-6])

        return get_data(links, titles, datetimes, sources)

    else:
        print('Yandex: error')


def lentaru():
    """
    Названия новостей и ссылки собираются с главной страницы в мобильной версии.
    Допускается, что источник всегда lenta.ru.
    Дата-время публикации собираются с соответствующих страниц новостей в десктопной версии.
    """
    print('Сбор на lenta.ru')
    main_link = 'https://lenta.ru'
    time.sleep(1)
    response = requests.get('https://m.lenta.ru', headers=MOBILE)

    if response.ok:
        root = html.fromstring(response.text)
        news_blocks = root.xpath("//div[@class='main-page__top']//li/a")

        links, titles, datetimes, sources = [], [], [], []

        for block in news_blocks:
            link = main_link + block.xpath("./@href")[0]
            links.append(link)
            titles.append(block.xpath("./div[1]/div[1]/text()")[0])
            sources.append('Lenta.ru')

            time.sleep(1)
            response = requests.get(link, headers=DESKTOP)
            if response.ok:
                root = html.fromstring(response.text)
                datetimes.append(root.xpath("//time[@class='g-date']/@datetime")[0])
            else:
                print('Lenta.ru: error')

        return get_data(links, titles, datetimes, sources)

    else:
        print('Lenta.ru: error')


client = MongoClient('localhost', 27017)
news_db = client['news_db']
news_collection = news_db.news

news = lentaru() + yandex() + mailru()
print('Собрано', len(news), 'новостей.')

added = 0
for document in news:
    try:
        news_collection.insert_one(document)
    except DuplicateKeyError:
        pass
    else:
        added += 1

print('Добавлено в базу', added, 'новых.')
print('Всего', news_collection.estimated_document_count(), 'новостей в базе.')
