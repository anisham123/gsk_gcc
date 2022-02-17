from dash import html, dcc

from textwrap import dedent as d

import dash_bootstrap_components as dbc

tabs_styles = {
    "zIndex": 99,
    "display": "inlineBlock",
    "height": "10vh",
    "width": "12vw",
    "position": "fixed",
    "background": "#967996",
    "top": "12.5vh",
    "left": "7.5vw",
    "border": "#967996",
    "border-radius": "4px",
}

tab_style = {
    "background": "#967996",
    "text-transform": "uppercase",
    "color": "#000000",
    "border": "#967996",
    "font-size": "11px",
    "font-weight": "bold",
    "align-items": "center",
    "justify-content": "center",
    "border-radius": "4px",
    "padding": "6px",
}

tab_selected_style = {
    "background": "",
    "text-transform": "uppercase",
    "color": "#ffffff",
    "font-size": "11px",
    "font-weight": "bold",
    "border": "#835383",
    "border-radius": "4px",
    "align-items": "center",
    "justify-content": "center",
    "padding": "8px",
}
mark = {
    "background-color": "white",
    "color": "blue",
}

styles = {"pre": {}}



html_layout = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.H3("Toxic Comments Analysis"),
                                            html.Div("User : ", id="dash-user-id"),
                                        ],
                                        style={
                                            "textAlign": "left",
                                            "color": "#ffffff",
                                        },
                                    )
                                ]
                            ),
                            # Logout button
                            dbc.Col(
                                html.Div(
                                    [
                                        html.A(
                                            html.Button(
                                                id="btn-logout",
                                                n_clicks=0,
                                                children="Logout",
                                            ),
                                            href="/logout",
                                        )
                                    ],
                                    style={"textAlign": "right"},
                                )
                            ),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        dcc.Textarea(
                                            id='input_search',
                                            placeholder='Search Comment & click on submit',
                                            style={'width': '100%', 'height': 35},
                                        ),
                                    ]
                                ),
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.A(
                                            html.Button(
                                                id="btn-submit",
                                                n_clicks=0,
                                                children="Submit",
                                            )
                                        )
                                    ],
                                )
                            ),
                            dbc.Col(
                                html.Div(
                                    [dcc.Dropdown(placeholder='Select Previous search and click on tick mark',
                                                  id='filter_dropdown',
                                                  options=[],
                                                  value=[],
                                                  multi=False
                                                  )], style={'offset': 12, 'color': '#396555',
                                                             'fontcolor': '#000000',
                                                             'border': '0px',
                                                             'font-weight': 'bold'
                                                             }), ),

                            dbc.Col(html.Div(
                                [
                                    html.A(
                                        html.Button(
                                            id="btn-filter",
                                            n_clicks=0,
                                            children="✓",
                                        ),
                                    )
                                ],
                            ), ),

                        ]
                    ),

                    dbc.Row(
                        [html.Div(id=f"input_search_{i}",hidden=True) for i in range(10)]),
                    html.Div(id="test_buttons"),
                    html.Div(id="input_search1",hidden=True),
                    html.Div(id="output-state", hidden=True),
                    html.Div(id="filter_value", hidden=True),
                    dbc.Row([dcc.Store(id="data_store")]),
                    html.Br(),
                    html.Div(id="pivottable_div"),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col([dcc.Graph(id="bar_plot")], width={"size": 6}),
                            dbc.Col([dcc.Graph(id="bar_plot1")], width={"size": 6}),
                        ]
                    ),
                    html.Br(),
                    dbc.Row(
                        [

                            dbc.Col([dcc.Graph(id="word_cloud")]),
                        ]
                    ),
                    html.Div(id="clickData_out"),
                    html.Br(),
                ],
                style={
                    "background": "#396D80",
                    "background-color": "#396D80",
                    "color": "#ffffff",
                    "border": "0px",
                    "font-weight": "bold",
                    "textAlign": "centre",
                },
            )
        ),
        html.Div(id="div-on-page-load", hidden=True),
    ]
)
