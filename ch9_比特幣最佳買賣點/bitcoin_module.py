import pandas as pd
import requests


def get_prices(url):
    response = requests.get(url)
    prices = response.json()['stats']

    df = pd.DataFrame(prices)
    df.columns = ['datetime', 'twd']
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.index = df['datetime']

    return df


def strategy(df, total, ma_num, stop_earn):
    """
    make state machine
    :param df: DataFrame
    :param total: 初期資金
    :param ma_num: 均線
    :param stop_earn: 停利點
    :return: 出淨值
    """
    df['ma'] = df['twd'].rolling(window=ma_num).mean()
    df = df[ma_num - 1:]
    entry_price = max_price = min_price = 0
    state = 'wait_long'

    for _, row in df.iterrows():
        now_price = row['twd']
        now_mean = row['ma']

        # 等待做多
        if state == 'wait_long' and now_price > now_mean:
            max_price = now_price
            entry_price = now_price
            state = 'entry_long'

        # 等待做空
        elif state == 'wait_short' and now_price < now_mean:
            min_price = now_price
            entry_price = now_price
            state = 'entry_short'

        # 進場作多
        elif state == 'entry_long':
            if now_price > max_price:
                max_price = now_price
            if now_price < max_price or \
                    now_price - entry_price > stop_earn != 0:
                total += now_price - entry_price
                state = 'wait_short'

        # 進場作空
        elif state == 'entry_short':
            if now_price < min_price:
                min_price = now_price
            if now_price > min_price or \
                    entry_price - now_price > stop_earn != 0:
                total += entry_price - now_price
                state = 'wait_long'

    return total
