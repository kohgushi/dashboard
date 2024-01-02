import datetime as dt
import pandas_datareader.data as web
import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
from pandas import DataFrame
from plotly.graph_objs._figure import Figure


@st.cache_data
def get_stock(ticker_symbol: int, start: str = "2022-01-01", end=None) -> DataFrame:
    ticker_symbol_dr = f"{ticker_symbol}.JP"

    # 集計終了期間が決められていない場合は最新日付まで取得する
    if end is None:
        end = dt.date.today()

    # データ取得
    df = web.DataReader(ticker_symbol_dr, data_source="stooq", start=start, end=end)

    # 列名修正
    df.columns = [col.lower() for col in df.columns.tolist()]

    # インデックスにコードを追加
    df.set_index([[ticker_symbol] * len(df), df.index], inplace=True)
    df.index.names = ["code", "date"]

    return df.sort_index()


def create_stock_chart(df: DataFrame, code: int, start: dt.date) -> Figure:
    df_single = df.loc[code].query("date>=@start").copy()
    df_single["ma7"] = df_single["close"].rolling(window=7).mean()
    return px.line(df_single, x=df_single.index, y=["close", "ma7"])


def create_stock_charts(
    df: DataFrame,
    cd2nm: dict,
    start: dt.date,
    ncol: int = 2,
) -> Figure:
    codes = list(cd2nm.keys())
    names = list(cd2nm.values())
    sp_titles = [f"{code}_{name}" for (code, name) in zip(codes, names)]
    nrow = len(codes) // ncol + 1
    main_fig = make_subplots(
        nrow,
        ncol,
        subplot_titles=sp_titles,
    )

    figures = [create_stock_chart(df, code, start) for code in codes]
    # 各トレースを適切なサブプロットに追加
    for i, figure in enumerate(figures):
        row = (i // ncol) + 1  # 行インデックスを計算
        col = (i % ncol) + 1  # 列インデックスを計算
        for trace in figure.data:
            main_fig.add_trace(trace, row=row, col=col)
    return main_fig
