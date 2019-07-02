"""
2 Отсортируйте по возрастанию методом слияния одномерный вещественный массив, заданный случайными числами на промежутке
[0; 50). Выведите на экран исходный и отсортированный массивы.
"""
from random import random
from collections import deque


# массив случайных вещественных целых чисел размером size в интервале [0, end_exc)
# uniform(a,b) не подойдет, тк генерирует в интервале [a,b]. А random() в интервале [0,1)
def rnd_arr(end_exc, size):
    return [round(random()*end_exc, 3) for _ in range(size)]


def merge_sort(array):

    def _merge(left, right):
        merged = []
        left = deque(left)
        right = deque(right)
        while left and right:
            if left[0] <= right[0]:
                merged.append(left.popleft())
            else:
                merged.append(right.popleft())
        if left:
            merged.extend(left)
        if right:
            merged.extend(right)
        return merged

    if len(array) <= 1:
        return array
    else:
        mid = len(array) // 2
        left_half = merge_sort(array[:mid])
        right_half = merge_sort(array[mid:])
        return _merge(left_half, right_half)


arr = rnd_arr(50, 10)
print(f'Исходный массив:           {arr}')
sorted_arr = merge_sort(arr)
print(f'Отсортиртированный массив: {sorted_arr}')
