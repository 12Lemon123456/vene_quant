import yfinance as yf
import pandas as pd

# ========== 1. 数据读取 ==========
# 下载苹果公司股票数据（2023年）
symbol = "AAPL"
start_date = "2023-01-01"
end_date = "2024-01-01"

# 使用yfinance获取数据
df = yf.download(symbol, start=start_date, end=end_date, progress=False)
df = df.sort_index(ascending=True)  # 确保时间升序

# ========== 2. 数据筛选（df.loc[]） ==========
# 示例1：选取2023-06月的所有数据（行筛选）
june_data = df.loc['2023-06']
print("2023年6月数据前5行：\n", june_data.head())

# 示例2：选取特定日期范围并仅保留收盘价（行列混合筛选）
subset = df.loc['2023-10-01':'2023-10-15', ['Close']]
print("\n2023年10月1-15日收盘价：\n", subset)

# ========== 3. 时间序列处理（df.resample()） ==========
# 示例：按月重采样计算月平均收盘价
monthly_avg = df['Close'].resample('ME').mean()  # 'M'表示按月聚合
print("\n2023年各月平均收盘价：\n", monthly_avg)

# ========== 4. 计算过去30天平均收盘价 ==========
# 直接基于日级数据计算滚动平均
df['30D_MA'] = df['Close'].rolling(
    window=30, 
    min_periods=1  # 允许最小1天数据计算（初期逐步增长）
).mean()

# 输出结果
print("\n最近5天的收盘价和30天均价：\n", df[['Close', '30D_MA']].tail())

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# 绘制收盘价与30日均线
plt.figure(figsize=(10, 6))  # 增大画布尺寸
plt.plot(df.index, df['Close'], label='Close Price', alpha=0.6)
plt.plot(df.index, df['30D_MA'], label='30D Moving Avg', color='red', linewidth=2)
plt.title(f"{symbol} Closing Price vs 30-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid(linestyle='--', alpha=0.5)
plt.tight_layout()  # 在 plt.show() 前调用
plt.show()
