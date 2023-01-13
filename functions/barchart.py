from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go


class Barchart(html.Div):
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

    def update(self, NTA, dropdown_choice): 
        #print(dropdown_choice)
        #print(NTA['points'][0]['location'])
        data = self.df.copy()
        data = data[data['NTA'] == NTA] 

        self.fig = px.bar(
            data,
            x = 'host_name',
            y = dropdown_choice
        ) 
        # yet to do some more bar chart layout after testing

        return self.fig


