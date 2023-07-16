import backtrader as bt

class RiskManagement(bt.Strategy):
    params = (('stop_loss', 0.01), ('take_profit', 0.02),)

    def __init__(self):
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        if self.order:
            return
        if not self.position:
            self.order = self.buy_bracket(limitprice=self.data.close[0] * (1 + self.params.take_profit),
                                          stopprice=self.data.close[0] * (1 - self.params.stop_loss))
        else:
            self.order = self.sell_bracket(limitprice=self.data.close[0] * (1 - self.params.take_profit),
                                           stopprice=self.data.close[0] * (1 + self.params.stop_loss))

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
