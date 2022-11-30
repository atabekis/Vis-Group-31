from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash import html
from dash import dcc
from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd
import numpy as np

from jbi100_app.config import neighbourhood_group

if __name__ == '__main__':
    # Create data
    open_ABNB_data = pd.read_csv("Data/airbnb_open_data.csv")

    neighbourhood_group = app.open_ABNB_data['neighbourhood group'].unique()

    mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"


    fig = px.scatter_mapbox(open_ABNB_data, lat="lat", lon="long", hover_name="NAME", hover_data=["room type", "price"],
                        color_discrete_sequence=["fuchsia"], zoom=10, height=500)
    fig.update_layout(mapbox_style="open-street-map")
    #fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(margin={"r":0,"t":0,"l":10,"b":50})


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
                children=[
                    dcc.Graph(
                        id='map',
                        figure=fig
                    )
                ],
            ),
        ],
    )


    app.run_server(debug=False, dev_tools_ui=False)