import json

import plotly.express as px
from dash import html, dcc


class Choropleth(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="graph_card",
            style={'backgroundColor': "#323130"},
            children=[
                dcc.Graph(id=self.html_id)
            ]
        )

    def update(self):
        data = self.df.copy()
        # filter data on chosen groups

        with open('data/neighbourhoods.geojson') as f:
            neighbourhoods = json.load(f)

        # filter data according to the given price range


        token = "pk.eyJ1IjoibHVjdG9ydGlrZSIsImEiOiJjbGJnZHJncDYwZmNkM29zMmN6ZDFweXVhIn0.f9rwUtWIeGiwuJTPKzuMUA"

        # draw the figure
        self.fig = px.choropleth_mapbox(data, geojson=neighbourhoods, locations='NTA', color='price',
                                        featureidkey='properties.ntaname',
                                        color_continuous_scale="Viridis",
                                        range_color=(0, 1200),
                                        mapbox_style="carto-positron",
                                        zoom=10, center={"lat": 40.73963, "lon": -73.98166},
                                        opacity=0.5,
                                        labels={'price': 'Average price'}
                                        )

        self.fig.update_layout(mapbox_accesstoken=token,
                               mapbox_style="dark"
                               )
        self.fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="#323130",
            # plot_bgcolor="#323130"
        )

        return self.fig
