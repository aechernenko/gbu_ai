# Алгоритм бинарного поиска индекса величины в массивве монотонно возрастающих чисел
import cProfile

py_1k = list(range(10**3))
py_10k = list(range(10**4))
py_100k = list(range(10**5))
py_1M = list(range(10**6))
py_10M = list(range(10**7))


def binary_search(massive, value):
    left = 0
    right = len(massive) - 1
    mid = left + (right - left) // 2
    while True:
        if value > massive[left]:
            if value < massive[mid]:
                right = mid
                mid = left + (right - left) // 2
            elif value > massive[mid]:
                if value < massive[right]:
                    left = mid
                    mid = left + (right - left) // 2
                else:
                    return right
            else:
                return mid
        else:
            return left
        if left + 1 == right:
            if massive[right] - value <= value - massive[left]:
                return right
            else:
                return left


# пример: python -m timeit -n 100 -s "import les_4_task_1_v2 as x" "x.line_search(x.py_100k, len(x.py_100k)-2)"
# во всех тестах искомая величина предпоследняя в массиве - то есть рассматривается наихудший вариант
#
# 100 loops, best of 5: 2.77 usec per loop   -    массив   1 тыс элементов
# 100 loops, best of 5: 3.86 usec per loop   -    массив  10 тыс элементов
# 100 loops, best of 5: 4.75 usec per loop   -    массив 100 тыс элементов
# 100 loops, best of 5: 5.47 usec per loop   -    массив   1 млн элементов
# 100 loops, best of 5: 6.51 usec per loop   -    массив  10 млн элементов
# Выводы:
# логарифмическая зависимость, O(log(n))
# с массивом  1 тыс элементов бинарный поиск работает в 16 раз быстрее линейного
# c массивом 10 тыс элементов бинарный поиск работает в 128 раз быстрее линейного


# cProfile.run('binary_search(py_10M, 9999998)')
"""
         5 function calls in 0.000 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 les_4_task_1_v2.py:11(binary_search)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

Слабых мест в алгоритме нет, видно, что в алгоритме используется built-in method builtins.len, но он совершенно
не влияет на скорость работы
"""