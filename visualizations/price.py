import pandas as pd
import plotly.express as px

def mean_price_service(df, uber='UberPool', lyft='Shared'):
    cond_uber_service = df['name'] == uber
    cond_lyft_service = df['name'] == lyft
    df = df[cond_uber_service | cond_lyft_service]
    df = df.groupby(['name', 'distance', 'cab_type'])['price'].mean().reset_index()
    fig = px.line(df, x='distance', y='price', color='cab_type', color_discrete_map={'Lyft': '#FF00BF','Uber':'#000000'},
    height=650)
    fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
    },font_color="#FFFFFF")
    return fig