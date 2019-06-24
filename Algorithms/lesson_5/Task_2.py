from collections import deque

fir = [char for char in input('Первое число: ').upper()]
sec = [char for char in input('Второе число: ').upper()]

HEX_DEC = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11,
           'C': 12, 'D': 13, 'E': 14, 'F': 15}

DEC_HEX = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B',
           12: 'C', 13: 'D', 14: 'E', 15: 'F'}


def hex_sum(first, second):
    d_fir = deque(first)
    d_sec = deque(second)
    d_res = deque()
    add = 0
    while d_fir or d_sec:
        if not d_fir:
            summ = HEX_DEC[d_sec.pop()] + add
        elif not d_sec:
            summ = HEX_DEC[d_fir.pop()] + add
        else:
            summ = HEX_DEC[d_fir.pop()] + HEX_DEC[d_sec.pop()] + add
        if summ > 15:
            add = 1
            summ -= 16
        else:
            add = 0
        d_res.appendleft(DEC_HEX[summ])
    if add:
        d_res.appendleft('1')
    return list(d_res)


def hex_mul(first, second):
    dec_sec = 0
    rev_sec = second[:]
    rev_sec.reverse()
    for i, x in enumerate(rev_sec):
        dec_sec += HEX_DEC[x] * (16**i)

    res = []
    for _ in range(dec_sec):
        res = hex_sum(res, first)

    return res


print('Сумма:', hex_sum(fir, sec))
print('Произведение:', hex_mul(fir, sec))
