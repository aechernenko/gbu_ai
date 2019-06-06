# Задание-2: EASY
# Дан шестизначный номер билета. Определить, является ли билет счастливым.
# Решение реализовать в виде функции.
# Билет считается счастливым, если сумма его первых и последних цифр равны.
# !!!P.S.: функция не должна НИЧЕГО print'ить

from functools import reduce


def lucky_ticket(ticket_number):
    full_num = str(ticket_number).zfill(6)

    def summ(start, end):
        return reduce(lambda a, b: int(a) + int(b), full_num[start:end])

    if summ(None, 3) == summ(3, None):
        return True
    else:
        return False


print(lucky_ticket(123006))
print(lucky_ticket(12321))
print(lucky_ticket(436751))


# Задание-1: NORMAL
# Напишите функцию, возвращающую ряд Фибоначчи с n-элемента до m-элемента.
# Первыми элементами ряда считать цифры 1 1

def fibonacci(n, m):
    fib, fir, sec = [1,1], 1, 1
    for i in range(2, m + 1):
        fir, sec = sec, fir + sec
        fib.append(sec)
    return fib[n:]


N, M = 5, 8
print(f'от {N} до {M} ряд: {fibonacci(N,M)}')


