# gbu_ai/Algorithms/lesson_3/les_3_task_2.py
# Во втором массиве сохранить индексы четных элементов первого массива. Например, если дан массив со значениями 8, 3,
# 15, 6, 4, 2, второй массив надо заполнить значениями 0, 3, 4, 5, (индексация начинается с нуля), т.к. именно в этих
# позициях первого массива стоят четные числа.


input_mas = [int(i) for i in input('Введите через пробел числа для заполнения массива: ').split()]

output_mas = []

for i, item in enumerate(input_mas):
    if item % 2 == 0:
        output_mas.append(i)

print(f'Входной массив чисел: {input_mas}')
print(f'Индексы четных чисел: {output_mas}')


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

"""
-------------------------РЕЗУЛЬТАТ 1:--------------------------
Введите через пробел числа для заполнения массива: 
Входной массив чисел: []
Индексы четных чисел: []
Память: 849
-------------------------РЕЗУЛЬТАТ 2:--------------------------
Введите через пробел числа для заполнения массива: 1
Входной массив чисел: [1]
Индексы четных чисел: []
Память: 961
-------------------------РЕЗУЛЬТАТ 3:--------------------------
Введите через пробел числа для заполнения массива: 2
Входной массив чисел: [2]
Индексы четных чисел: [0]
Память: 1017
-------------------------РЕЗУЛЬТАТ 4:--------------------------
Введите через пробел числа для заполнения массива: 1 2 3 4 5 6 7 8 9 0
Входной массив чисел: [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
Индексы четных чисел: [1, 3, 5, 7, 9]
Память: 1509
-------------------------РЕЗУЛЬТАТ 5:--------------------------
Введите через пробел числа для заполнения массива: 2 4 6 8 0 12 18 24 28 56
Входной массив чисел: [2, 4, 6, 8, 0, 12, 18, 24, 28, 56]
Индексы четных чисел: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Память: 1713
"""
