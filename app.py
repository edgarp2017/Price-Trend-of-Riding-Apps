import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# import visualizations
from visualizations.rain import price_when_rains, amount_rides_in_rain
from visualizations.rides import top_rides, share_rides
from visualizations.surge import surge_multiplier_bar
from visualizations.price import mean_price_service

app = dash.Dash(__name__, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"])
app.title = 'Uber vs Lyft'
server = app.server

# loading in both dataframes 
df_1 = pd.read_csv("data/dataframe1.csv")
df_2 = pd.read_csv("data/dataframe2.csv")

# appending df1 and df2 to create out final dataframe
df = df_1.append(df_2)

mean_rain = df['source_rain'].mean()
cond_raining = df['source_rain'] >= mean_rain
df_rain = df[cond_raining] 

tabs_styles = {
    'height': '44px',
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': '#808080',
    'height': '50px',
    'color': '#FFFFF'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'padding': '6px'
}

input_box = {
    'background-color': '#C5C6D0',
}

graph_title = {
    'color': '#FBD428'
}

page_title = {
    'font-weight': 'bold'
}

app.layout = html.Div(children=[
    html.Div(children=[
        html.Strong("Uber vs Lyft", className="display-1 mt-5 text-warning", style=page_title),
    ], className="row justify-content-center bg-secondary pb-5"),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Uber vs Lyft - General Analysis', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Uber vs Lyft - Rain Analysis', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='More To Explore ...', value='tab-3', style=tab_style, selected_style=tab_selected_style),
    ]),
    html.Div(id='tabs-example-content')
])

@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        df_uber = df[df['cab_type'] == "Uber"]
        df_lyft = df[df['cab_type'] == "Lyft"]

        fig_question_6 = top_rides(df_uber, df_lyft)
        fig_question_7 = share_rides(df_uber, df_lyft)

        return html.Div([
    
            html.Div([
                html.Div(children=[
                    html.H3('''
                        Top five Rides for Uber and Lyft
                    ''', style=graph_title),
                    html.P('''
                        Looking at the top 5 rides for uber and Lyft
                    '''),
                    dcc.Graph(
                        id='question-6',
                        figure=fig_question_6
                    ),
                ], className="col-7 mt-5"),


                html.Div(children=[
                    html.Div(children=[
                        html.H3('''
                            Shared vs NonShared
                        ''', style=graph_title),
                    ], className="mt-5 container"),
                    dcc.Graph(
                        id='question-6',
                        figure=fig_question_7
                    ),
                ], className="col mt-5"),
            ], className="d-flex justify-content-between"),

            # center this graph
            html.Div([
               
                html.H3('''
                    Average Price for each distance
                ''', style=graph_title),
                html.P('''
                    Taking a look at all our rides we are averaging the price for each distance that we have on 
                    our dataset. 
                '''),
                html.P('''
                    Use the drop down menu to compare the different services that Uber and Lyft offer.
                '''),
                dcc.Dropdown(id='mean-dropdown', options=[
                    {'label': 'UberPool/Lyft Shared', 'value': 'Shared'},
                    {'label': 'UberX/Lyft', 'value': 'Regular'},
                    {'label': 'UberXL/Lyft XL', 'value': 'XL'},
                    {'label': 'Uber Black/Lyft Black', 'value': 'Black'},
                    {'label': 'Uber Black SUV/Lyft Black XL', 'value': 'Black XL'},
                    ],
                    value = 'Shared',
                    style=input_box,
                ),
                dcc.Graph(
                    id='price-mean',
                ),
            ], className="col-9 mt-5 justify-content-center")

        ],  className="bg-secondary text-white pb-5")

    elif tab == 'tab-2':

        return html.Div([
            html.Div(children=[
                html.H3('''
                    Select a Service
                ''', style=graph_title),
                dcc.Dropdown(id='dropdown', options=[
                    {'label': 'UberPool/Lyft Shared', 'value': 'Shared'},
                    {'label': 'UberX/Lyft', 'value': 'Regular'},
                    {'label': 'UberXL/Lyft XL', 'value': 'XL'},
                    {'label': 'Uber Black/Lyft Black', 'value': 'Black'},
                    {'label': 'Uber Black SUV/Lyft Black XL', 'value': 'Black XL'},
                    ],
                    value = 'Shared',
                    style=input_box
                ),
            ], className="pt-5 container"),
            html.Div(children=[
                html.H3('''
                    Rides on a rainy Day
                ''', style=graph_title),
                html.P('''
                    Taking a look of the rides on a rainy day. We only showing rides that
                    rained more than the mean in our data. The rain is measured in inches.
                '''),
                 
                dcc.Graph(
                    id='rain-scatter'
                ),

            ], className="mt-5 container"),

            html.Div(children=[
                html.H3('''
                    Rides on a rainy Day
                ''', style=graph_title),
                html.P('''
                    Taking a look of the rides on a rainy day. We only showing rides that
                    rained more than the mean in our data. The rain is measured in inches.
                '''),
                dcc.Graph(
                    id='question-2'
                ),

            ], className="mt-5 container"),
            
        ],  className="bg-secondary text-white pb-5")


    elif tab == "tab-3":
        df_lyft = df[df['cab_type'] == "Lyft"]
        surgeBar = surge_multiplier_bar(df_lyft)

        return html.Div([
            html.Div(children=[
                html.H3('''
                    Surge multiplier(Lyft)
                ''', style=graph_title),
                html.P('''
                    Here we are showing the surge multipler to see what day has the highest multipler.
                '''),
            ], className="pt-5 container"),
            html.Div(children=[
                dcc.Graph(
                    id='surgeBar',
                    figure=surgeBar
                ),
            ], className=" container"), 
             html.Div(children=[
                html.P('From what we can see here that the most common surge multipler for lyft is 1.25.'),
                html.P('This surge multiplier would most frequently be Monday.')
            ], className=" container"), 
        ],  className="bg-secondary text-white pb-5 custom-body")



