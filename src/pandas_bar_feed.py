from pyalgotrade import bar
from pyalgotrade.barfeed import barfeed
from pyalgotrade.utils import dt

class PandasBarFeed(barfeed.BaseBarFeed):
    def __init__(self, frequency, timezone=None):
        super(PandasBarFeed, self).__init__(frequency, timezone)
        self.__bars = {}

    def barsHaveAdjClose(self):
        return False

    def addBarsFromDataFrame(self, symbol, dataFrame):
        self.__bars[symbol] = []
        for dateTime, row in dataFrame.iterrows():
            bar_ = bar.BasicBar(
                dateTime,
                row['open'],
                row['high'],
                row['low'],
                row['close'],
                row['volume'],
                self.getFrequency(),
                None,
                row['adj_close'],
                row.name,
                symbol
            )
            self.__bars[symbol].append(bar_)
        self.__bars[symbol].sort(key=lambda x: x.getDateTime())

    def getNextBars(self):
        dateTime = None
        bars = []
        for symbol, symbol_bars in self.__bars.items():
            if len(symbol_bars) > 0:
                bar_ = symbol_bars.pop(0)
                if dateTime is None:
                    dateTime = bar_.getDateTime()
                elif bar_.getDateTime() != dateTime:
                    raise ValueError("Different date times")
                bars.append(bar_)
        if dateTime is not None:
            return dt.localize(dateTime, self.getTimezone()), bars
        else:
            return None, None