import json
import plotly.express as px
from dash import html, dcc

#Choropleth graph class file
class Choropleth(html.Div):

    #class initialiser
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

    #Update function that gets called in the app callbacks
    #Params:
    # map_type: ("neighbourhoods" or "boroughs") defines what kind of graph will be displayed
    def update(self, map_type):
        data = self.df.copy()
        # filter data on chosen groups

        if map_type == 'neighbourhoods':
            
            with open('Data/neighbourhoods.geojson') as f:
                file = json.load(f)

            feature = 'properties.ntaname'
            location = 'NTA'
        elif map_type == 'boroughs':

            with open('Data/boroughs.geojson') as f:
                file = json.load(f)

            feature = 'properties.boro_name'
            location = 'neighbourhood_group'

        token = "pk.eyJ1IjoibHVjdG9ydGlrZSIsImEiOiJjbGJnZHJncDYwZmNkM29zMmN6ZDFweXVhIn0.f9rwUtWIeGiwuJTPKzuMUA"

        # draw the figure
        self.fig = px.choropleth_mapbox(data, geojson=file, locations=location, color='price',
                                        featureidkey=feature,
                                        color_continuous_scale="matter",
                                        range_color=(0, 1200),
                                        mapbox_style="carto-positron",
                                        zoom=10, center={"lat": 40.73963, "lon": -73.98166},
                                        opacity=0.8,
                                        labels={'price': 'Average price'},
                                        custom_data=['NTA', 'price']
                                        )

        #update the figure with style parameters
        self.fig.update_layout(
            mapbox_accesstoken=token,
            mapbox_style="dark",
            font_color="#bfbbbb"
        )

        self.fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="#191a1a"
        )

        #update the traces on the figure
        self.fig.update_traces(
            hovertemplate="<br>".join([
                'Name: <b>%{customdata[0]}</b>',
                "Average Price: $%{customdata[1]}"
            ])
        )

        return self.fig
