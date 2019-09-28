import twstock  # https://github.com/mlouielu/twstock


class Stock:
    def __init__(self, stock_info):
        self._stock_id = stock_info[0].strip()
        self._low = float(stock_info[1])
        self._high = float(stock_info[2])

        self._name = ''
        self._price = 0

        self._action = ''
        self._why = ''

    def get_info(self):
        return self._stock_id, self._low, self._high, \
               self._name, self._price, \
               self._action, self._why

    def set_price(self):
        realtime = twstock.realtime.get(self._stock_id)
        if realtime['success']:
            self._name = realtime['info']['name']
            self._price = float(realtime['realtime']['latest_trade_price'])

    def set_best(self):
        stock = twstock.Stock(self._stock_id)
        best_four_point = twstock.BestFourPoint(stock).best_four_point()
        if best_four_point:
            self._action = '買進' if best_four_point[0] else '賣出'
            self._why = best_four_point[1]
        else:
            self._why = ''

    def alert(self, advice):
        alert_info = ('【通知】', self._name, f'股價: {self._price}', f'建議操作: {advice}')
        print('\n'.join(alert_info))
