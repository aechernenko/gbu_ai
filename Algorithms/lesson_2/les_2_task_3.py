# 3. Сформировать из введенного числа обратное по порядку входящих в него цифр и вывести на экран. Например, если
# введено число 3486, надо вывести 6843.


def rec(n):
    if n == 0:
        return ''
    else:
        return str(num // (10**(length-n)) % 10) + rec(n-1)


num = input('Введите число: ')
length = len(num)
num = int(num)

print(f'Обратный порядок: {rec(length)}')