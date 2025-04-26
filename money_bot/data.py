import yfinance as yf
import pandas as pd
import numpy as np
import json
from scipy.stats import norm
import time

# 计算年化收益率（CAGR）
def calculate_cagr(start_price, end_price, years):
    return (end_price / start_price) ** (1 / years) - 1

# 计算波动率（标准差）
def calculate_volatility(price_data):
    return price_data.pct_change().std() * np.sqrt(252)

# 计算夏普比率（Sharpe Ratio）
def calculate_sharpe_ratio(price_data, risk_free_rate=0.02):
    daily_returns = price_data.pct_change().dropna()
    excess_returns = daily_returns - risk_free_rate / 252
    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)

def calculate_max_drawdown(price_data):
    running_max = price_data.cummax()
    drawdown = (price_data - running_max) / running_max
    max_drawdown = drawdown.min()
    return max_drawdown

# 获取基金数据并计算特征
def get_fund_data(fund_code):
    try:
        fund = yf.Ticker(fund_code)
        historical_data = fund.history(period="1y")  # 获取过去1年的数据
        if historical_data.empty:
            print(f"基金代码 {fund_code} 的历史数据为空")
            return None
    except Exception as e:
        print(f"获取基金代码 {fund_code} 的数据时出错: {e}")
        return None
    
    # 计算特征
    start_price = historical_data['Close'].iloc[0]
    end_price = historical_data['Close'].iloc[-1]
    
    cagr = calculate_cagr(start_price, end_price, 1)
    volatility = calculate_volatility(historical_data['Close'])
    sharpe_ratio = calculate_sharpe_ratio(historical_data['Close'])
    max_drawdown = calculate_max_drawdown(historical_data['Close'])
    
    # 特征字典
    fund_features = {
    "fund_code": fund_code,
    "fund_name": fund.info.get('shortName', '未知基金'),
    "category": fund.info.get('category', '未知类别'),
    "expense_ratio": fund.info.get('expenseRatio', 0.0),  # 默认为 0.0
    "annual_return": cagr,
    "volatility": volatility,
    "sharpe_ratio": sharpe_ratio,
    "max_drawdown": max_drawdown,
    "five_year_growth": cagr,
}
    return fund_features

# 500只基金代码（这里只是示例，实际使用时你可以根据需要填写更多基金代码）
fund_codes = ['VTSAX', 'VTI', 'VOO', 'SPY', 'FXAIX', 'SCHB', 'IVV', 'FZROX', 'VFINX', 'VIG']

# 处理基金数据
fund_data = []
for fund_code in fund_codes:
    fund_features = get_fund_data(fund_code)
    if fund_features:
        fund_data.append(fund_features)
    time.sleep(2)  # 每次请求后暂停 2 秒
try:
    with open("fund_data.json", "w", encoding="utf-8") as json_file:
        json.dump(fund_data, json_file, ensure_ascii=False, indent=4)
    print(f"基金的特征已保存为 fund_data.json")
except Exception as e:
    print(f"保存 JSON 文件时出错: {e}")