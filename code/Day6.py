import pandas as pd
import matplotlib.pyplot as plt

# 读取数据（假设文件包含日期和收盘价）
df = pd.read_csv('AAPL_company_stock.csv', parse_dates=['Date'], index_col='Date')
df = df.sort_index()  # 按日期排序

# 选择近一年的数据（避免图表太密集）
df = df[-365:]
close_prices = df['Close']

# --------------------------
# 方案一：使用TA-Lib计算MACD（建议首选）
# --------------------------
try:
    import talib
    # 计算MACD（参数：快线12天，慢线26天，信号线9天）
    macd_line, signal_line, macd_hist = talib.MACD(
        close_prices, 
        fastperiod=12, 
        slowperiod=26, 
        signalperiod=9
    )
    method = 'TA-Lib'
except ImportError:
    # --------------------------
    # 方案二：用Pandas手动计算（安装TA-Lib失败时使用）
    # --------------------------
    # 计算12日和26日EMA（指数移动平均）
    ema12 = close_prices.ewm(span=12, adjust=False).mean()
    ema26 = close_prices.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    
    # 计算信号线（MACD的9日EMA）
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    macd_hist = macd_line - signal_line
    #method = 'Pandas替代方案'
    method = 'Pandas alternative'

# 合并结果到DataFrame
df['MACD线'] = macd_line
df['信号线'] = signal_line
df['MACD柱'] = macd_hist

# --------------------------
# 绘制图表
# --------------------------
plt.figure(figsize=(12, 8))

# 股价图
plt.subplot(2, 1, 1)
#收盘价
plt.plot(df['Close'], label='closing price', color='blue')
#plt.title(f'苹果股价与MACD指标（计算方法: {method}）')
plt.title(f'Apple stock price and MACD indicator(Calculation method: {method})')
plt.legend()

# MACD图
plt.subplot(2, 1, 2)
#MACD线（快线）
plt.plot(df['MACD线'], label='MACD line (fast line)', color='orange')
#信号线（慢线）
plt.plot(df['信号线'], label='Signal line (slow line)', color='green')
#MACD柱
plt.bar(df.index, df['MACD柱'], label='MACD column', color=np.where(df['MACD柱']>0, 'red', 'lime'), alpha=0.5)
plt.axhline(0, color='gray', linestyle='--')
plt.legend()

plt.tight_layout()
plt.show()
