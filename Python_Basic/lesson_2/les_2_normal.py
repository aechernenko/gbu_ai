# Задача-1:
# Дан список, заполненный произвольными целыми числами, получите новый список,
# элементами которого будут квадратные корни элементов исходного списка,
# но только если результаты извлечения корня не имеют десятичной части и
# если такой корень вообще можно извлечь
# Пример: Дано: [2, -5, 8, 9, -25, 25, 4]   Результат: [3, 5, 2]

from random import randint
from math import sqrt

print('Task #1')

input_list = [randint(-100, 100) for _ in range(15)]
print(input_list)

sq_input_list = []
for item in input_list:
    if item >= 0:
        sq_item = int(sqrt(item))
        if sq_item**2 == item:
            sq_input_list.append(sq_item)

print(sq_input_list)

# Задача-2: Дана дата в формате dd.mm.yyyy, например: 02.11.2013.
# Ваша задача вывести дату в текстовом виде, например: второе ноября 2013 года.
# Склонением пренебречь (2000 года, 2010 года)

print('\nTask #2')

input_date = '25.06.1992'
print(input_date)

dd_str = 'первое, второе, третье, четвертое, пятое, шестое, седьмое, восьмое, девятое, десятое, одинадцатое, ' \
         'двенадцатое, тринадцатое, четырнадцатое, пятнадцатое, шестнадцатое, семнадцатое, восемнадцатое, '    \
         'девятнадцатое, двадцатое, двадцать перове, дадцать второе, двадцать третье, двадцать четвертое, '    \
         'двадцать пятое, двадцать шестое, двадцать седьмое, двадцать восьмое, двадцать девятое, тридцатое, '  \
         'тридцать первое'
mm_str = 'января, февраля, марта, апреля, мая, июня, июля, августа, сентября, октябрся, ноября, декабря'

dd = dd_str.split(sep=', ')
mm = mm_str.split(sep=', ')
date = list(map(int, input_date.split(sep='.')))

print(dd[date[0] - 1], mm[date[1] - 1], date[2], 'года')

# Задача-3: Напишите алгоритм, заполняющий список произвольными целыми числами
# в диапазоне от -100 до 100. В списке должно быть n - элементов.
# Подсказка:
# для получения случайного числа используйте функцию randint() модуля random

print('\nTask #3')


def random_list(n):
    return [randint(-100, 100) for _ in range(n)]


print(random_list(5))
print(random_list(10))
print(random_list(15))

# Задача-4: Дан список, заполненный произвольными целыми числами.
# Получите новый список, элементами которого будут:
# а) неповторяющиеся элементы исходного списка:
# например, lst = [1, 2, 4, 5, 6, 2, 5, 2], нужно получить lst2 = [1, 2, 4, 5, 6]
# б) элементы исходного списка, которые не имеют повторений:
# например, lst = [1 , 2, 4, 5, 6, 2, 5, 2], нужно получить lst2 = [1, 4, 6]

print('\nTask #4')

a_lst = [1, 2, 4, 5, 6, 2, 5, 2]
a_lst2 = list(set(a_lst))

print('a)', a_lst, a_lst2)

b_lst = [1, 2, 4, 5, 6, 2, 5, 2]
b_lst_copy = b_lst[:]  # извиняюсь, копировать массивы - дурной тон, но хочется быстрее закончить и спать :)
b_lst2 = list(set(b_lst))

for item in set(b_lst):
    b_lst_copy.remove(item)
    if item in b_lst_copy:
        b_lst2.remove(item)

print('б)', b_lst, b_lst2)