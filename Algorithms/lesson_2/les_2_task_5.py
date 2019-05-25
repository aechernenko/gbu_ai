# 5. Вывести на экран коды и символы таблицы ASCII, начиная с символа под номером 32 и заканчивая 127-м включительно.
# Вывод выполнить в табличной форме: по десять пар "код-символ" в каждой строке.


FIRST = 32
LAST = 127

table = ''
counter = 0

for i in range(FIRST, LAST+1):
    table += str(i) + '-' + chr(i)
    if counter < 10:
        counter += 1
        table += '\t'
    else:
        counter = 0
        table += '\n'

print(table)

