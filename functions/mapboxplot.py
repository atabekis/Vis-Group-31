from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go


class Mapboxplot(html.Div):
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


    def update(self, data): 

        token = "pk.eyJ1IjoibHVjdG9ydGlrZSIsImEiOiJjbGJnZHJncDYwZmNkM29zMmN6ZDFweXVhIn0.f9rwUtWIeGiwuJTPKzuMUA"

        self.df = data

        # draw the figure
        self.fig = px.scatter_mapbox(
            self.df,
            lat="lat",
            lon="long",
            hover_name="name",
            # hover_data=["room_type", "price"],
            color='price',
            color_continuous_scale='matter',
            opacity=0.8,
            range_color=(0, 1200),
            #zoom=10,
            height=500,
            labels={'price': 'Price'},
            custom_data=['name']
        )

        lat_range = max(self.df['lat']) - min(self.df['lat'])
        lon_range = max(self.df['long']) - min(self.df['long'])
        
        zoom_level = 10
        zoom_scaler = (1/(lat_range + lon_range))

        if zoom_scaler > 5:
            zoom_level = 14
        elif zoom_scaler > 2:
            zoom_level = 12 

        self.fig.update_layout(
            mapbox_accesstoken=token,
            mapbox_style="dark",
            font_color='#bfbbbb',
            mapbox_zoom=zoom_level,
            mapbox_center={"lat": self.df['lat'].mean(), "lon": self.df['long'].mean()},
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="#191a1a",
        )

        self.fig.update_traces(
            hovertemplate="<br>".join([
                '<b>%{customdata[0]}</b>',
            ])
        )

        return self.fig
