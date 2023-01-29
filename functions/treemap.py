from dash import html, dcc
import plotly.express as px
from functions.config import count_words
import plotly.graph_objects as go


class TreeMap(html.Div):

    def __init__(self, name, df):
        self.html_id = name
        self.df = df
        self.clear = df

        super().__init__(
            className="graph_card",
            style={'backgroundColor': "#191a1a"},
            children=[
                dcc.Graph(id=self.html_id)
            ]
        )

    def update(self, data):

        df = count_words(data, 30)



        #sort by descending order
        df.sort_values(by='count',inplace=True, ascending=False)
        
        fig = px.treemap(
            df,
            path=[px.Constant("<br>"), 'word'],
            values='count',
            color='count',
            color_continuous_scale= 'matter',
            custom_data=['count', 'word'],
            hover_name='word',
            labels={'count': 'Count'}

        )

        nl = '\n'

        fig.update_layout(
            title=nl + "Commonly used words within the chosen area:" + nl,
            title_x=0.5,
            title_y=0.90,
            title_font_color = '#bfbbbb',
            hoverlabel=dict(
                    font_size=12,
                    font_family="Calibri"
                ),
            template="plotly_white",
            paper_bgcolor="#191a1a",
            height=300,
            font_color='#bfbbbb'

            # width=1000
        )

        fig.add_annotation(
            text='Select an Area on the Mapbox or Click on a Word to Filter Listings',
            font={
                'color': '#bfbbbb',
                'size': 10
            },
            y=-0.15,
            showarrow=False
        )

        fig.update_traces(
            hovertemplate="<br>".join([
                'Word: <b>%{customdata[1]}</b>',
                "Times word has appeared: %{customdata[0]}"
            ])
        )

        return fig

