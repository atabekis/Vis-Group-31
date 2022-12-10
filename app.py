from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.mapboxplot import Mapboxplot

from dash import html, dcc
from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd
import numpy as np
import os


def clean_csv():

    df1 = pd.read_csv('Data/airbnb_open_data.csv', low_memory=False)

    df1 = df1.fillna(0)
    df1.rename(columns=lambda x: (x.replace(' ', '_')).lower(), inplace=True)

    df1['price'] = (df1['price'].replace({'\$': '', ',': ''}, regex=True)).astype(int)
    df1['service_fee'] = (df1['service_fee'].replace({'\$': '', ',': ''}, regex=True)).astype(int)
    df1 = df1.drop(['country', 'country_code'], axis=1)
    df1['last_review'] = pd.to_datetime(df1.last_review)

    df1 = df1.astype({'minimum_nights': int, 'number_of_reviews': int, 'reviews_per_month': int,
                      'review_rate_number': int, 'availability_365': int, 'calculated_host_listings_count': int,
                      'construction_year': int})

    df1.to_csv('Data/airbnb_open_data_clean.csv')



if __name__ == '__main__':
    #clean data
    if not os.path.exists("Data/airbnb_open_data_clean.csv"):
        clean_csv()

    # import Data
    open_ABNB_data = pd.read_csv("Data/airbnb_open_data_clean.csv")


    map_boxplot = Mapboxplot("boxplot1", open_ABNB_data)

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=map_boxplot
            ),
        ],
    )

    #interactions
    @app.callback(
        Output(map_boxplot.html_id, "figure"), [
        Input("select-neighbourhood-group", "value"),
        Input("select-neighbourhood", "value"),
        Input('price-range-slider', "value"),
        Input('instant-bookable', "value")
    ])
    def update_mapboxplot(neighbourhood_group, neighbourhood, price_range, inst_bookable):
        return map_boxplot.update(neighbourhood_group, neighbourhood, price_range, inst_bookable)


    app.run_server(debug=False, dev_tools_ui=False)