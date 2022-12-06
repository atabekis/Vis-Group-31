from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

class Mapboxplot(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ]
        )

    def update(self, neighbourhood_group, neighbourhood):#, selected_data):
        data = self.df.copy()

        #filter data on chosen groups
        if neighbourhood_group != 'All':
            data = data.loc[data['neighbourhood_group'] == neighbourhood_group]
        
        # if neighbourhood != 'All':
        #     data = data.loc[data['neighbourhood'] == neighbourhood]

        #draw the figure
        pxfig = px.scatter_mapbox(
            data,
            lat="lat", 
            lon="long", 
            hover_name="name", 
            hover_data=["room_type", "price"],
            color = "price", 
            color_continuous_scale=px.colors.cyclical.IceFire, 
            zoom=10, 
            height=500
        )
        self.fig = go.Figure(pxfig)
        # self.fig.update_traces()
        self.fig.update_layout(mapbox_style="open-street-map")
        #self.fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

       


        #highlight points chosen in other graph(s)
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