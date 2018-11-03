from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma, rsi
from typing import Union


def safe_round(value: Union[float, None], digits: int) -> Union[float, None]:
    if value is not None:
        value = round(value, digits)
    return value


class FirstSmaRsiStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(FirstSmaRsiStrategy, self).__init__(feed)
        self.__instrument = instrument
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        return
    
    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info('{} {} {}'.format(bar.getClose(), safe_round(self.__rsi[-1], 2), safe_round(self.__sma[-1], 2)))
        return

feed = quandlfeed.Feed()
feed.addBarsFromCSV('orcl', 'WIKI-ORCL-2000-quandl.csv')

strat = FirstSmaRsiStrategy(feed, 'orcl')
strat.run()
