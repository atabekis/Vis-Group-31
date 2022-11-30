from dash import dcc, html
from ..config import neighbourhood_group


def generate_description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Group 31 Visualisations"),
            html.Div(
                id="intro",
                children="Settings:",
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Color scatterplot 1"),
            dcc.Dropdown(
                id="select-neighbourhood-group",
                options=[{"label": i, "value": i} for i in neighbourhood_group],
                value=neighbourhood_group[0],
            ),
            html.Br(),
            html.Label("Color scatterplot 2"),
            dcc.Dropdown(
                id="select-color-scatter-2",
                options=[{"label": i, "value": i} for i in neighbourhood_group],
                value=neighbourhood_group[0],
            ),
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
