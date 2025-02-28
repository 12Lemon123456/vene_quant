import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 读取CSV文件（注意路径正确性）
df = pd.read_csv('AAPL_company_stock.csv', 
                 parse_dates=['Date'],  # 将日期列转为datetime类型
                 index_col='Date'       # 设置日期为索引
                ).sort_index()          # 确保按日期升序排列

# 检查关键列是否存在
required_columns = ['Open', 'High', 'Low', 'Close']
if not all(col in df.columns for col in required_columns):
    raise ValueError("CSV文件中缺少必要列：'Open', 'High', 'Low', 'Close'")

# 提取最近一年的数据示例（避免图表过于密集）
#sample_data = df[-365:] 
# 修改原始代码中的 sample_data 定义
sample_data = df[-365:].copy()  # 关键：.copy() 强制创建独立副本


# 计算简单移动平均（SMA）
sample_data['SMA5'] = sample_data['Close'].rolling(window=5, min_periods=1).mean()
sample_data['SMA30'] = sample_data['Close'].rolling(window=30, min_periods=1).mean()



# 创建画布和坐标轴
fig, ax = plt.subplots(figsize=(15, 7))

# ---------------------------
# 第一部分：绘制K线图（核心代码）
# ---------------------------
for idx, row in sample_data.iterrows():
    # 计算颜色：收盘价>开盘价为绿色(涨)，否则红色(跌)
    color = 'green' if row['Close'] > row['Open'] else 'red'
    
    # 绘制垂直影线（最高价-最低价）
    ax.vlines(x=idx, 
              ymin=row['Low'], 
              ymax=row['High'], 
              color=color, 
              linewidth=1)
    
    # 绘制实体矩形（开盘价-收盘价）
    rect = plt.Rectangle((mdates.date2num(idx) - 0.3, row['Open']), 
                         0.6, 
                         row['Close'] - row['Open'],
                         facecolor=color)
    ax.add_patch(rect)

# ---------------------------
# 第二部分：添加均线
# ---------------------------
#蓝色:5日均线
#橘色:30日均线
ax.plot(sample_data['SMA5'], label='5-day moving average', color='blue', linewidth=1.5)
ax.plot(sample_data['SMA30'], label='30-day moving average', color='orange', linewidth=1.5)

# ---------------------------
# 图表装饰
# ---------------------------
#苹果公司股价走势 (K线 + 双均线
ax.set_title('Apple stock price trend', fontsize=14)
ax.set_xlabel('data', fontsize=12)
ax.set_ylabel('price (USD)', fontsize=12)
ax.legend()
plt.xticks(rotation=45)  # 旋转日期标签

# 设置日期格式（重要！）
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  
ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # 自动选择刻度间隔

plt.tight_layout()
plt.show()
