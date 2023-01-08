from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

class Selectedplot(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        super().__init__(
            className="graph_card",
            style={'backgroundColor':"#323130"},
            children=[
                dcc.Graph(id=self.html_id)
            ]
        )

# Does not work at all rn 

    def update(self, selected_data):
        data = self.df.copy()
        self.fig = go.Figure()

        x_values = data[self.feature_x]
        y_values = data[self.feature_y]
        self.fig.add_trace(go.Scatter(
            x=x_values, 
            y=y_values,
            mode='markers',
            marker_color='rgb(200,200,200)'
        ))
        self.fig.update_traces(mode='markers', marker_size=10)
        self.fig.update_layout(
            yaxis_zeroline=False,
            xaxis_zeroline=False,
            dragmode='select'
        )
        self.fig.update_xaxes(fixedrange=True)
        self.fig.update_yaxes(fixedrange=True)

        return self.fig



