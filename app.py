import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# import visualizations
from visualizations.rain import price_when_rains, amount_rides_in_rain
from visualizations.rides import top_rides, share_rides
from visualizations.surge import surge_multiplier_bar
from visualizations.price import mean_price_service

app = dash.Dash(__name__, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"])

# loading in both dataframes 
df_1 = pd.read_csv("data/dataframe1.csv")
df_2 = pd.read_csv("data/dataframe2.csv")

# appending df1 and df2 to create out final dataframe
df = df_1.append(df_2)

# spliting into datafrtames that would be used for our figures
mean_rain = df['source_rain'].mean()
cond_raining = df['source_rain'] >= mean_rain
df_rain = df[cond_raining] 

df_uber = df[df['cab_type'] == "Uber"]
df_lyft = df[df['cab_type'] == "Lyft"]

# question 1

fig = price_when_rains(df_rain)

# question 2

fig_question_2 = amount_rides_in_rain(df_rain)

# question 6

fig_question_6 = top_rides(df_uber, df_lyft)

# Question 7

fig_question_7 = share_rides(df_uber, df_lyft)

# surge multipler vis
surgeBar = surge_multiplier_bar(df_lyft)

# mean price at distance for each service
mean_uber = mean_price_service(df_uber)
mean_lyft = mean_price_service(df_lyft)

app.layout = html.Div(children=[
    html.H1("Uber vs Lyft"),
    html.Div(children=[
        html.H3('''
            Top five Rides for Uber and Lyft
        '''),
        html.P('''
            Looking at the top 5 rides for uber and Lyft
        '''),
    ], className="mt-5 mr-5 container"),

    html.Div(children=[
        dcc.Graph(
            id='question-6',
            figure=fig_question_6
        ),
    ], className="container"),

    html.Div(children=[
        html.H3('''
            Average Price vs Distance
        '''),
        html.P('''
            Took the average price for each distance
        '''),
    ], className="mt-5 mr-5 container"),

    html.Div(children=[
        dcc.Graph(
            id='uber-mean',
            figure=mean_uber
        ),
        dcc.Graph(
            id='lyft-mean',
            figure=mean_lyft
        ),
    ], className="row justify-content-center"),

    html.Div(children=[
        html.H3('''
            Rides on a rainy Day
        '''),
        html.P('''
            Taking a look of the rides on a rainy day. We only showing rides that
            rained more than the mean in our data. The rain is measured in inches.
        '''),
    ], className="mt-5 container"),

    html.Div(children=[
        dcc.Graph(
            id='question-1',
            figure=fig
        ),
        dcc.Graph(
            id='question-2',
            figure=fig_question_2
        ),
    ], className="row justify-content-center"),


    html.Div(children=[
        html.H3('''
            Shared vs NonShared
        '''),
    ], className="mt-5 container"),


    html.Div(children=[
        dcc.Graph(
            id='question-7',
            figure=fig_question_7
        ), 
    ], className="row justify-content-center"),


    html.Div(children=[
        html.H3('''
            Surge multiplier(Lyft)
        '''),
        html.P('''
            Here we are showing the surge multipler to see what day has the highest multipler.
        ''')
    ], className="mt-5 container"),

    html.Div(children=[
        dcc.Graph(
            id='surgeBar',
            figure=surgeBar
        ),
    ], className="row justify-content-center"), 
], className="container")

if __name__ == '__main__':
    app.run_server(debug=True)