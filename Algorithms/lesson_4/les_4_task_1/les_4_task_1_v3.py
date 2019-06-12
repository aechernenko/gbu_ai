# поиск из модуля NumPy
import numpy
import cProfile

np_1k = numpy.arange(1000)
np_10k = numpy.arange(10000)
np_100k = numpy.arange(100000)
np_1M = numpy.arange(1000000)
np_10M = numpy.arange(10000000)
np_1G = numpy.arange(1000000000)  # только для cProfile


def numpy_search(massive, value):
    return numpy.searchsorted(massive, value)


# пример: python -m timeit -n 100 -s "import les_4_task_1_v3 as x" "x.numpy_search(x.np_1k, len(x.np_1k)-2)"
# не знаю, как работает этот алгоритм, но поиск из любого места в массиве выдает за примерно одинаковое время
#
# 100 loops, best of 5: 1.48 usec per loop   -    массив   1 тыс элементов
# 100 loops, best of 5: 1.5  usec per loop   -    массив  10 тыс элементов
# 100 loops, best of 5: 1.5  usec per loop   -    массив 100 тыс элементов
# 100 loops, best of 5: 1.51 usec per loop   -    массив   1 млн элементов
# 100 loops, best of 5: 1.51 usec per loop   -    массив  10 млн элементов
# Выводы:
# константная зависимость, O(1)
# быстрее алгоритма бинарного поиска, реализованного на стандартном python

# в документации написано, что в searchsorted используется алгоритм бинарного поиска...
# библиотека numpy использует уже скомпилированный, оптимизированный код. возможно, время чуть меньше 1.5 мкс -
# - это время выполнения какого-то кода, который выполняется всегда, независимо от кода поиска
# а код поиска в конкретно наших примерах выполняется за пренебрежительно малое время, проверить на еще больших массивах
# слишком ресурсо затратно. Резуьтаты по массиву с 1 млрд выглядят странно:
#
# 1 loop, best of 5: 2.6 usec per loop
# :0: UserWarning: The test results are likely unreliable. The worst time (331 msec) was more than four times slower
# than the best time (2.6 usec).
#
# 1 loop, best of 5: 4.3 usec per loop
# :0: UserWarning: The test results are likely unreliable. The worst time (17.4 msec) was more than four times slower
# than the best time (4.3 usec).
#
# 10 loops, best of 5: 1.57 usec per loop
# :0: UserWarning: The test results are likely unreliable. The worst time (6.06 msec) was more than four times slower
# than the best time (1.57 usec).


# cProfile.run('numpy_search(np_1G, 999999998)')
"""
         8 function calls in 0.035 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.019    0.019 <string>:1(<module>)
        1    0.001    0.001    0.016    0.016 fromnumeric.py:1179(searchsorted)
        1    0.003    0.003    0.015    0.015 fromnumeric.py:54(_wrapfunc)
        1    0.003    0.003    0.019    0.019 les_4_task_1_v3.py:12(numpy_search)
        1    0.016    0.016    0.035    0.035 {built-in method builtins.exec}
        1    0.001    0.001    0.001    0.001 {built-in method builtins.getattr}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.010    0.010    0.010    0.010 {method 'searchsorted' of 'numpy.ndarray' objects}


"""