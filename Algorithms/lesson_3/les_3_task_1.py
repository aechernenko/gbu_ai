# В диапазоне натуральных чисел от 2 до 99 определить, сколько из них кратны каждому из чисел в диапазоне от 2 до 9.


# диапазон делимых
FIRST_DIVIDEND = 2
LAST_DIVIDEND = 99
RAG_DIVIDEND = range(FIRST_DIVIDEND, LAST_DIVIDEND + 1)

# диапазон делителей
FIRST_DIVIDER = 2
LAST_DIVIDER = 9
RNG_DIVIDER = range(FIRST_DIVIDER, LAST_DIVIDER + 1)

# создание списка счетчиков для каждого из делителей и их обнуление
counter = [0 for _ in RNG_DIVIDER]

# подсчет для каждого делителя, сколько делимых ему кратны
for dividend in RAG_DIVIDEND:
    for i, divider in enumerate(RNG_DIVIDER):
        if dividend % divider == 0:
            counter[i] += 1

print(f'B диапазоне от {FIRST_DIVIDEND} до {LAST_DIVIDEND} картны числам:')

# print([(i+FIRST_DIVIDER, count) for i, count in enumerate(counter)])

# Вывод результата и филологический алгоритм :)
for i, divider in enumerate(RNG_DIVIDER):
    print(f'\t{divider}: {counter[i]}', end='')
    if counter[i] % 100 in range(5, 21):
        print('чисел')
    elif counter[i] % 10 in (2, 3, 4):
        print('числа')
    elif counter[i] % 10 == 1:
        print('число')
    else:
        print('чисел')
