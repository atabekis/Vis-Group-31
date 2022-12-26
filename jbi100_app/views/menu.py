from dash import dcc, html
import numpy as np

import jbi100_app.config as config

neighbourhood_group = config.get_neighbourhood_groups()
neighbourhood = config.get_neighbourhood()
min_price, max_price = config.get_price_min_max()
instant_bookability = config.get_inst_bookable()
min_service_fee, max_service_fee = config.get_service_fee()

def generate_description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Group 31 Visualisations"),
            html.Label(
                id="intro",
                children="Settings:",
                style={'color': "white"}
            ),
        ],
    )


def generate_control_card(neighbourhood_name):
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Neighbourhood Groups",style={'color': "white"}),
            dcc.Dropdown(
                style={"border": "0px solid black"},
                id="select-neighbourhood-group",
                options=[{"label": i, "value": i} for i in neighbourhood_group],
                value=neighbourhood_group[np.where(neighbourhood_group == neighbourhood_name)[0][0]],
            ),
            html.Br(),
            html.Label("Neighbourhoods",style={'color': "white"}),
            dcc.Dropdown(
                style={"border": "0px solid black"},
                id="select-neighbourhood",
                options=[{"label": i, "value": i} for i in neighbourhood[neighbourhood_name]],
                value=neighbourhood[neighbourhood_name][0],
            ),
            html.Br(),
            html.Label("Price Range",style={'color': "white"}),
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
            html.Label("Service Fee Range",style={'color': "white"}),
            dcc.RangeSlider(
                min=min_service_fee,
                max=max_service_fee,
                value=[min_service_fee,max_service_fee],
                allowCross=False,
                id='service-fee-range-slider',
                marks={
                    min_price:{'label': str(min_service_fee)},
                    max_price:{'label': str(max_service_fee)}
                },
                tooltip={"placement":"bottom", "always_visible":True}
            ),            
            html.Br(),
            html.Label("Instantly Bookable",style={'color': "white"}),
            dcc.Dropdown(
                style={"border": "0px solid black"},
                id='instant-bookable',
                options=[{"label": i, "value": i} for i in instant_bookability],
                value=instant_bookability[0]
            )

        ], style={"textAlign": "float-left"}
    )


def make_menu_layout(neighbourhood):
    return [generate_description_card(), generate_control_card(neighbourhood)]
