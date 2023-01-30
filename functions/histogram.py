from dash import dcc, html
import plotly.express as px

#class for Histogram figure
class Histogram(html.Div):

    #initialise the figure properties and assign dataframe
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

    # Update function that will be called from callback functions
    # Params:
    #   NTA: registered neighbourhood
    #   dropdown_choice: type of visualisation that has been chosen by the user
    #   map_dropdown: Input from the other visualisation
    def update(self, NTA, dropdown_choice, map_dropdown):

        #NTA is not None when a neighbourhood/borough has been chosen on the other visualisation
        if NTA is not None:
            data = self.df.copy()

            #filter data according to the decision by the user
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
            #update the histogram
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

        else: #if the NTA is none the neighbourhood or the borough has not been chosen therefore a text will be displayed
              #asking the user too choose a neighbourhood/borough

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
                            "text": f"Click on the Map to Select Neighbourhoods/Boroughs",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {
                                "size": 15,
                                'color': '#bfbbbb'
                            },
                        }
                    ],
                }
            }
