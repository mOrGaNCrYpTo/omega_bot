from pyalgotrade.barfeed import csvfeed

class OneHourBarFeed(csvfeed.GenericBarFeed):
    def __init__(self, frequency):
        super().__init__(frequency)

    def barsHaveAdjClose(self):
        return True

    def addBarsFromCSV(self, instrument, path, timezone=None):
        super().addBarsFromCSV(instrument, path, "openTime", "openPrice", "highPrice", "lowPrice", "closePrice", "volume", None, "%Y-%m-%d %H:%M:%S", timezone)