from hashlib import sha1


def subs_count(string):
    h_subs = set()
    for i in range(len(string)):
        for j in range(i+1, len(string)+1):
            h_subs.add(sha1(string[i:j].encode('utf-8')).hexdigest())
    return len(h_subs) - 1  # за вычетом целой строки (когда i == 0, j == len(string))


inp = input('Введите строку: ')
print('Количество подстрок: ', subs_count(inp))

""" Некоторые результаты:
Введите строку: kate
Количество подстрок:  9

Введите строку: Я сразу смазал карту будней, плеснувши краски из стакана
Количество подстрок:  1552

Введите строку: Денег нет, но вы держитесь
Количество подстрок:  338

Введите строку: Эрмитаж проверил. Замечаний нет!
Количество подстрок:  514
"""


