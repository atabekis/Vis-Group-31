import dash
import dash_loading_spinners
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import functions.config as config
from functions.mapboxplot import Mapboxplot
from functions.choropleth_mapbox import Choropleth
import numpy as np
import pandas as pd
from textwrap import dedent
import dash_loading_spinners
import time

app = dash.Dash(__name__)


def build_banner():
    return html.Div(
        id='banner',
        className='banner',
        children=[
            html.H5('Somebody please end my suffering'),
            # html.Br,
            # html.H6('Bartan is a little bitch'),
            # html.Img(src='assets/TUE.png'),
            html.Button(
                id='whats-this-button',
                children="What's This?",
                n_clicks=0),
            html.Img(src='assets/TUE.png'),
        ]
    )


def build_explanation():
    return html.Div(
        id='markdown',
        className='modal',
        style={'display': 'none'},
        children=[
            html.Div(
                id='markdown-container',
                className='markdown-container',
                children=[
                    html.Div(
                        className='close-container',
                        children=[html.Button(
                            'Close',
                            id='markdown-close',
                            n_clicks=0,
                            className='closeButton'
                        )]
                    ),
                    html.Div(
                        className='markdown-text',
                        children=dcc.Markdown(
                            children=dedent("""
                            IM WRITING THIS TO LET YOU KNOW THAT BARTAN IS A LITTLE BITCH
                            AND I STAND WITH WHAT I SAY :)))
                            """)
                        )
                    )
                ]
            )
        ]
    )


def build_tabs():
    return html.Div(
        id='tabs',
        className='row container scalable',
        children=[
            dcc.Tabs(
                id='app-tabs',
                value='tab1',
                className='custom-tabs',
                children=[
                    dcc.Tab(
                        id='tab1',
                        label='Choropleth',
                        value='tab1',
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        disabled_style={
                            'backgroundColor': '#2d3038',
                            'color': '#95969A',
                            'borderColor': '#23262E',
                            'display': 'flex',
                            'flex-direction': 'column',
                            'alignItems': 'center',
                            'justifyContent': 'center'
                        },
                        disabled=False,
                        children=[
                            html.Div(
                                children=[
                                    html.Br(),
                                    html.Br(),
                                    # map_choropleth,
                                    dcc.Loading(id='loading-icon',children=[map_choropleth])

                                ]
                            )
                        ]
                    ),
                    dcc.Tab(
                        id='tab2',
                        label='Mapbox',
                        value='tab2',
                        className='custom-tab',
                        selected_className='custom-tab--selected',
                        disabled_style={
                            'backgroundColor': '#2d3038',
                            'color': '#95969A',
                            'borderColor': '#23262E',
                            'display': 'flex',
                            'flex-direction': 'column',
                            'alignItems': 'center',
                            'justifyContent': 'center'
                        },
                        children=[
                            html.Div(
                                build_mapbox_controls('All')
                            ),
                            html.Div(
                                children=map_boxplot
                            )
                        ],
                        disabled=False)

                ]
            )
        ]
    )


def build_choropleth_controls():
    pass

