import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


app = dash.Dash(__name__, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


# loading in both dataframes 
df_1 = pd.read_csv("data/dataframe1.csv")
df_2 = pd.read_csv("data/dataframe2.csv")

# appending df1 and df2 to create out final dataframe
df = df_1.append(df_2)

# spliting into datafrtames that would be used for our figures
cond_raining = df['source_rain'] > 0

df_uber = df[df['cab_type'] == "Uber"]
df_lyft = df[df['cab_type'] == "Lyft"]
df_rain = df[cond_raining] 

# question 1
cond_distance = df_rain['distance'].isin([0.5, 1, 1.5, 2, 2.5, 3])
df_data = df_rain[cond_distance]
cond_uber = df_data['name'] == 'UberPool' 
cond_lyft = df_data['name'] == 'Shared' 

df_data = df_data[cond_uber | cond_lyft]
df_data = df_data.sort_values(by='distance')

fig = px.scatter(df_data, x="source_rain", y="price", color="cab_type", hover_data=['distance', 'name'], 
                 animation_frame = 'distance', color_discrete_map={'Lyft': '#FF00BF','Uber':'#000000'})
fig["layout"].pop("updatemenus")


# question 2

df_rides_rain = df_rain.groupby(['cab_type', 'date']).size().reset_index()
df_rides_rain = df_rides_rain.rename(columns={0: "amount"})

fig_question_2 = px.bar(df_rides_rain, 
                 x='cab_type', y='amount', 
                 color = 'cab_type',
                 color_discrete_map={'Lyft': '#FF00BF','Uber':'#000000'},
                 width = 500, height = 500,
                 animation_frame = 'date'
                )
fig_question_2["layout"].pop("updatemenus")


# question 6
uber_source_dest_df = df_uber.groupby(['source', 'destination', 'date', 'cab_type']).size().reset_index()
uber_source_dest_df.columns = ["source", "destination", "date",'cab_type',"count"]
uber_source_dest_df.sort_values(['date', 'count'], inplace=True, ascending=False)


dates = ['2018-11-25','2018-11-26','2018-11-27','2018-11-28','2018-11-29',
        '2018-11-30','2018-12-01','2018-12-02','2018-12-03','2018-12-04',
        '2018-12-05','2018-12-06','2018-12-07','2018-12-08','2018-12-09',
        '2018-12-10','2018-12-11','2018-12-12','2018-12-13','2018-12-14',
         '2018-12-15','2018-12-16','2018-12-17','2018-12-18']
uber_top5 = pd.DataFrame()
for date in dates:
    temp = uber_source_dest_df[uber_source_dest_df['date'] == date]
    temp = temp.sort_values('count', ascending = False)
    uber_top5 = uber_top5.append(temp.head(5))


lyft_source_dest_df = df_lyft.groupby(['source', 'destination', 'date', 'cab_type']).size().reset_index()
lyft_source_dest_df.columns = ["source", "destination","date","cab_type","count"]
lyft_source_dest_df.sort_values(["count", "date"], inplace=True, ascending=False)



dates = ['2018-11-25','2018-11-26','2018-11-27','2018-11-28','2018-11-29',
        '2018-11-30','2018-12-01','2018-12-02','2018-12-03','2018-12-04',
        '2018-12-05','2018-12-06','2018-12-07','2018-12-08','2018-12-09',
        '2018-12-10','2018-12-11','2018-12-12','2018-12-13','2018-12-14',
         '2018-12-15','2018-12-16','2018-12-17','2018-12-18']
lyft_top5 = pd.DataFrame()
for date in dates:
    temp = lyft_source_dest_df[lyft_source_dest_df['date'] == date]
    temp = temp.sort_values('count', ascending = False)
    lyft_top5 = lyft_top5.append(temp.head(5))


top5 = uber_top5.append(lyft_top5)


fig_question_6 = px.scatter(top5, 
                 x='source', y='destination', 
                 hover_data = ['count'],
                 color = 'cab_type',
                 color_discrete_map={'Lyft': '#FF00BF','Uber':'#000000'},
                 width = 600, height = 400,
                animation_frame = 'date')
fig_question_6["layout"].pop("updatemenus")


# Question 7

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


fig_question_7 = px.bar(is_shared_df,
                 x='cab_type', y='count',
                 color = 'is_shared',
                 hover_data = ['name'],
                 color_discrete_map={'Yes': '#FF8C00','No':'#A52A2A'},
                 width = 500, height =600,
                 animation_frame = 'date'
                )
fig_question_7["layout"].pop("updatemenus")




app.layout = html.Div(children=[
    html.H1("Uber vs Lyft"),

    html.Div(children=[
        html.Div(children=[
            dcc.Graph(
                id='question-1',
                figure=fig
            )
        ], className="col"),

        html.Div(children=[
            dcc.Graph(
                id='question-2',
                figure=fig_question_2
            ),
        ], className="col"),
    ], className="row"),

    dcc.Graph(
        id='question-6',
        figure=fig_question_6
    ), 

    dcc.Graph(
        id='question-7',
        figure=fig_question_7
    ), 
], className="mt-5")

if __name__ == '__main__':
    app.run_server(debug=True)