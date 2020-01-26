import pandas as pd
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


df = pd.read_csv('opendata.csv', encoding='cp1251', parse_dates=['date'])

print('ТИПЫ ДАННЫХ:')
[print(f'{i}\t{name}') for i, name in enumerate(df['name'].unique())]
name_index = int(input('Введите номер типа данных из списка:'))
name = df['name'].unique()[name_index]

print('РЕГИОНЫ:')
[print(f'{i}\t{region}') for i, region in enumerate(df['region'].unique())]
region_index = int(input('Введите номер региона из списка:'))
region = df['region'].unique()[region_index]

date_min = input('Введите начальную дату в формате "yyyy-mm-dd":')
date_max = input('Введите конечную  дату в формате "yyyy-mm-dd":')

mask_regions = df['region'] == region
mask_names = df['name'] == name
mask_date_min = pd.to_datetime(date_min) < df['date']
mask_date_max = df['date'] < pd.to_datetime(date_max)

sample = df.loc[mask_regions & mask_names & mask_date_min & mask_date_max]

plt.plot(sample['date'], sample['value'])
plt.xlabel('Дата')
plt.ylabel('Значение')
plt.title(f'{name}\n{region}')
plt.show()
