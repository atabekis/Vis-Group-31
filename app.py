from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash import html
from dash import dcc
from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd
import numpy as np



if __name__ == '__main__':
    # Create data
    open_ABNB_data = pd.read_csv("Data/airbnb_open_data.csv")

    df = px.data.iris()  #TODO: remove and replace with preprocessed data (Ata)

    # Dictionary of important locations in New York TODO; avoid plagiarism ;)
    list_of_locations = {
        "Madison Square Garden": {"lat": 40.7505, "lon": -73.9934},
        "Yankee Stadium": {"lat": 40.8296, "lon": -73.9262},
        "Empire State Building": {"lat": 40.7484, "lon": -73.9857},
        "New York Stock Exchange": {"lat": 40.7069, "lon": -74.0113},
        "JFK Airport": {"lat": 40.644987, "lon": -73.785607},
        "Grand Central Station": {"lat": 40.7527, "lon": -73.9772},
        "Times Square": {"lat": 40.7589, "lon": -73.9851},
        "Columbia University": {"lat": 40.8075, "lon": -73.9626},
        "United Nations HQ": {"lat": 40.7489, "lon": -73.9680},
    }

    fig = px.scatter_mapbox(open_ABNB_data, lat="lat", lon="long", hover_name="NAME", hover_data=["room type", "price"],
                        color_discrete_sequence=["fuchsia"], zoom=10, height=500)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":10,"b":50})
    # fig.show()

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