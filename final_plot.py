from matplotlib.pyplot import plot
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import dummy

def plot_data():
    df = pd.read_csv("bars.csv")
    tic_groups = df.groupby(by=['tic'],sort=False)
    
    tics = []
    figs = []
    for tic in tic_groups:
        df = tic[1]
        fig = go.Figure(data=[go.Candlestick(x=df['time'],
                            open=df['open'],high=df['high'],low=df['low'],close=df.close)])
        fig.update_layout(xaxis_rangeslider_visible=False)
        tics.append(tic[0])
        figs.append(fig)
    return tics,figs

tics,figs = plot_data()

for plots in zip(tics,figs):
    st.write(f'CandleSticks graph for {plots[0]}')
    st.plotly_chart(plots[1])
