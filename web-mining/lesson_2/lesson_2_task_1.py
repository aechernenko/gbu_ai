from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/78.0.3904.108 '
                         'YaBrowser/19.12.1.229 Yowser/2.5 Safari/537.36'}


def super_job(key_words, count=-1):
    main_link = 'https://www.superjob.ru'
    params = f'/vacancy/search/?keywords={key_words}&geo%5Bc%5D%5B0%5D=1'

    def get_html_page(num_of_page=1):
        add_page = '' if num_of_page < 2 else f'&page={num_of_page}'
        response = requests.get(main_link + params + add_page)
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
                return float('nan'), float('nan')
            else:
                salary = salary[:-2].replace('\xa0', '')
                if salary.find('от') != -1:
                    return float(salary[2:]), float('nan')
                elif salary.find('до') != -1:
                    return float('nan'), float(salary[2:])
                elif salary.find('—') != -1:
                    salary = salary.split('—')
                    return float(salary[0]), float(salary[1])
                else:
                    return float(salary), float(salary)

        salaries = [get_salary_data(salary) for salary in salaries_raw]

        data = [{} for _ in range(len(logos))]
        for dct, name, link, salary in zip(data, names, links, salaries):
            dct['name'] = name
            dct['link'] = link
            dct['min_salary'] = salary[0]
            dct['max_salary'] = salary[1]
            dct['source'] = 'SuperJob.ru'

        return data

    print('Поиск')
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
        return []

# count - количество выводимых вакансий 
# (count=-1 по умолчанию, выводит все найденные вакансии)
vacs = super_job('разработчик python', count=5)
pprint(vacs)
print('Найдено вакансий:', len(vacs))