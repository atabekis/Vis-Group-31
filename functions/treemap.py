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

        df = count_words(data, 500)

        #sort by descending order
        df.sort_values(by='count',inplace=True, ascending=False)
        print(df)

        #take the first 30 values
        bin_count = 30
        if len(df) > 30:
            df = df[:bin_count]
        
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

        return fig

