# Алгоритм - решето Эратосфена. Сначала исследуется 100 чисел на предмет наличия простых, если простых чисел не хватает,
# добавляется еще 100 чисел для анализа, и так пока не найдется i-ое простое число
import cProfile


def simple(n):
    sieve = list(range(100))
    sieve[1] = 0
    while True:
        counter = 0
        sieve += list(range(len(sieve), len(sieve)+100))
        for i in range(2, len(sieve)):
            if sieve[i] != 0:
                j = i + i
                while j < len(sieve):
                    sieve[j] = 0
                    j += i
        for i in sieve:
            if i != 0:
                counter += 1
                if counter == n:
                    return i

"""
python -m timeit -n 100 -s "import les_4_task_2_v1 as x" "x.simple(1)"
100 loops, best of 5: 47.3 usec per loop
"x.simple(50)"
100 loops, best of 5: 149 usec per loop
"x.simple(100)"
100 loops, best of 5: 732 usec per loop
"x.simple(150)"
100 loops, best of 5: 1.43 msec per loop
"x.simple(200)"
100 loops, best of 5: 3.19 msec per loop
"x.simple(250)"
100 loops, best of 5: 4.69 msec per loop
"x.simple(300)"
100 loops, best of 5: 7.31 msec per loop
"x.simple(350)"
100 loops, best of 5: 12 msec per loop
"x.simple(400)"
100 loops, best of 5: 14.9 msec per loop
 
Апроксимация полученной зависимости в Google Таблицах производилась с помощью:
    полинома 2 степени y = 0,1176x^2 - 9,9467x + 262,47
    полинома 3 степени y = 0,00007*x^3 + 0,077*x^2 - 3,7799*x + 115,63

Проверим интерполируемые значения:
для 225-го числа "x.simple(225)"
100 loops, best of 5: 4 msec per loop
Аналитический расчет: 
    2 степ:   0,1176*(225*225) - 9,9467*(225) + 262,47 = 3978 мкс = 4 мс
    3 степ:   0,00007*225^3 + 0,077*225^2 - 3,7799*225 + 115,63 = 3961 мкс = 4 мс
Высокая точность интерполяции.

Проверим экстраполируемые значения:
"x.simple(600)"
100 loops, best of 5: 42.4 msec per loop
Аналитический расчет: 
    2 степ:   0,1176*(600*600) - 9,9467*(600) + 262,47 = 36630 мкс = 36,6 мс
    3 степ:   0,00007*600^3 + 0,077*600^2 - 3,7799*600 + 115,63 = 40688 мкс = 40,7 мс
    
"x.simple(800)"
100 loops, best of 5: 83.2 msec per loop 
Аналитический расчет:
    2 степ:   0,1176*(800*800) - 9,9467*(800) + 262,47 = 67569,11 мкс = 67,6 мс (расхождения 15,6 мс или 19%)
    3 степ:   0,00007*600^3 + 0,077*600^2 - 3,7799*600 + 115,63 = 82212 мкс = 82,2 мс (расхождения 1 мс или 1,2%)
    
ВЫВОДЫ:
Алгоритм O(n^3)
Время выполнения в мкс хорошо апроксимируется полиномом 3 степени y = 0,00007*x^3 + 0,077*x^2 - 3,7799*x + 115,63
где x - i-ое просто число
"""

# cProfile.run('simple(1000)')
"""
758865 function calls in 0.336 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.336    0.336 <string>:1(<module>)
        1    0.279    0.279    0.336    0.336 les_4_task_2_v1.py:6(simple)
        1    0.000    0.000    0.336    0.336 {built-in method builtins.exec}
   758861    0.057    0.000    0.057    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}

0.279 - время выполнения тела функции алгоритма для 1000-го простого числа
758861 - количество обращений к длинне исследуемого массива, len() - встроенная функция, занимает примерно 17 % времени 
работы алгоритма
"""

# Попробуем переписать алгоритм, постараясь свести к минимуму вызовы len(). Для этого введем две локальные переменные:
# l - длина массива
# lp - Длина массива после расширения


def simple_wo_len(n):
    sieve = list(range(100))
    sieve[1] = 0
    while True:
        counter = 0
        l = len(sieve)
        lp = l+100
        sieve += list(range(l, lp))
        for i in range(2, lp):
            if sieve[i] != 0:
                j = i + i
                while j < lp:
                    sieve[j] = 0
                    j += i
        for i in sieve:
            if i != 0:
                counter += 1
                if counter == n:
                    return i


# cProfile.run('simple_wo_len(1000)')
"""
83 function calls in 0.105 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.105    0.105 <string>:1(<module>)
        1    0.105    0.105    0.105    0.105 les_4_task_2_v1.py:98(simple_wo_len)
        1    0.000    0.000    0.105    0.105 {built-in method builtins.exec}
       79    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        
Количество вызовов len() сократилось в 9606 раз, практически исключив свои затраты на временные ресурсы, 
к тому же само тело функции стало в 2.5 раза быстрее работать.

ПРОВЕРИМ НОВЫЙ АЛГОРИТМ С TIMEIT:

"x.simple_wo_len(1)"
100 loops, best of 5: 32.7 usec per loop

"x.simple_wo_len(50)"
100 loops, best of 5: 97 usec per loop

"x.simple_wo_len(100)"
100 loops, best of 5: 418 usec per loop

"x.simple_wo_len(150)"
100 loops, best of 5: 949 usec per loop

"x.simple_wo_len(200)"
100 loops, best of 5: 2 msec per loop

"x.simple_wo_len(250)"
100 loops, best of 5: 3.02 msec per loop

"x.simple_wo_len(300)"
100 loops, best of 5: 4.75 msec per loop

"x.simple_wo_len(350)"
100 loops, best of 5: 7.1 msec per loop

"x.simple_wo_len(400)"
100 loops, best of 5: 9.46 msec per loop

Видно из Google Таблиц, что зависимость для новой функции также апроксимируетя полиномом 3 степени, однако, имеет 
меньшую скорость роста, по сравнению с предыдущим алгоритмом. Это связано с оптимизацией алгоритма, заключающейся 
в сокращении числа вызовов функции len() за счет использования двух дополнительных переменных
"""