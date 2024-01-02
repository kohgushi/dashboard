import streamlit as st
import pandas as pd
import datetime as dt
from src.stock import get_stock, create_stock_charts
import yaml

st.title("My Dashboard")

##########################################################
# 株価
##########################################################
# 表示期間変更ボタン
days = [30, 60, 120, 180, 365]
cols = st.columns(len(days))  # ボタンを横方向に配置
if "days_stock_chart" not in st.session_state:
    st.session_state.days_stock_chart = 120  # チャート表示期間


# ボタンが押されたときの挙動を設定
def set_days_stock_chart(days: int) -> None:
    """押されたボタンに応じて表示期間を変更するコールバック"""
    st.session_state.days_stock_chart = days


for col, day in zip(cols, days):
    with col:
        st.button(str(day), on_click=set_days_stock_chart, args=(day,))

# 表示する株価のコードと銘柄名を読み込む
with open("stocks.yaml", "r", encoding="utf-8") as f:
    stocks = yaml.safe_load(f)
stock_codes = list(stocks.keys())
stock_names = list(stocks.values())

# 株価を取得する
end = dt.date.today()
start = end - dt.timedelta(days=days[-1])  # 表示可能な最長期間前までデータを取得する
df_stock = pd.concat([get_stock(code, start, end) for code in stock_codes], axis=0)

# 表示期間を設定してチャートを表示する
start_fig = end - dt.timedelta(days=st.session_state.days_stock_chart)
fig = create_stock_charts(df_stock, stocks, start_fig, ncol=2)
fig.update_layout(height=800, showlegend=False)
st.plotly_chart(fig)
