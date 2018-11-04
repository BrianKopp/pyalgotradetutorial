from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import ma

class SmaStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod: int):
        super(SmaStrategy, self).__init__(feed, 1000)
        self.__position = None
        self.__instrument = instrument
        self.setUseAdjustedValues(True)
        self.__sma = ma.SMA(feed[instrument].getPriceDataSeries(), smaPeriod)
        print('initial portfolio value: {:.2f}'.format(self.getBroker().getEquity()))
        return
    
    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info('BUY at {:.2f}'.format(execInfo.getPrice()))
        return
    
    def onEnterCanceled(self, position):
        self.__position = None
        return
    
    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info('SELL at {:.2f}'.format(execInfo.getPrice()))
        self.__position = None
        return

    def onExitCanceled(self, position):
        self.__position.exitMarket()
        return
    
    def onBars(self, bars):
        if self.__sma[-1] is None:
            return
        bar = bars[self.__instrument]
        # no position currently
        if self.__position is None:
            # if price is above sma, buy
            if bar.getPrice() > self.__sma[-1]:
                self.__position = self.enterLong(self.__instrument, 10, True)
        elif bar.getPrice() < self.__sma[-1] and not self.__position.exitActive():
            self.__position.exitMarket()
        return

feed = quandlfeed.Feed()
feed.addBarsFromCSV('orcl', 'WIKI-ORCL-2000-quandl.csv')

strat = SmaStrategy(feed, 'orcl', 15)
strat.run()
print('Final portfolio value: {:.2f}'.format(strat.getBroker().getEquity()))
