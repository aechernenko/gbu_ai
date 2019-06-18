from collections import namedtuple
from functools import reduce

num = int(input('Введите количество предприятий: '))
Enterprise = namedtuple('Enterprise', 'name quarters profit')

enterprises = []

for i in range(1, num + 1):
    name = input(f'Введите название {i}-го предприятия: ')
    quarters = [int(input(f'Введите прибыль "{name}" за {q}-й квартал: ')) for q in (1, 2, 3, 4)]
    profit = sum(quarters)

    enterprises.append(
        Enterprise(
            name=name,
            quarters=quarters,
            profit=profit,
        )
    )

average_profit = reduce(lambda a, b: a + b, [enterprise.profit for enterprise in enterprises]) / len(enterprises)

print('Средняя прибыль за год среди предприятий: ', average_profit)

print('Предприятия, имеющие прибыль ВЫШЕ среднего:')
for enterprise in enterprises:
    if enterprise.profit > average_profit:
        print('\t', enterprise.name)

print('Предприятия, имеющие прибыль НИЖЕ среднего:')
for enterprise in enterprises:
    if enterprise.profit < average_profit:
        print('\t', enterprise.name)
