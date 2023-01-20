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
            color_continuous_scale=px.colors.sequential.Brwnyl,
            range_color=(0, 1200),
            #zoom=10,
            height=500,
            # labels={'price': 'Price'}
        )

        self.fig.update_layout(mapbox_accesstoken=token,
                               mapbox_style="dark"
                               )
        self.fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="#323130",
            # plot_bgcolor="#323130"
        )
        # self.fig.update_traces(
        #     hovertemplate=None,
        #     hoverinfo = 'skip')

        # highlight points chosen in other graph(s)
        # if selected_data is None:
        #     selected_index = data.index #shows all
        # else:
        #     selected_index = [ #show only selected indices
        #         x.get('pointIndex', None)
        #         for x in selected_data['points']
        #     ]

        # self.fig.data[0].update(
        #     selectedpoints = selected_index,

        #     # color of selected points
        #     selected=dict(marker=dict(color='BLUE')),

        #     # color of unselected pts
        #     unselected=dict(marker=dict(color='rgb(200,200,200)', opacity=0.9))
        # )
        return self.fig
