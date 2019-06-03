# В массиве случайных целых чисел поменять местами минимальный и максимальный элементы.


from random import randint

# параметры массива случайных чисел
MIN_RND = 10
MAX_RND = 200
SIZE = 15

# создание и заполнение массива
before_mas = [randint(MIN_RND, MAX_RND) for _ in range(SIZE)]

# переменные мин., макс, и их индексы изначально соответствуют нулевому элементу массива
minimum, maximum = before_mas[0], before_mas[0]
min_index, max_index = 0, 0

# поиск минимума и максимума в массиве перебором, сохранение их инджексов
for i, item in enumerate(before_mas):
    if item < minimum:
        minimum = item
        min_index = i
    if item > maximum:
        maximum = item
        max_index = i

# копия массива, замена мин. и макс, местами
after_mas = before_mas[:]
after_mas[min_index], after_mas[max_index] = after_mas[max_index], after_mas[min_index]

print(f'Мин: {minimum}. Макс: {maximum}. Индексы: {min_index}, {max_index}.')
print('Массив до и после замены min и max местам соответственно:')
print(after_mas)
print(before_mas)
