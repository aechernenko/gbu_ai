# gbu_ai/Algorithms/lesson_1/les_1_task_4.py
"""Написать программу, которая генерирует в указанных пользователем границах:
● случайное целое число,
● случайное вещественное число,
● случайный символ.
Для каждого из трех случаев пользователь задает свои границы диапазона.
Например, если надо получить случайный символ от 'a' до 'f', то вводятся эти символы. Программа должна вывести на
экран любой символ алфавита от 'a' до 'f' включительно."""


from random import randint, uniform

print('Для целых чисел:')
int_a = int(input('    введите нижнюю границу: '))
int_b = int(input('    введите верхнюю границу: '))

print('\nДля вещественных чисел:')
float_a = float(input('    введите нижнюю границу: '))
float_b = float(input('    введите верхнюю границу: '))

print('\nДля букв алфавита:')
ord_a = ord(input('    введите первую букву: '))
ord_b = ord(input('    введите вторую букву: '))

rand_int = randint(int_a, int_b)
rand_float = uniform(float_a, float_b)
rand_char = chr(randint(ord_a, ord_b))

print(f'\nСлучайное целое число: {rand_int}')
print(f'Случайное вещественное число: {rand_float}')
print(f'Случайная буква: {rand_char}')


# скрипт подсчета памяти
vars = list(globals().values())
size = 0
from sys import getsizeof as sz
for var in vars:
    if isinstance(var, dict):
        size += sz(var)
        size += sum([sz(i) for i in var.values()])
        size += sum([sz(i) for i in var.keys()])
    elif isinstance(var, list) or isinstance(var, tuple) or isinstance(var, set) or isinstance(var, frozenset):
        size += sz(var)
        size += sum([sz(i) for i in var])
    else:
        size += sz(var)
print('Память:', size)
# ps: скрипт не совершенен. в основном он подсчитывает толко память, занимаемую переменными программы, а так же память
# объектов, содержащихся в dict, list, tuple, set, frozenset.
# Что можно улучшить:
# 1) добавить анализ памяти внутри модулей, классов, экземляров и других объектов, на которые есть ссылки
# 2) придумать алгоритм глубокого подсчета памяти, если список содержит список, который содержит список и тд...
# 3) ???
# 4) PROFIT

"""
-------------------------РЕЗУЛЬТАТ 1:--------------------------
Для целых чисел:
    введите нижнюю границу: 1
    введите верхнюю границу: 11111111111111111111111111

Для вещественных чисел:
    введите нижнюю границу: 1
    введите верхнюю границу: 1111111111111111111111111111111111111111111

Для букв алфавита:
    введите первую букву: a
    введите вторую букву: q

Случайное целое число: 3167261619380244345232497
Случайное вещественное число: 8.172698764847721e+41
Случайная буква: n
Память: 1971

Process finished with exit code 0

-------------------------РЕЗУЛЬТАТ 2:--------------------------
Для целых чисел:
    введите нижнюю границу: 1
    введите верхнюю границу: 2

Для вещественных чисел:
    введите нижнюю границу: 1
    введите верхнюю границу: 2

Для букв алфавита:
    введите первую букву: a
    введите вторую букву: c

Случайное целое число: 1
Случайное вещественное число: 1.1100359623392313
Случайная буква: b
Память: 1955

Process finished with exit code 0
"""
