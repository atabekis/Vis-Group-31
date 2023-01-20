from dash import html, dcc
import plotly.express as px
from functions.config import count_words


class TreeMap(html.Div):

    def __init__(self, name, df):
        self.html_id = name
        self.df = df

        super().__init__(
            className="graph_card",
            style={'backgroundColor': "#323130"},
            children=[
                dcc.Graph(id=self.html_id)
            ]
        )

    def update(self, data):
        bin_count = 30

        df = count_words(data, 500)[:bin_count]
        
        

        fig = px.treemap(
            df,
            path=[px.Constant("<br>"), 'word'],
            values='count',
            color='count',
            color_continuous_scale= px.colors.sequential.Sunsetdark,
        )

        nl = '\n'

        fig.update_layout(
            title=nl + "Commonly used words within the chosen area:" + nl,
            title_x=0.5,
            title_y=0.90,
            title_font_color = 'white',
            hoverlabel=dict(
                    font_size=12,
                    font_family="Calibri"
                ),
            template="plotly_white",
            paper_bgcolor="#444444",
            height=300,
            # width=1000
        )

        # fig.add_annotation(
        #     text=(
        #         "<b>Data Source: </b>" +
        #         'Haspelmath, Martin & Tadmor, Uri (eds.) 2009. ' +
        #         'World Loanword Database. ' +
        #         '<br>' +
        #         'Leipzig: Max Planck Institute for Evolutionary Anthropology. ' +
        #         '<br>' +
        #         '(Available online at http://wold.clld.org, Accessed on 2022-03-31.) '
        #     ),
        #     xref="paper", yref="paper",
        #     x=0.01, y=-0.13, showarrow=False,
        #     font=dict(
        #         family="Calibri",
        #         size=11,
        #         color="white"
        #     ),
        #     opacity=0.5,
        #     align="left"
        # )

        return fig

    # fig.update(layout_coloraxis_showscale=False)
    # fig.data[0].customdata[-1][0] = 650
    # fig.data[0].customdata[-1][1] = "N/A"
    # fig.data[0].marker.colors[-1] = np.NaN
    # fig.show()

