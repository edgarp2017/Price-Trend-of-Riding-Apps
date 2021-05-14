import pandas as pd
import plotly.express as px

def mean_price_service(df):
    df = df.groupby(['name', 'distance'])['price'].mean().reset_index()
    fig = px.line(df, x='distance', y='price', color='name')

    return fig