from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from time import sleep
import json

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/78.0.3904.108 '
                         'YaBrowser/19.12.1.229 Yowser/2.5 Safari/537.36'}

NULL = None

def super_job(key_words, count=-1):
    main_link = 'https://www.superjob.ru'
    params = f'/vacancy/search/?keywords={key_words}&geo%5Bc%5D%5B0%5D=1'

    def get_html_page(num_of_page=1):
        add_page = '' if num_of_page < 2 else f'&page={num_of_page}'
        response = requests.get(main_link + params + add_page, headers=HEADERS)
        if response.ok:
            return bs(response.text, 'lxml')
        else:
            return None

    def get_pages_count(page):
        '''
        Сначала проверка на отсутствие результата (поиск текста "Вакансий не найдено").
        Если страниц 2 и больше обязательно присутствует кнопка "дальше".
        У кнопок следующей по порядку страницы и кнопки "дальше" в теге <a> имеется параметр rel="next",
        то есть если страниц больше 1, то всегда имеется две кнопки с указанным параметром, вторая из них - "дальше".
        Предыдущий элемент кнопки "дальше" содержит номер последней страницы.
        Если кнопок с параметром rel="next" нет, а вакансии найдены, то всего одна страница
        :param page: str, html страница
        :return: int, количество найденных страниц
        '''
        no_vacs_found = page.find('span', {'class': '_3mfro _1hP6a _2JVkc _2VHxz'})
        if no_vacs_found:
            if no_vacs_found.text == 'Вакансий не найдено':
                return 0
        else:
            next_buttons = page.find_all('a', {'rel': 'next'})
            if next_buttons:
                return int(next_buttons[-1].previous)
            else:
                return 1

    def get_data(page):
        '''
        У каждой вакансии есть контейнер для логотипа работодателя. От него и отталкиваемся в поиске информации
        :param page:
        :return:
        '''
        logos = page.find_all('div', {'class': '_1Tocb'})  # контейнеры для логотипов

        names = [logo.find_next_sibling().find_next().text for logo in logos]
        links = [main_link + logo.find_next_sibling().find('a')['href'] for logo in logos]
        salaries_raw = [logo.find_next_sibling().findChildren(recursive=False)[2].text for logo in logos]

        def get_salary_data(salary):
            if salary == 'По договорённости':
                return NULL, NULL, NULL
            else:
                salary = salary[:-2].replace('\xa0', '')
                if salary.find('от') != -1:
                    return float(salary[2:]), NULL, 'RUR'
                elif salary.find('до') != -1:
                    return NULL, float(salary[2:]), 'RUR'
                elif salary.find('—') != -1:
                    salary = salary.split('—')
                    return float(salary[0]), float(salary[1]), 'RUB'
                else:
                    return float(salary), float(salary), 'RUR'

        salaries = [get_salary_data(salary) for salary in salaries_raw]

        data = [{} for _ in range(len(logos))]
        for dct, name, link, salary in zip(data, names, links, salaries):
            dct['name'] = name
            dct['link'] = link
            dct['min_salary'] = salary[0]
            dct['max_salary'] = salary[1]
            dct['currency'] = salary[2]
            dct['source'] = 'SuperJob.ru'

        return data

    print('Поиск на superjob.ru')
    page_1 = get_html_page()
    pages_count = get_pages_count(page_1)
    print('1 страница из', pages_count)
    summary_data = get_data(page_1)
    if pages_count == 1:
        return summary_data[:count]
    elif pages_count > 1:
        for i in range(1, pages_count):
            print(i+1, 'страница из', pages_count)
            summary_data += get_data(get_html_page(i))
            if (count > 0) and (len(summary_data) > count):
                return summary_data[:count]
        return summary_data[:count]
    else:
        print('На superjob.ru ничего не найдено')
        return []

def hh(key_words, count=-1):
    main_link = 'https://sergievposad.hh.ru'
    add_params = '/search/vacancy?clusters=true&enable_snippets=true&' \
                 f'text={key_words.replace(" ", "+")}&L_save_area=true&area=113&from=cluster_area&showClusters = true'

    first_link = main_link + add_params

    def get_html_page(link):
        sleep(1)
        response = requests.get(link, headers=HEADERS)
        if response.ok:
            return bs(response.text, 'lxml')
        else:
            return None

    def is_found(page):
        if page.find('h1', {'data-qa': 'page-title'}).text.find('не найдено') == -1:
            return True
        else:
            return False

    def get_next_page_link(page):
        next_button = page.find('a', {'data-qa': 'pager-next'})
        if next_button:
            return main_link + next_button['href']
        else:
            return None

    def get_links(page):
        links = page.find_all('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        return [href['href'] for href in links]

    def get_data(page, link):
        dct = {}
        dct['link'] = link
        dct['name'] = page.find('h1', {'data-qa': 'vacancy-title'}).text
        dct['source'] = 'hh.ru'

        currency = page.find('meta', {'itemprop': 'currency'})
        if currency:
            dct['currency'] = currency['content']
        else:
            dct['currency'] = NULL

        minValue = page.find('meta', {'itemprop': 'minValue'})
        if minValue:
            dct['min_salary'] = float(minValue['content'])
        else:
            dct['min_salary'] = NULL

        maxValue = page.find('meta', {'itemprop': 'maxValue'})
        if maxValue:
            dct['max_salary'] = float(maxValue['content'])
        else:
            dct['max_salary'] = NULL

        return dct


    print('Поиск на hh.ru')
    cur_page = get_html_page(first_link)
    if is_found(cur_page):
        data = []
        while True:
            print('Еще страница')
            links = get_links(cur_page)
            data += [get_data(get_html_page(link), link) for link in links]
            if (len(data) > count) and (count > 0):
                break
            next_page_link = get_next_page_link(cur_page)
            if next_page_link:
                cur_page = get_html_page(next_page_link)
            else:
                break
        return data[:count]
    else:
        print('на hh.ru ничего не найдено')
        return []


def save_json(key_words, count_in_each=-1):
    sj_result = super_job(key_words, count_in_each)
    hh_result = hh(key_words, count_in_each)

    # сохранение всех данных в файл .json
    with open(f'{key_words}.json', 'w', encoding='utf-8') as file:
        json.dump(sj_result+hh_result, file, indent=2, ensure_ascii=False)

    return sj_result+hh_result


pprint(save_json('Нейронные сети', 30))
