# 2. Посчитать четные и нечетные цифры введенного натурального числа. Например,
# если введено число 34560, в нем 3 четные # цифры (4, 6 и 0) и 2 нечетные (3 и 5).


num = input('Введите натуральное число: ')
count_1 = 0  # счетчик нечетных цифр
count_2 = 0  # счетчик четных цифр

for dig in num:
    if int(dig) % 2 == 0:
        count_2 += 1
    else:
        count_1 += 1

print(f'В числе "{num}"" содержится {count_1} нечетных цифр \n'
      f'В числе "{num}"" содержится {count_2} четных цифр')
