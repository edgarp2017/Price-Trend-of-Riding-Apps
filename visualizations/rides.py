import pandas as pd
import numpy as np
import plotly.express as px

def extract_top_five_rides(df):
    df = df.groupby(['source', 'destination', 'date', 'cab_type']).size().reset_index()
    df.columns = ["source", "destination", "date",'cab_type',"count"]
    df.sort_values(['date', 'count'], inplace=True, ascending=False)


    dates = ['2018-11-25','2018-11-26','2018-11-27','2018-11-28','2018-11-29',
            '2018-11-30','2018-12-01','2018-12-02','2018-12-03','2018-12-04',
            '2018-12-05','2018-12-06','2018-12-07','2018-12-08','2018-12-09',
            '2018-12-10','2018-12-11','2018-12-12','2018-12-13','2018-12-14',
            '2018-12-15','2018-12-16','2018-12-17','2018-12-18']
    
    top_5 = pd.DataFrame()

    for date in dates:
        temp = df[df['date'] == date]
        temp = temp.sort_values('count', ascending = False)
        top_5 = top_5.append(temp.head(5))

    return top_5

def top_rides(df_uber, df_lyft):
    top_uber = extract_top_five_rides(df_uber)
    top_lyft = extract_top_five_rides(df_lyft)

    top_five_rides = top_uber.append(top_lyft)

    fig = px.scatter(top_five_rides, 
                 x='source', y='destination', 
                 hover_data = ['count'],
                 color = 'cab_type',
                 color_discrete_map={'Lyft': '#FF00BF','Uber':'#000000'},
                animation_frame = 'date')
    fig["layout"].pop("updatemenus")
    fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
    },font_color="#FFFFFF")

    return fig


def share_rides(df_uber, df_lyft):
    uber_carname_df = df_uber.groupby(['name','cab_type', "date"]).size().reset_index()
    uber_carname_df.columns = ["name", "cab_type","date", "count"]
    uber_carname_df.sort_values("count", inplace = True, ascending = False)

    condition = uber_carname_df['name'] == "UberPool"
    uber_carname_df["is_shared"] = np.where(condition, "Yes", "No")

    lyft_carname_df = df_lyft.groupby(['name','cab_type', "date"]).size().reset_index()
    lyft_carname_df.columns = ["name", "cab_type","date", "count"]
    lyft_carname_df.sort_values(["date"], inplace = True, ascending = True)

    condition = lyft_carname_df['name'] == "Shared"
    lyft_carname_df["is_shared"] = np.where(condition, "Yes", "No")

    is_shared_df = uber_carname_df.append(lyft_carname_df)

    fig = px.bar(is_shared_df,
                 x='cab_type', y='count',
                 color = 'is_shared',
                 hover_data = ['name'],
                 color_discrete_map={'Yes': '#FF8C00','No':'#A52A2A'},
                 width = 500, height =600,
                 animation_frame = 'date'
                )
    fig["layout"].pop("updatemenus")
    fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
    },font_color="#FFFFFF")

    return fig