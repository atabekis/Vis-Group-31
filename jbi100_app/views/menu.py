from dash import dcc, html
import numpy as np

import jbi100_app.config as config

neighbourhood_group = config.get_neighbourhood_groups()
neighbourhood = config.get_neighbourhood()
min_price, max_price = config.get_price_min_max()
instant_bookability = config.get_inst_bookable()

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


def generate_control_card(neighbourhood_name):
    """
    :return: A Div containing controls for graphs.
    """
    x = np.where(neighbourhood_group == neighbourhood_name)[0][0]
    return html.Div(
        id="control-card",
        children=[
            html.Label("Neighbourhood Groups"),
            dcc.Dropdown(
                id="select-neighbourhood-group",
                options=[{"label": i, "value": i} for i in neighbourhood_group],
                value=neighbourhood_group[np.where(neighbourhood_group == neighbourhood_name)[0][0]],
            ),
            html.Br(),
            html.Label("Neighbourhoods"),
            dcc.Dropdown(
                id="select-neighbourhood",
                options=[{"label": i, "value": i} for i in neighbourhood[neighbourhood_name]],
                value=neighbourhood[neighbourhood_name][0],
            ),
            html.Br(),
            html.Label("Price Range"),
            dcc.RangeSlider(
                min=min_price,
                max=max_price,
                value=[min_price,max_price],
                allowCross=False,
                id='price-range-slider',
                marks={
                    min_price:{'label': str(min_price)},
                    max_price:{'label': str(max_price)}
                },
                tooltip={"placement":"bottom", "always_visible":True}
            ),
            html.Br(),
            html.Label("Instantly Bookable"),
            dcc.Dropdown(
                id='instant-bookable',
                options=[{"label": i, "value": i} for i in instant_bookability],
                value=instant_bookability[0]
            )

        ], style={"textAlign": "float-left"}
    )


def make_menu_layout(neighbourhood):
    return [generate_description_card(), generate_control_card(neighbourhood)]
