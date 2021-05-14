import pandas as pd
import plotly.express as px

def surge_multiplier_bar(df_lyft):
    surge_df = df_lyft[df_lyft["surge_multiplier"] >1]
    high_surge = pd.DataFrame(surge_df.groupby(['weekday', "surge_multiplier"]).size().reset_index())

    high_surge.columns = ["Weekday", "Surge", "Count"]

    high_surge["Day_of_Week"] = high_surge['Weekday'].map({'Monday': 1,
                                                       'Tuesday': 2,
                                                       'Wednesday': 3,
                                                       'Thursday': 4,
                                                       'Friday': 5,
                                                       'Saturday': 6,
                                                       'Sunday':7})
    high_surge.sort_values(by = 'Day_of_Week', inplace = True)

    high_surge['Surge'] = high_surge['Surge'].astype(str)
    fig = px.bar(high_surge, 
                    x='Weekday', y='Count', 
                    color = 'Surge',
                    color_discrete_sequence= px.colors.qualitative.Vivid,

                    barmode= 'group'
                    )

    return fig
