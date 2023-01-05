from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

class Mapboxplot(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="graph_card",
            style={'backgroundColor':"#323130"},
            children=[
                dcc.Graph(id=self.html_id)
            ]
        )

    def update(self, neighbourhood_group, neighbourhood, price_range, inst_bookable, service_fee_range): #, selected_data):
        data = self.df.copy()

        #filter data on chosen groups
        if neighbourhood_group != 'All':
            data = data.loc[data['neighbourhood_group'] == neighbourhood_group]
        
        if neighbourhood != 'All':
            data = data.loc[data['neighbourhood'] == neighbourhood]
        
        #filter data according to the given price range
        min_price_mask = data["price"] >= price_range[0]
        max_price_mask = data["price"] <= price_range[1]
        data = data[min_price_mask & max_price_mask]

        #filtler data according to the fiven service fee range
        min_service_mask = data["service_fee"] >= service_fee_range[0]
        max_service_mask = data["service_fee"] <= service_fee_range[1]
        data = data[min_service_mask & max_service_mask]

        #filter for instant bookability
        data = data[data["instant_bookable"] == inst_bookable]

        token = "pk.eyJ1IjoibHVjdG9ydGlrZSIsImEiOiJjbGJnZHJncDYwZmNkM29zMmN6ZDFweXVhIn0.f9rwUtWIeGiwuJTPKzuMUA"
        
        #draw the figure
        self.fig = px.scatter_mapbox(
            data,
            lat="lat", 
            lon="long", 
            hover_name="name", 
            hover_data=["room_type", "price"],
            color = "price", 
            color_continuous_scale=px.colors.sequential.Brwnyl, 
            zoom=10, 
            height=500,
        )
        
        self.fig.update_layout(mapbox_accesstoken = token, 
                                mapbox_style="dark"
        )
        self.fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor="#323130",
            #plot_bgcolor="#323130"
        )

        

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