def build_mapbox_controls(neighbourhood_name):
    # Define the basic variables
    neighbourhood_group = config.get_neighbourhood_groups()
    neighbourhood = config.get_neighbourhood()
    min_price, max_price = config.get_price_min_max()
    instant_bookability = config.get_inst_bookable()
    min_service_fee, max_service_fee = config.get_service_fee()

    return html.Div(
        id='tab1-content',
        children=[
            html.Br(),
            html.Div(style={'display': 'flex', 'justify-content': 'space-between'},
                     children=[
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      html.Label('Select Neighbourhood Group'),
                                      dcc.Dropdown(
                                          style={"border": "0px solid black"},
                                          id="select-neighbourhood-group",
                                          options=[{"label": i, "value": i} for i in neighbourhood_group],
                                          value=neighbourhood_group[
                                              np.where(neighbourhood_group == neighbourhood_name)[0][0]],
                                      )
                                  ]
                                  ),
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  id='test',
                                  children=[
                                      html.Label('Select Neighbourhood'),
                                      dcc.Dropdown(
                                          style={"border": "0px solid black"},
                                          id="select-neighbourhood",
                                          options=[{"label": i, "value": i} for i in neighbourhood[neighbourhood_name]],
                                          value=neighbourhood[neighbourhood_name][0],
                                      )
                                  ]
                                  ),
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      html.Label('Price Range', style={'margin-left': '20px'}),
                                      dcc.RangeSlider(
                                          # TODO: ADD CLASSNAME HERE AND IN CSS
                                          min=min_price,
                                          max=max_price,
                                          value=[min_price, max_price],
                                          allowCross=False,
                                          id='price-range-slider',
                                          marks={
                                              min_price: {'label': str(min_price)},
                                              max_price: {'label': str(max_price)}
                                          },
                                          tooltip={"placement": "bottom", "always_visible": False}
                                      )
                                  ]
                                  ),
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      html.Label('Service Fee', style={'margin-left': '20px'}),
                                      dcc.RangeSlider(
                                          min=min_service_fee,
                                          max=max_service_fee,
                                          value=[min_service_fee, max_service_fee],
                                          allowCross=False,
                                          id='service-fee-range-slider',
                                          marks={
                                              min_price: {'label': str(min_service_fee)},
                                              max_price: {'label': str(max_service_fee)}
                                          },
                                          tooltip={"placement": "bottom", "always_visible": False}
                                      )
                                  ]
                                  ),
                         html.Div(style={'width': '20%', 'height': '100px', 'margin': '5px'},
                                  children=[
                                      html.Label("Instantly Bookable"),
                                      dcc.Dropdown(
                                          style={"border": "0px solid black"},
                                          id='instant-bookable',
                                          options=[{"label": i, "value": i} for i in instant_bookability],
                                          value=instant_bookability[0]
                                      )
                                  ]
                                  )
                     ]
                     )
        ]
    )


data = pd.read_csv("Data/airbnb_open_data_clean.csv", low_memory=False)

map_boxplot = Mapboxplot("boxplot1", data)
map_choropleth = Choropleth('choropleth', data)

app.layout = html.Div(
    children=[
        build_banner(),
        build_tabs(),
        html.Div(
            id='app-content',
            className='container scalable'
        )
    ]
)


# app.layout = html.Div(
#      children=[
#              html.Div(
#                  className="div-app",
#                  id="div-app",
#                  children=[
#                      build_banner(),
#                      build_tabs(),
#                      html.Div(
#                          id='app-content',
#                          className='container scalable'
#                      )
#                  ]
#              )
#          ]
#      )


# @app.callback(
#     Output("div-loading", "children"),
#     [
#         Input("div-app", "loading_state")
#     ],
#     [
#         State("div-loading", "children"),
#     ]
# )
# def hide_loading_after_startup(
#         loading_state,
#         children
# ):
#     if children:
#         print("remove loading spinner!")
#         time.sleep(3)
#         return None
#     print("spinner already gone!")
#     raise PreventUpdate



@app.callback(Output('markdown', 'style'),
              Input('whats-this-button', 'n_clicks'),
              Input('markdown-close', 'n_clicks'))
def update_markdown(open_click, close_click):
    callback = dash.callback_context
    if callback.triggered:
        prop_id = callback.triggered[0]['prop_id'].split('.')[0]
        if prop_id == 'whats-this-button':
            return {'display':'block'}
    return {'display':'none'}



@app.callback(
    Output(map_boxplot.html_id, "figure"), [
        Input("select-neighbourhood-group", "value"),
        Input("select-neighbourhood", "value"),
        Input('price-range-slider', "value"),
        Input('instant-bookable', "value"),
        Input('service-fee-range-slider', 'value')
    ])
def update_mapboxplot(neighbourhood_group, neighbourhood, price_range, inst_bookable, service_fee_range):
    return map_boxplot.update(neighbourhood_group, neighbourhood, price_range, inst_bookable, service_fee_range)


@app.callback(
    Output("tab1-content", "children"),
    Input("select-neighbourhood-group", "value")
)
def update_neighbourhoods(neighbourhood):
    return [build_mapbox_controls(neighbourhood)]

@app.callback(
    Output(map_choropleth.html_id, 'figure'),
    Input('app-tabs', 'value')
)
def update_map_choropleth(asd):
    return map_choropleth.update()


app.run_server()
