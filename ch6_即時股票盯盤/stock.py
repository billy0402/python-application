import time

from stock_module import Stock

stocks = list()
try:
    with open('stock.txt', 'r') as file:
        for line in file.readlines():
            stock_info = line.split(',')
            stock = Stock(stock_info)
            stocks.append(stock)
except Exception as e:
    print('stock.txt 讀取錯誤', e)

log_price = [''] * len(stocks)
log_best = log_price.copy()
check_counter = 1

while True:
    print(f'---------- 第 {check_counter} 次 ----------')
    for index, stock in enumerate(stocks):
        stock.set_price()
        stock.set_best()
        stock_id, low, high, name, price, action, why = stock.get_info()
        print(f'檢查: {name}, 股價: {price}, 區間: {low} ~ {high}')

        if price <= low and log_price[index] != '買進':
            stock.alert(f'買進 (股價低於{low})')
            log_price[index] = '買進'
        elif price >= high and log_price[index] != '賣出':
            stock.alert(f'賣出 (股價高於{high})')
            log_price[index] = '賣出'

        if why and log_best[index] != why:
            stock.alert(f'{action}({why})')
            log_best[index] = why

        print('-' * 30)

    check_counter += 1
    time.sleep(180)
