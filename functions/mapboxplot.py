from dash import dcc, html
import plotly.express as px

#Class for scatter mapboxplot
class Mapboxplot(html.Div):
    #intialisation function
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

    #update function that will be called by callback function
    #params:
    #   Data: data passed by the callback function depending on the state of the previous figure
    def update(self, data): 

        #token for the dark map
        token = "pk.eyJ1IjoibHVjdG9ydGlrZSIsImEiOiJjbGJnZHJncDYwZmNkM29zMmN6ZDFweXVhIn0.f9rwUtWIeGiwuJTPKzuMUA"

        self.df = data

        # draw the figure with data parameters
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

        #calculate the amount of zoom depending on the lateral and longitudinal ranges 
        #base zoom level
        zoom_level = 10
        try:
            lat_range = max(self.df['lat']) - min(self.df['lat'])
            lon_range = max(self.df['long']) - min(self.df['long'])
            
            #calculate zoom
            zoom_scaler = (1/(lat_range + lon_range))

            if zoom_scaler > 5:
                zoom_level = 14
            elif zoom_scaler > 2:
                zoom_level = 12 
        except:
            print("no data available")

        #update layout with parameters
        self.fig.update_layout(
            mapbox_accesstoken=token,
            mapbox_style="dark",
            font_color='#bfbbbb',
            mapbox_zoom=zoom_level,
            mapbox_center={"lat": self.df['lat'].mean(), "lon": self.df['long'].mean()},
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="#191a1a",
        )

        #update the traces
        self.fig.update_traces(
            hovertemplate="<br>".join([
                '<b>%{customdata[0]}</b>',
            ])
        )

        return self.fig
