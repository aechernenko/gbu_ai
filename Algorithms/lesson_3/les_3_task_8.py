# Матрица 5x4 заполняется вводом с клавиатуры, кроме последних элементов строк. Программа должна вычислять сумму
# введенных элементов каждой строки и записывать ее в последнюю ячейку строки. В конце следует вывести полученную
# матрицу.


# параметры матрицы
COLUMNS = 5
LINES = 4

# создание и заполнение матрицы с клавиатуры
print(f'Для матрицы {COLUMNS}x{LINES}:')
matrix = []
for i in range(LINES - 1):
    new_line = [int(el) for el in input(f'Введите {COLUMNS - 1} чисел через пробел для {i} строки: ').split()]
    matrix.append(new_line)

# буферный список сумм по столбцам
sum_col = [0 for _ in range(COLUMNS)]

# подсчет сумм по столбцам и строкам
# добавление крайних строки и столбца с суммами
for line in matrix:
    sum_line = 0  # переменная для накопления суммы элементов строки
    for i, element in enumerate(line):
        sum_line += element
        sum_col[i] += element
    line.append(sum_line)
    sum_col[-1] += sum_line
matrix.append(sum_col)

# вывод результирующей матрицы с разграничением последних строки и столбца
print(f'Результирующая матрица {COLUMNS}x{LINES}:')
for i, line in enumerate(matrix):
    if i == LINES - 1:
        print('-\t' * (COLUMNS - 1), end='+\t-\n')
    for k, element in enumerate(line):
        if k == COLUMNS - 1:
            print('|', end='\t')
        print(element, end='\t') if k < COLUMNS - 1 else print(element)
