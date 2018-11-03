from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed


class FirstStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(FirstStrategy, self).__init__(feed)
        self.__instrument = instrument
    
    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())

feed = quandlfeed.Feed()
feed.addBarsFromCSV('orcl', 'WIKI-ORCL-2000-quandl.csv')

strat = FirstStrategy(feed, 'orcl')
strat.run()
