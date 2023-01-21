from dash import dcc, html
import plotly.express as px


class Histogram(html.Div):
    def __init__(self, name, df):
        self.fig = None
        self.html_id = name.lower().replace(" ", "-")
        self.df = df

        super().__init__(
            className="graph_card",
            style={'backgroundColor': "#191a1a"},
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

            # Histogram:
            self.fig = px.histogram(
                data,
                x=dropdown_choice,
                nbins=50,
                color_discrete_sequence=['#f3204f'],
                labels={'count': 'Count', 'price': 'Price', 'service_fee': 'Service Fee',
                        'reviews_per_month': 'Number of Monthly Reviews'},
            )

            self.fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                paper_bgcolor="#191a1a",
                plot_bgcolor="#191a1a",
                font_color="white",
                yaxis={
                    'showgrid': False
                },
                bargap=0.1,
                yaxis_title='Count',

            )

            return self.fig

        else:

            return {
                "layout": {
                    'paper_bgcolor': "#191a1a",
                    'plot_bgcolor': "#191a1a",

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
