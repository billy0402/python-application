from calendar import monthrange
from datetime import datetime, date

import bitcoin_module
import matplotlib.pyplot as plt

url = 'https://www.coingecko.com/price_charts/1/twd/90_days.json'
df_bitcoin = bitcoin_module.get_prices(url)

total = best_ma = best_stop_earn = 0
for i in range(0, 2000, 100):
    for j in range(0, 2000, 100):
        temp_total = bitcoin_module.strategy(df_bitcoin, 100_0000, i, j)
        if temp_total > total:
            total = temp_total
            best_ma = i
            best_stop_earn = j

for i in range(best_ma - 100, best_ma + 100, 10):
    for j in range(best_stop_earn - 100, best_stop_earn + 100, 10):
        temp_total = bitcoin_module.strategy(df_bitcoin, 100_0000, i, j)
        if temp_total > total:
            total = temp_total
            best_ma = i
            best_stop_earn = j

print(f'total = {total}, Best MA = {best_ma}, Best stop earn = {best_stop_earn}')

today = datetime.now().date()
year, month = today.year, today.month - 1
_, last_day = monthrange(today.year, today.month)
first_day = date(year, month, 1)
last_day = date(year, month, last_day)

df_bitcoin['ma'] = df_bitcoin['twd'].rolling(window=best_ma).mean()
df_bitcoin[['twd', 'ma']].plot(kind='line', figsize=(15, 5),
                               xlim=(first_day, last_day))
plt.show()
