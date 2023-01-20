from dash import dcc, html
import plotly.express as px
from plotly.graph_objects import Layout
import plotly.graph_objects as go


class Barchart(html.Div):
    def __init__(self, name, df):
        self.fig = None
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="graph_card",
            style={'backgroundColor': "#323130"},
            children=[
                dcc.Graph(id=self.html_id)
            ]
        )

    def update(self, NTA, dropdown_choice, map_dropdown):

        if NTA is not None:
            data = self.df.copy()

            if map_dropdown == 'boroughs':
                data = data[data['neighbourhood_group'] == NTA]
            else:
                data = data[data['NTA'] == NTA]


            ### histogram:
            self.fig = px.histogram(
                data,
                #y='price',
                x=dropdown_choice,
                nbins=50,
                # color='red',
                color_discrete_sequence=['#f3204f']
            )

            self.fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                paper_bgcolor="#323130",
                plot_bgcolor="#323130",
                font_color="white",
                yaxis={
                    'showgrid': False
                    },
                bargap=0.1
            )
            ### original barchart:
            # self.fig = px.bar(
            #     data,
            #     x='id',
            #     y=dropdown_choice)

            # self.fig.update_layout(
            #     margin={"r": 0, "t": 0, "l": 0, "b": 0},
            #     paper_bgcolor="#323130",
            #     plot_bgcolor="#323130",
            #     font_color="white",
            #     xaxis={
            #         'showgrid': False,
            #     },
            #     yaxis={
            #         'showgrid': False
            #     }

            # )

            return self.fig

        else:

            return {
                "layout": {
                    'paper_bgcolor': "#323130",
                    'plot_bgcolor' : "#323130",

                    "xaxis": {
                        "visible": False
                    },
                    "yaxis": {
                        "visible": False
                    },
                    "annotations": [
                        {
                            "text": "Click on an area or i'll beat your ass",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {
                                "size": 20,
                                'color': '#bfbbbb'
                            },

                        }
                    ],
                }
            }