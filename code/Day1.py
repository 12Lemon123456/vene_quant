"""

# 需要先安装：pip install yfinance
import yfinance as yf  

# 1. 下载股票历史数据（以苹果公司为例）
stock_data = yf.download(
    "AAPL",                 # 股票代码
    start="2023-01-01",     # 起始日期
    end="2024-01-01",       # 结束日期
    progress=False          # 关闭进度条
)

# 2. 输出前5行数据
print("前5行数据：")
print(stock_data.head())

# 3. 可选：只保留关键列（如不需要Volume）
print("\n精简版（仅价格）：")
print(stock_data[['Open', 'High', 'Low', 'Close']].head())

Q:why不选此代码?
A: 历史数据下载不全, 无法显示. 故下载.csv文件进行操作.

"""

import pandas as pd

#苹果公司股票.csv文件的绝对路径
#之后所有代码, 均用苹果股票数据
data = pd.read_csv('AAPL_company_stock.csv')
#打印前5行数据
print(data.head())


