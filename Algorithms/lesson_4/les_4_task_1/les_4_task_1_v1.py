# Алгоритм прямого поиска индекса величины в массивве монотонно возрастающих чисел
import cProfile

py_1k = list(range(1000))
py_2k = list(range(2000))
py_5k = list(range(5000))
py_10k = list(range(10000))
py_20k = list(range(20000))
py_10M = list(range(10000000))  # только для cProfile


def line_search(massive, value):
    for i, item in enumerate(massive):
        if value == item:
            return i


# пример: python -m timeit -n 100 -s "import les_4_task_1_v1 as x" "x.line_search(x.py_1k, len(x.py_1k)-1)"
# во всех тестах искомая величина в конце массива - то есть рассматривается наихудший вариант
#
# 100 loops, best of 5: 44.4 usec per loop   -    массив  1 тыс элементов
# 100 loops, best of 5: 91.7 usec per loop   -    массив  2 тыс элементов
# 100 loops, best of 5: 234 usec per loop    -    массив  5 тыс элементов
# 100 loops, best of 5: 493 usec per loop    -    массив 10 тыс элементов
# 100 loops, best of 5: 1 msec per loop      -    массив 20 тыс элементов
# Вывод: линейная зависимость, O(n)



# cProfile.run('line_search(py_10M, 9999999)')
"""
   4 function calls in 0.534 seconds
   Ordered by: standard name
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.534    0.534 <string>:1(<module>)
        1    0.534    0.534    0.534    0.534 les_4_task_1_v1.py:11(line_search)
        1    0.000    0.000    0.534    0.534 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        
Слабых мест в алгоритме нет (не считая, что слабое место - сам алгоритм)
"""