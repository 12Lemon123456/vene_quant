import pandas as pd
import matplotlib.pyplot as plt

# 从CSV文件读取数据（确保文件路径正确）
df = pd.read_csv('AAPL_company_stock.csv', parse_dates=['Date'], index_col='Date')

# 按日期升序排列（确保时间序列正确）
df = df.sort_index()

# 输出前5行数据
print("First 5 rows of data：")
print(df.head())

# 数据筛选示例：loc基础操作
print("\n筛选示例1（2022年3月数据）：")
print(df.loc['2022-03'])  # 筛选2022年3月所有数据

print("\n筛选示例2（特定日期收盘价）：")
print(df.loc['2020-03-23', 'Close'])  # 获取2020年3月23日收盘价

# 时间序列处理 - 计算过去30天平均收盘价
# （使用rolling窗口函数，min_periods处理初期数据不足情况）
df['30Day_aveLine'] = df['Close'].rolling(window=30, min_periods=1).mean()

# 提取最后30天均线值（验证计算）
print("\n最新的30天平均收盘价：{:.2f}".format(df['30Day_aveLine'].iloc[-1]))

# 可视化（可选）
df[['Close', '30Day_aveLine']].plot(figsize=(12,6), title='Appl_30Day_aveLine')
plt.show()