@app.callback(Output('price-mean', 'figure'), 
              [Input('mean-dropdown', 'value')])
def mean_price_updater(value):
    if value == 'Shared':
        fig = mean_price_service(df, 'UberPool', 'Shared')
    elif value == 'XL':
        fig = mean_price_service(df, 'UberXL', 'Lyft XL')
    elif value == 'Black':
        fig = mean_price_service(df, 'Black', 'Lux Black')
    elif value == 'Black XL':
        fig = mean_price_service(df, 'Black SUV', 'Lux Black XL')
    elif value == 'Regular':
        fig = mean_price_service(df, 'UberX', 'Lyft')

    return fig


@app.callback(Output('rain-scatter', 'figure'), 
              [Input('dropdown', 'value')])
def rain_price_updater(value):

    if value == 'Shared':
        fig = price_when_rains(df_rain, 'UberPool', 'Shared')
    elif value == 'XL':
        fig = price_when_rains(df_rain, 'UberXL', 'Lyft XL')
    elif value == 'Black':
        fig = price_when_rains(df_rain, 'Black', 'Lux Black')
    elif value == 'Black XL':
        fig = price_when_rains(df_rain, 'Black SUV', 'Lux Black XL')
    elif value == 'Regular':
        fig = price_when_rains(df_rain, 'UberX', 'Lyft')

    return fig


@app.callback(Output('question-2', 'figure'), 
              [Input('dropdown', 'value')])
def rain_ride_updater(value):
    if value == 'Shared':
        fig = amount_rides_in_rain(df_rain, 'UberPool', 'Shared')
    elif value == 'XL':
        fig = amount_rides_in_rain(df_rain, 'UberXL', 'Lyft XL')
    elif value == 'Black':
        fig = amount_rides_in_rain(df_rain, 'Black', 'Lux Black')
    elif value == 'Black XL':
        fig = amount_rides_in_rain(df_rain, 'Black SUV', 'Lux Black XL')
    elif value == 'Regular':
        fig = amount_rides_in_rain(df_rain, 'UberX', 'Lyft')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)