# Найти максимальный элемент среди минимальных элементов столбцов матрицы.


from random import randint

# параметры матрицы
COLUMNS = 8
LINES = 5
START_RND = 20
END_RND = 500

# создание и заполнение матрицы случайными числами
matrix = []
for _ in range(LINES):
    matrix.append([randint(START_RND, END_RND) for _ in range(COLUMNS)])

# вывод матрицы
print(f'Исследуемая матрица {COLUMNS}x{LINES}:')
for line in matrix:
    for i, element in enumerate(line):
        print(element, end='\t') if i < COLUMNS - 1 else print(element)

# буферный список минимальных элементов столбцов матрицы
min_line = matrix[0].copy()

# поиск в каждом столбце минимального элемента
for line in matrix:
    for i, element in enumerate(line):
        if element < min_line[i]:
            min_line[i] = element

print('\nСписок минимальных элементов в столбцах матрицы:')
print(min_line, end='\n\n')

# поиск максимального элемента в min_line
maximum = min_line[0]
for element in min_line:
    if element > maximum:
        maximum = element

print(f'Макс. элемент среди мин. элементов столбцов матрицы: {maximum}.')
