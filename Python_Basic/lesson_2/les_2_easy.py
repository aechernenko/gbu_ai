# Задача-1:
# Дан список фруктов.
# Напишите программу, выводящую фрукты в виде нумерованного списка,
# выровненного по правой стороне.

# Пример:
# Дано: ["яблоко", "банан", "киви", "арбуз"]
# Вывод:
# 1. яблоко
# 2.  банан
# 3.   киви
# 4.  арбуз

# Подсказка: воспользоваться методом .format()

fruit_list = ["яблоко", "банан", "киви", "арбуз"]
for i, fruit in enumerate(fruit_list):
    print('{0}.{1:>7}'.format(i+1, fruit))

# Задача-2:
# Даны два произвольные списка.
# Удалите из первого списка элементы, присутствующие во втором списке.

from random import randint

first_list = [randint(0, 10) for _ in range(randint(3, 7))]
second_list = [randint(0, 10) for _ in range(randint(3, 7))]

print('before remove:')
print('1st:', first_list)
print('2nd:', second_list)

for item in second_list:
    while(item in first_list):
        first_list.remove(item)

print('after remove:')
print('1st:', first_list)
print('2nd:', second_list)

# Задача-3:
# Дан произвольный список из целых чисел.
# Получите НОВЫЙ список из элементов исходного, выполнив следующие условия:
# если элемент кратен двум, то разделить его на 4, если не кратен, то умножить на два.

int_list = [randint(0, 10) for _ in range(randint(3, 10))]

print('old list:', int_list)

new_int_list = []
for item in int_list:
    if item % 2 == 0:
        new_int_list.append(item / 4)
    else:
        new_int_list.append(item * 2)

print('new list:', new_int_list)
