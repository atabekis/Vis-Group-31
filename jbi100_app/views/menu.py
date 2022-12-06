from dash import dcc, html

import jbi100_app.config as config

neighbourhood_group = config.get_neighbourhood_groups()

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
            html.Label("Neighbourhood Groups"),
            dcc.Dropdown(
                id="select-neighbourhood-group",
                options=[{"label": i, "value": i} for i in neighbourhood_group],
                value=neighbourhood_group[0],
            ),
            html.Br(),
            html.Label("Neighbourhoods"),
            dcc.Dropdown(
                id="select-neighbourhood",
                options=[{"label": i, "value": i} for i in neighbourhood_group],
                value=neighbourhood_group[0],
            ),
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
