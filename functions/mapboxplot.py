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

        self.fig.update_layout(mapbox_accesstoken=token,
                               mapbox_style="dark",
                               font_color='#bfbbbb'
                               )
        self.fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="#191a1a"
        )

        self.fig.update_traces(
            hovertemplate="<br>".join([
                '<b>%{customdata[0]}</b>',
            ])
        )

        return self.fig
