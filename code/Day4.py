#价格突破N日新高即买入


import pandas as pd
import matplotlib.pyplot as plt

# --- 1. 数据准备 ---
f = pd.read_csv('AAPL_company_stock.csv', 
                 parse_dates=['Date'], 
                 index_col='Date').sort_index()

# 参数设置
N = 20         # 突破N日新高周期
fee_rate = 0.0005  # 交易手续费率（0.05%）
slippage = 0.002   # 滑点（0.2%）

# --- 2. 策略逻辑实现 ---
# 计算N日最高价（填充初始NaN值）
df['N日最高价'] = df['High'].rolling(window=N).max().shift(1)
df['N日最高价'] = df['N日最高价'].ffill().bfill()  # 向前填充缺失值

# 生成信号：当日最高价突破N日最高价时买入
assert not df['N日最高价'].isnull().any(), "N日最高价列仍有缺失值！请检查数据或填充逻辑"
df['买入信号'] = df['High'] > df['N日最高价']

# 初始化持仓状态和交易记录
hold_position = False  # 是否持有多头仓位
trade_records = []     # 交易记录列表

# --- 3. 回测流程模拟 ---
# 综合修正后的完整处理流程：
# 计算初始N日最高价（含NaN）
df['N日最高价_初始'] = df['High'].rolling(window=N).max().shift(1)

# 分步骤填充：
df['N日最高价'] = (df['N日最高价_初始'].ffill()) 
# 向前填充（用前面有效值填充后面）.bfill()  # 向后填充（处理起始位置的NaN）

df = df.drop(columns=['N日最高价_初始'])  # 清理中间列

for i in range(len(df)):
    current_date = df.index[i]
    current_close = df['Close'].iloc[i]
    current_high = df['High'].iloc[i]
    
    # 存在买入信号且未持仓
    if df['买入信号'].iloc[i] and not hold_position:
        # 计算实际买入价格（考虑滑点）
        buy_price = current_high * (1 + slippage)
        # 记录买入
        trade_records.append({
            'date': current_date,
            'action': 'buy',
            'price': buy_price,
            'fee': buy_price * fee_rate
        })
        hold_position = True
    
    # 简单的卖出条件：持有时遇到收盘价下跌5%则卖出
    elif hold_position and (current_close < (trade_records[-1]['price'] * 0.95)):
        sell_price = current_close * (1 - slippage)
        trade_records.append({
            'date': current_date,
            'action': 'sell',
            'price': sell_price,
            'fee': sell_price * fee_rate
        })
        hold_position = False

# 添加在回测循环之后
if hold_position:
    # 以最后一天的收盘价强制平仓
    sell_price = df['Close'].iloc[-1] * (1 - slippage)
    trade_records.append({
        'date': df.index[-1],
        'action': 'sell',
        'price': sell_price,
        'fee': sell_price * fee_rate
    })


# --- 4. 结果分析 ---
# 将交易记录转为DataFrame
trades_df = pd.DataFrame(trade_records)

# 计算累计收益
if not trades_df.empty:
    # 计算单笔收益（考虑手续费）
    profit = []
    buy_records = trades_df[trades_df['action'] == 'buy']
    sell_records = trades_df[trades_df['action'] == 'sell']
    
    # ==== 修改后（正确方法） ====
    for buy, sell in zip(buy_records.itertuples(), sell_records.itertuples()):
        # 计算单笔收益
        pct = (sell.price - buy.price) / buy.price
        pct -= (buy.fee + sell.fee) / buy.price
        profit.append(pct)


    
    # 输出统计信息
    print(f"总交易次数：{len(profit)} 次")
    print(f"平均收益率：{sum(profit)/len(profit)*100:.2f}%")
else:
    print("期间无符合策略的交易")

# --- 5. 可视化信号 ---
plt.figure(figsize=(12,6))
#收盘价
plt.plot(df['Close'], label='closing price')
#N日最高价
plt.plot(df['N日最高价'], label=f'Highest price on {N} days', linestyle='--')

# 标记买入点
buy_dates = trades_df[trades_df['action']=='buy']['date']
plt.scatter(buy_dates, df.loc[buy_dates, 'Close'], marker='^', color='r', s=100, label='buy signal')

#价格突破策略信号演示
plt.title('Price Breakout Strategy Signal Demonstration')
plt.legend()
plt.show()
