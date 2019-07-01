"""
3 Массив размером 2m + 1, где m — натуральное число, заполнен случайным образом. Найдите в массиве медиану. Медианой
называется элемент ряда, делящий его на две равные части: в одной находятся элементы, которые не меньше медианы, в
другой — не больше медианы.

Примечание: задачу можно решить без сортировки исходного массива. Но если это слишком сложно, используйте метод
сортировки, который не рассматривался на уроках (сортировка слиянием также недопустима).
"""

from random import randint


# массив случайных целых чисел размером 2*m+1 в интервале [start, end]
def rnd_arr(start, end, m):
    return [randint(start, end) for _ in range(2*m + 1)]


# простой и неэффективный способ
def mediana_with_sort(array):
    return sorted(array)[len(array)//2]


def mediana_without_sort(array):
    for i in array:
        less, more, equals= 0, 0, 0
        for j in array:
            if i > j:
                less += 1
            elif i < j:
                more += 1
            else:
                equals += 1
        if abs(less - more) < equals:
            return i


arr = rnd_arr(0, 20, 10)
print(f'Исходный массив:  {arr}')
print(f'Медианна массива:   (с сорт): {mediana_with_sort(arr)}')
print(f'Медианна массива: (без сорт): {mediana_without_sort(arr)}')


# рандомный тест. будем считать, что mediana_with_sort() - эталонная функция
def test(count):
    for i in range(count):
        _rnd = randint(-100, 100)
        test_arr = rnd_arr(_rnd, _rnd + randint(10, 100), count)
        if mediana_with_sort(test_arr) == mediana_without_sort(test_arr):
            print(f'#{i+1} ok', end='')
            print('\n', end='') if (i+1) % 9 == 0 else print('\t\t', end='')
        else:
            print(f'\n#{i+1} FAIL in {test_arr}\n')


test(225) # все ок
