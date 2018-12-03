import talib
import numpy as np
import pandas as pd
from ..DyStockCtaTemplate import *

class DyST_MacdCycle(DyStockCtaTemplate):

    name = 'DyST_MacdCycle'

    chName = '周期共振'

    broker = 'simu6'

    backTestingMode = 'bar1m'
    multicycle = 'mcycle' #多周期15, 30, 60 分钟级别

    codes = ['600498.SH']

    #策略参数
    maxBuyNbr = 5

    def __init__(self, ctaEngine, info, state, strategyParam=None):
        super().__init__(ctaEngine, info, state, strategyParam)

        self._period = [15, 30, 60]

        self._close = pd.DataFrame(columns=['close'])
        self._close60 = pd.DataFrame(columns=['close'])
        self._close30 = pd.DataFrame(columns=['close'])
        self._close15 = pd.DataFrame(columns=['close'])

        self._df60 = pd.DataFrame(columns=['close'])
        self._df30 = pd.DataFrame(columns=['close'])
        self._df15 = pd.DataFrame(columns=['close'])

        self._m60cr = False #60分钟是否金叉
        self._m30cr = False #30分钟是否金叉
        self._m15cr = False #15分钟是否金叉

        self._lastBuyDeal = {}
        self._lastSellDeal = {}

        self._buySignal = {}

        #self._close60 = []
        self._curInit()

    def _curInit(self, date=None):
        self._marketData = []

    def _onOpenConfig(self):
        self._monitoredStocks.extend(self.codes)

    #开盘前的准备
    @DyStockCtaTemplate.onOpenWrapper
    def onOpen(self, date, codes=None):
        self._curInit(date)

        self._onOpenConfig()
        return True

    @DyStockCtaTemplate.onCloseWrapper
    def onClose(self):
        #清空sefl._close
        self._close.drop(self._close.index, inplace=True)
        self._close60 = pd.concat([self._close60, self._df60])
        self._close30 = pd.concat([self._close30, self._df30])
        self._close15 = pd.concat([self._close15, self._df15])

    def onTicks(self, ticks):
        for code, tick in ticks.items():
            #print(tick.date, tick.close)
            if tick.volume == 0:
                continue

            # 处理除复权
            if not self._processAdj(tick):
                continue

        self._procSignal(ticks)

    def onBars(self, bars):
        self.onTicks(bars)

    def _procSignal(self, ticks):
        #处理买入和卖出信号
        buyCodes, sellCodes = self._calcSignal(ticks)

        self._execSignal(buyCodes, sellCodes, ticks)


    def _calcSignal(self, ticks):
        """
            计算信号
            @return: [buy code], [sell code]
        """
        return self._calcSignal(ticks)


    #计算买入信号
    def _calcSignal(self, ticks):
        buyCodes = {}
        buyCodes1 = {}

        sellCodes = []

        for code, tick in ticks.items():

            self._close.loc[tick.datetime] = tick.close

            #计算不同周期的macd是否金叉

            if self._isPoint(tick, 60):
                self._df60 = self._processData(60, tick.date)
                tmp = pd.concat([self._close60, self._df60])

                #开始计算当前时间点的macd是否已经金叉
                if self._macdGoldCrossOver(tmp):
                    self._m60cr = True

                if self._macdDeathCrossOver(tmp):
                    self._m60cr = False

            if self._isPoint(tick, 30):
                # print(tick.time)
                self._df30 = self._processData(30, tick.date)
                tmp = pd.concat([self._close30, self._df30])

                # 开始计算当前时间点的macd是否已经金叉
                if self._macdGoldCrossOver(tmp):
                    self._m30cr = True

                if self._macdDeathCrossOver(tmp):
                    self._m30cr = False

            if self._isPoint(tick, 15):
                # print(tick.time)
                self._df15 = self._processData(15, tick.date)
                tmp = pd.concat([self._close15, self._df15])

                # 开始计算当前时间点的macd是否已经金叉
                if self._macdGoldCrossOver(tmp):
                    self._m15cr = True

                if self._macdDeathCrossOver(tmp):
                    self._m15cr = False

            if self._m15cr and self._m30cr and self._m60cr:

                #判断是否已经买入了
                if code in self._lastBuyDeal.keys():
                    continue

                #此时三个周期点均是金叉状态,买入时间点
                print(tick.datetime, '买入信号')
                self._lastBuyDeal[code] = tick.datetime
                buyCodes[code] = tick.price

            else:

                if code in self._lastBuyDeal.keys():
                    self._lastBuyDeal.pop(code)

                    for code, pos in self._curPos.items():
                        print('当前可卖出:', pos.availVolume,'当前总持仓:',pos.totalVolume, tick.datetime)
                        if pos.availVolume == 0:
                            continue

                        print(tick.datetime, pos.totalVolume, '卖出信号')
                        sellCodes.append(code)

        buyCodes = sorted(buyCodes, key=lambda k: buyCodes[k], reverse=False)

        return buyCodes, sellCodes
        # return buyCodes


    @DyStockCtaTemplate.processPreparedDataAdjWrapper
    def _processPreparedDataAdj(self, tick, preClose=None):
        """
            处理准备数据除复权
            @preClose: 数据库里的前一日收盘价，由装饰器传入。具体策略无需关注。
        """
        self.processDataAdj(tick, preClose, self._preparedData, ['walkMa'])
        self.processOhlcvDataAdj(tick, preClose, self._preparedData, 'days')

    @DyStockCtaTemplate.processPreparedPosDataAdjWrapper
    def _processPreparedPosDataAdj(self, tick, preClose=None):
        """
            处理准备数据除复权
            @preClose: 数据库里的前一日收盘价，由装饰器传入。具体策略无需关注。
        """
        self.processDataAdj(tick, preClose, self._preparedPosData, ['ma10', 'atr'], keyCodeFormat=False)


    def _processAdj(self, tick):
        """ 处理除复权 """
        return self._processPreparedDataAdj(tick) and self._processPreparedPosDataAdj(tick)

    def _macdGoldCrossOver(self, df):

        try:
            dif, dea, bar = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
            bar *= 2
        except Exception as ex:
            return False

        if (len(dif) <= 26): return False

        #判断是否是金叉
        if (dif[-1] > dea[-1] and dif[-2] < dea[-2]):
            return True

        return False

    def _macdDeathCrossOver(self, df):

        try:
            dif, dea, bar = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
            bar *= 2
        except Exception as ex:
            return False

        if (len(dif) <= 26): return False

        #判断是否是金叉
        if (dif[-1] < dea[-1] and dif[-2] > dea[-2]):
            return True

        return False

    def _processData(self, m, curTDay):
        dfMorning = self._close['{} 09:31:00'.format(curTDay):'{} 12:00:00'.format(curTDay)]
        dfMorning = dfMorning.resample(str(m) + 'min', closed='right', label='right', base=30).apply({'close': 'last'})

        dfAfternoon = self._close['{} 13:01:00'.format(curTDay):'{} 15:00:00'.format(curTDay)]
        dfAfternoon = dfAfternoon.resample(str(m) + 'min', closed='right', label='right').apply({'close': 'last'})

        return pd.concat([dfMorning, dfAfternoon])

    def _isPoint(self, tick, m):
        #print(tick.time[3:5], int(tick.time[3:5]) % m)
       # print(tick.time)
        if m is not 60:
            if int(tick.time[3:5]) % m == 0:
                return True

            return False
        else:
            #区分上午还是下午
            if int(tick.time[0:2]) in range(9,12):
                if int(tick.time[3:5]) == 30:
                    return True
            else:

                if int(tick.time[3:5]) == 0:
                    return True

            return False

    def _execSignal(self, buyCodes, sellCodes, ticks):
        """
            执行信号
            先卖后买，对于日线级别的回测，可以有效利用仓位。
        """
        self._execSellSignal(sellCodes, ticks)
        self._execBuySignal(buyCodes, ticks)

    def _execBuySignal(self, buyCodes, ticks):
        """
            执行买入信号
        """
        trueBuyCodes = []

        for code in buyCodes:
            if code in self._curPos:
                continue

            tick = ticks.get(code)
            if tick is None:
                continue

            trueBuyCodes.append(code)

            trueBuyCodes = trueBuyCodes[:self.maxBuyNbr]

            #现金比例
            cashRatio = self.getCashOverCapital()
            print(cashRatio)
            for code in trueBuyCodes:
                self.buyByRatio(ticks.get(code), min(30, 1 / len(trueBuyCodes) * cashRatio), self.cAccountCapital)


    def _execSellSignal(self, sellCodes, ticks):
        """
            执行卖出信号
        """
        for code in sellCodes:
            self.closePos(ticks.get(code))
