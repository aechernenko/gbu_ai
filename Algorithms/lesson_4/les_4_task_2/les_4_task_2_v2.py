# классический способ проверки числа на простоту
# import cProfile


def prime(n):
    counter = 0
    i = 2
    while True:
        for k in range(2, i):
            if i % k == 0:
                break
        else:
            counter += 1
            if counter == n:
                return i
        i += 1


# cProfile.run('prime(1000)')

"""
   4 function calls in 0.222 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.221    0.221 <string>:1(<module>)
        1    0.221    0.221    0.221    0.221 les_4_task_2_v2.py:5(prime)
        1    0.000    0.000    0.222    0.222 {built-in method builtins.exec}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        
Простой алгоритм, все временные ресурсы затрачены на функцию prime()


"x.prime(1)"
100 loops, best of 5: 355 nsec per loop

"x.prime(50)"
100 loops, best of 5: 285 usec per loop

"x.prime(100)"
100 loops, best of 5: 1.26 msec per loop

"x.prime(150)"
100 loops, best of 5: 3.27 msec per loop

"x.prime(200)"
100 loops, best of 5: 5.94 msec per loop

"x.prime(250)"
100 loops, best of 5: 10.4 msec per loop

"x.prime(300)"
100 loops, best of 5: 16.5 msec per loop

"x.prime(350)"
100 loops, best of 5: 24.1 msec per loop

"x.prime(400)"
100 loops, best of 5: 30.1 msec per loop


Анализ графика для prime() в Google Таблицах показывает, что полученная зависимость хорошо апроксимируется полиномом 
4 степени. Заметно, что скорость роста функции гораздо выше, чем у предыдущих алгоритмов. Это вызванно слабостью
алгоритма. Алгоритм prime() перебирает все числа по порядку и проверяет кратно ли оно хотя бы одному какому-либо числу 
кроме 1 и самого себя.

"""
