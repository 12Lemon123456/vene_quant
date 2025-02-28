#学习Backtrader/Zipline框架基础,理解回测框架流程（Strategy类、DataFeed）

import backtrader as bt
import pandas as pd
import os

# 检查文件路径
data_path = 'AAPL_company_stock.csv'
print("文件存在性:", os.path.exists(data_path))

# 验证原始数据
raw_df = pd.read_csv(data_path)
print("\n=== 原始数据前5行 ===\n", raw_df.head())

# 数据加载配置
data = bt.feeds.GenericCSVData(
    dataname=data_path,
    datetime=0, open=1, high=2, low=3, close=4, volume=5,
    dtformat='%Y-%m-%d',
    skiprows=1,    # 假设第一行是标题 "Date,Open,High,Low,Close,Volume"
    nullvalue=0.0
)

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.order = None
    
    def notify_order(self, order):
        if order.status == order.Completed:
            print(f"\n订单成交: {order.getstatusname()}")
            print(f"方向: {'买入' if order.isbuy() else '卖出'}")
            print(f"价格: {order.executed.price:.2f}")
            print(f"数量: {order.executed.size}")
            print(f"手续费: {order.executed.comm:.2f}\n")
            self.order = None
        
    def next(self):
        # 简单策略：第一天买入，第二天卖出
        if len(self) == 1 and not self.position:
            self.order = self.buy(size=100)
        elif len(self) == 2 and self.position:
            self.order = self.close()

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.001)

# 执行前数据验证
print("\n数据总量:", len(data))
print("前5个收盘价:", data.close.array[:5])


# 运行回测
print('\n初始资金: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('最终资金: %.2f' % cerebro.broker.getvalue())
