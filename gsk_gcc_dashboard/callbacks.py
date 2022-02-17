import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from flask import current_app as app
from flask_caching import Cache
from dash import html, dcc, callback_context
import json
import plotly.graph_objects as go
import numpy as np
import random
from collections import Counter
from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.io as pio
from flask_login import current_user, logout_user, login_required
from dash import dash_table
import vaex
from nltk.corpus import stopwords
import dash_bootstrap_components as dbc



pio.templates.default = "none"
# Initiate logger
log = app.logger
chart_template = "simple_white"


cache = Cache()
TIMEOUT = 1000


class User:
    email = "admin@gmail.com"
    name = "Admin"
    category = "test"


return_null = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No matching data found",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 28, "color": "#ffffff"},
            }
        ],
        "plot_bgcolor": "#396D78",
        "paper_bgcolor": "#396D78",
    }
}
column_change = {
    "comment_text": "Comment Text",
    "toxic": "Toxic",
    "text": "Text",
    "severe_toxic": "Severe Toxic",
    "obscene": "Obscene",
    "threat": "Threat",
    "insult": "Insult",
    "identity_hate": "Identity Hate",
    "not_toxic": "Not Toxic",
}

mark = {
    "background-color": "white",
    "color": "blue",
}

def init_callbacks(dash_app):
    cache.init_app(
        dash_app.server,
        config={
            "CACHE_TYPE": "filesystem",
            "CACHE_DIR": "gsk_gcc_dashboard/data/cache_data",
        },
    )

    @cache.memoize(timeout=100)
    # get data
    def get_data():
        df = vaex.open("gsk_gcc_dashboard/data/final.arrow")
        return df

    # Initial setup - Username
    @dash_app.callback(
        [Output("dash-user-id", "children")], Input("div-on-page-load", "children")
    )
    def update_user_label(pageload):
        return [f"User : {current_user.name}"]

    # data plot
    @cache.memoize(timeout=100)
    @dash_app.callback(
        [Output("pivottable_div", "children")],
        [Input("div-on-page-load", "children"), Input("btn-submit", "n_clicks"),Input("input_search1", "children")],
        [State("input_search", "value")]
    )
    def get_datatable(pageload, n_clicks, input_search1,input_search):
        df = get_data()
        df = df.drop(
            columns=[
                "id",
                "__index_level_0__",
                "__index_level_1__",
                "__index_level_2__",
                "__index_level_3__",
                "__index_level_4__",
                "__index_level_5__",
                "__index_level_6__",
            ]
        )
        if(n_clicks>0 and input_search1):
                input_search = input_search1['props']['children']
        if n_clicks > 0:
                df = df[df["comment_text"].str.contains(input_search, regex=True)]
                df['comment_text'] = df['comment_text'].str.replace(pat='"', repl='')
                df['comment_text'] = df['comment_text'].str.replace(pat=input_search,repl=f' *__{input_search}__* ')
                '''df["text"] = df.comment_text.str.extract_regex(
                    pattern=f"(?P<text>{input_search})"
                )
                df["text"] = df["text"].apply(lambda x: x["text"])'''
                # df['comment_text'] = df['comment_text'].str.replace(pat=df['text'], repl=f'<mark>{df['text']}</mark>')
                return [
                    html.Div(
                        [
                            dash_table.DataTable(
                                id="datatable-interactivity",
                                data=df.to_records(),
                                columns=[
                                    {
                                        "name": column_change[i],
                                        "id": i,
                                        "type": "text",
                                        "presentation": "markdown",
                                    }
                                    for i in df.column_names
                                    if i in column_change.keys()
                                ],
                                page_size=8,
                                style_data={
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "backgroundColor": "#396D78",
                                },
                                style_data_conditional=[
                                    {
                                        'if': {
                                            'filter_query': '{Comment Text} contains {Text}',
                                            'column_id': 'Comment Text'
                                        },
                                        'color': 'blue',
                                        'fontWeight': 'bold'
                                    }],
                                style_cell={"height": "auto", "padding": "5px"},
                                page_action="native",
                                page_current=0,
                                style_header={
                                    "backgroundColor": "#396D78",
                                    "fontWeight": "bold",
                                },
                                                    )
                        ]
                    )
                ]
        else:
            return [
                html.Div(
                    [
                        dash_table.DataTable(
                            id="datatable-interactivity",
                            data=df.to_records(),
                            columns=[
                                {"name": column_change[i], "id": i}
                                for i in df.column_names
                            ],
                            page_size=8,
                            style_data={
                                "whiteSpace": "normal",
                                "height": "auto",
                                "backgroundColor": "#396D78",
                            },
                            style_cell={"height": "auto", "padding": "5px"},
                            page_action="native",
                            page_current=0,
                            style_header={
                                "backgroundColor": "#396D78",
                                "fontWeight": "bold",
                            },
                        )
                    ]
                )
            ]

    # bar plot
    @cache.memoize(timeout=100)
    @dash_app.callback(
        [Output("bar_plot", "figure")],
        [Input("div-on-page-load", "children"), Input("btn-submit", "n_clicks"),Input("input_search1", "children")],State("input_search", "value")
    )
    def get_barplot(pageload, n_clicks, input_search1,input_search):
        df = get_data()
        if (n_clicks > 0 and input_search1):
            input_search = input_search1['props']['children']
        if n_clicks > 0:
            df = df[df["comment_text"].str.contains(input_search, regex=True)]
        cnt = df.sum(
            [
                df.toxic,
                df.severe_toxic,
                df.obscene,
                df.threat,
                df.insult,
                df.identity_hate,
            ]
        )
        values = [
            "toxic",
            "severe_toxic",
            "obscene",
            "threat",
            "insult",
            "identity_hate",
        ]
        fig = px.bar(
            x=values,
            y=cnt,
            title="Toxic Comments Classification",
            color_discrete_sequence=px.colors.sequential.Tealgrn,
        )
        fig.update_layout(
            plot_bgcolor="#396555",
            paper_bgcolor="#396D78",
            title_font_color="#ffffff",
            font_color="#ffffff",
            xaxis_title="Toxic nature",
            yaxis_title="#Comments",
        )
        return [fig]


    # button with one option for each dataframe
    @cache.memoize(timeout=100)
    @dash_app.callback(
        [Output("test_buttons", "children")],
        [Input("btn-submit", "n_clicks")],
        [State("input_search", "value"), State("data_store", "data")],
    )
    def data_push2(n_clicks, input_search, data):
        if n_clicks:
            if n_clicks > 0:
                if data:
                    if input_search not in data:
                        data.append(input_search)
                else:
                    data = [input_search]
            buttons = []
            num = 0
            if data:
                for col in data[-10:]:
                    buttons.append(
                        dbc.Button(
                            col,
                            id=f"button-{num}",
                            className="me-2",
                            color="secondary",
                            n_clicks=0,
                        )
                    )
                    num += 1
                buttons.append(
                    dbc.Button(
                        "Clear Filter",
                        id="clear_filter",
                        className="me-2",
                        color="secondary",
                        n_clicks=0,
                    )
                )
                return [html.Div(buttons)]
            else:
                return []

    # add dropdown menus to the figure

    # filter dropdown
    @cache.memoize(timeout=100)
    @dash_app.callback(
        [Output("filter_dropdown", "options"), Output("data_store", "data")],
        [Input("btn-submit", "n_clicks")],
        [State("input_search", "value"), State("data_store", "data")],
    )
    def data_push(n_clicks, input_search, data):
        if n_clicks:
            if n_clicks > 0:
                if data:
                    if input_search not in data:
                        data.append(input_search)
                else:
                    data = [input_search]

            options = []
            if n_clicks > 0:
                for i in range(len(data)):
                    options.append({"value": data[i], "label": data[i]})
                return [options, data]
            else:
                return [[], data]

    @dash_app.callback(
        [Output("filter_value", "children"), Output("btn-filter", "n_clicks")],
        [Input("filter_dropdown", "value"), Input("btn-filter", "n_clicks")],
    )
    def filter_update(value, n_clicks):
        if n_clicks > 0:
            return [[value], 0]

    @cache.memoize(timeout=100)
    @dash_app.callback(
        [Output("bar_plot1", "figure")],
        [
            Input("div-on-page-load", "children"),
            Input("btn-submit", "n_clicks"),
            Input("bar_plot", "clickData"),Input("input_search1", "children"),Input("input_search", "value")],
    )
    def get_barplot1(pageload, n_clicks, clickData,input_search1, input_search):
        df = get_data()
        if clickData:
            click = json.dumps(clickData, indent=2)
            click = json.loads(click)
            label = click["points"][0]["label"]
            df = df[df[label] == 1]
        if (n_clicks > 0 and input_search1):
            input_search = input_search1['props']['children']
        if n_clicks > 0:
                df = df[df["comment_text"].str.contains(input_search, regex=True)]
        if len(df) > 0:
            df = df.drop(columns=["id", "comment_text", "not_toxic"])
            columns = [
                "toxic",
                "severe_toxic",
                "obscene",
                "threat",
                "insult",
                "identity_hate",
            ]
            df_final = df[df[columns[0]] == 1]
            df_final = df_final.groupby(columns[0], agg="sum")
            for i in columns[1:]:
                df_final1 = df[df[i] == 1]
                df_final1 = df_final1.groupby(i, agg="sum")
                df_final = df_final.concat(df_final1)
            df_final = pd.DataFrame(df_final.to_records())
            for column in df_final.columns:
                if column in columns:
                    df_final.loc[df_final[column] == 1,column+'_sum'] = df[column].sum()
            df_final.fillna(0,inplace=True)
            df_final.set_index(columns, inplace=True)
            fig = go.Figure(
                data=go.Heatmap(
                    z=df_final,
                    y=[
                        "toxic",
                        "severe_toxic",
                        "obscene",
                        "threat",
                        "insult",
                        "identity_hate"
                    ],
                    x=[
                        "severe_toxic_sum",
                        "obscene_sum",
                        "threat_sum",
                        "insult_sum",
                        "identity_hate_sum",
                        "toxic_sum"
                    ],
                    colorscale="tealgrn",
                )
            )
            fig.update_layout(
                title="Toxic Comments Values",
                plot_bgcolor="#396555",
                paper_bgcolor="#396D78",
                title_font_color="#ffffff",
                font_color="#ffffff",
                xaxis_title="Toxic nature",
                yaxis_title="#Comments"
            )
            return [fig]
        else:
            fig = go.Figure()
            fig.update_layout(
                title="Toxic Comments Values",
                plot_bgcolor="#396555",
                paper_bgcolor="#396D78",
                title_font_color="#ffffff",
                font_color="#ffffff",
                xaxis_title="Toxic nature",
                yaxis_title="#comments",
            )
            return [fig]

    @cache.memoize(timeout=100)
    @dash_app.callback(
        [Output("word_cloud", "figure")],
        [
            Input("div-on-page-load", "children"),
            Input("btn-submit", "n_clicks"),Input("input_search1", "children"),Input("input_search", "value")
        ],
        [ State("bar_plot", "clickData")],
    )
    def get_wordcloud(pageload, n_clicks,input_search1,input_search, clickData):
        df = get_data()
        if clickData:
            click = json.dumps(clickData, indent=2)
            click = json.loads(click)
            label = click["points"][0]["label"]
            df = df[df[label] == 1]
        if (n_clicks > 0 and input_search1):
            input_search = input_search1['props']['children']
        if n_clicks > 0:
                df = df[df["comment_text"].str.contains(input_search, regex=True)]
        if len(df) > 0:
            df.comment_text = df.comment_text.astype(str)
            records = df.to_records(column_names=["comment_text"])
            text = [records[i]["comment_text"] for i in range(len(records))]
            text = "".join(text)
            text = text.lower()
            text = text.split(" ")
            cnt = Counter(text)
            cnt_new = []
            i = 0
            x = 0
            cnt = cnt.most_common(150)
            while i < 35:
                if cnt[x][0] not in stopwords.words("english"):
                    cnt_new.append(cnt[x][0])
                    i += 1
                x += 1
            weights = list(range(10, 45))[::-1]
            data = go.Scatter(
                x=[random.randint(0, 20) for i in range(35)],
                y=[random.randint(0, 20) for i in range(35)],
                mode="text",
                text=cnt_new,
                textfont={"size": weights, "color": "white"},
                textposition="top center",
            )
            layout = go.Layout(
                {
                    "xaxis": {
                        "showgrid": False,
                        "showticklabels": False,
                        "zeroline": False,
                    },
                    "yaxis": {
                        "showgrid": False,
                        "showticklabels": False,
                        "zeroline": False,
                    },
                }
            )
            fig = go.Figure(data=[data], layout=layout)
            fig.update_layout(
                title="Toxic Comments",
                plot_bgcolor="#396555",
                paper_bgcolor="#396D78",
                title_font_color="#ffffff",
                font_color="#ffffff",
            )
            return [fig]
        else:
            fig = go.Figure()
            fig.update_layout(
                title="Toxic Comments",
                plot_bgcolor="#396555",
                paper_bgcolor="#396D78",
                title_font_color="#ffffff",
                font_color="#ffffff",
                xaxis_title="Toxic nature",
                yaxis_title="Count",
            )
            return [fig]

    @dash_app.callback(
        [Output("btn-submit", "n_clicks"), Output("input_search", "value")],
        [Input("clear_filter", "n_clicks")],
    )
    def reset_search(n_clicks):
        if n_clicks > 0:
            return [0, ""]

    """for i in range(0,10):
            @dash_app.callback([Output(f"input_search_{i}", "children")],
                           [Input(f'button-{i}', 'n_clicks'), Input(f'button-{i}', 'children')])
            def reset_buttons(n_clicks, children):
                changed_id = [p['prop_id'] for p in callback_context.triggered][0]
                give_null=True
                if (n_clicks):
                    if(n_clicks> 0):
                        return [html.Div([p for p in callback_context.triggered][0])]"""

    @dash_app.callback(
        [Output(f"input_search_0", "children")],
        [Input(f"button-0", "n_clicks"), Input(f"button-0", "children")],
    )
    def reset_buttons0(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-0.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output(f"input_search_1", "children")],
        [Input(f"button-1", "n_clicks"), Input(f"button-1", "children")],
    )
    def reset_buttons1(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-1.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output(f"input_search_2", "children")],
        [Input(f"button-2", "n_clicks"), Input(f"button-2", "children")],
    )
    def reset_buttons2(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-2.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output(f"input_search_3", "children")],
        [Input(f"button-3", "n_clicks"), Input(f"button-3", "children")],
    )
    def reset_buttons3(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-3.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output(f"input_search_4", "children")],
        [Input(f"button-4", "n_clicks"), Input(f"button-4", "children")],
    )
    def reset_buttons4(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-4.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output(f"input_search_5", "children")],
        [Input(f"button-5", "n_clicks"), Input(f"button-5", "children")],
    )
    def reset_buttons5(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-5.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output(f"input_search_6", "children")],
        [Input(f"button-6", "n_clicks"), Input(f"button-6", "children")],
    )
    def reset_buttons6(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-6.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output(f"input_search_7", "children")],
        [Input(f"button-7", "n_clicks"), Input(f"button-7", "children")],
    )
    def reset_buttons7(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-7.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output(f"input_search_8", "children")],
        [Input(f"button-8", "n_clicks"), Input(f"button-8", "children")],
    )
    def reset_buttons8(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-8.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output(f"input_search_9", "children")],
        [Input(f"button-9", "n_clicks"), Input(f"button-9", "children")],
    )
    def reset_buttons9(n_clicks, children):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        give_null = True
        if n_clicks:
            if n_clicks > 0:
                if f"button-9.n_clicks" == changed_id:
                    return [html.Div(children)]
        if give_null == True:
            return [None]

    @dash_app.callback(
        [Output("input_search1", "children")],
        [Input("filter_value", "children"),
         Input("btn-submit", "n_clicks"),
            Input("clear_filter", "n_clicks"),
            Input("input_search_0", "children"),
            Input("input_search_1", "children"),
            Input("input_search_2", "children"),
            Input("input_search_3", "children"),
            Input("input_search_4", "children"),
            Input("input_search_5", "children"),
            Input("input_search_6", "children"),
            Input("input_search_7", "children"),
            Input("input_search_8", "children"),
            Input("input_search_9", "children")
        ],
    )
    def update(v,btn, n_clicks, i0, i1, i2, i3, i4, i5, i6, i7, i8, i9):
        changed_id = [p["prop_id"] for p in callback_context.triggered][0]
        print(v,btn, n_clicks, i0, i1, i2, i3, i4, i5, i6, i7, i8, i9)
        if n_clicks > 0:
            if('clear_filter' in  changed_id):
                return []
        if('filter_value' not in changed_id):
            v = []
        if ('btn-submit' in changed_id):
            return []
        if v:
            return [{'props':{'children':v[0]}}]
        elif i0:
            return [i0]
        elif i1:
            return [i1]
        elif i2:
            return [i2]
        elif i3:
            return [i3]
        elif i4:
            return [i4]
        elif i5:
            return [i5]
        elif i6:
            return [i6]
        elif i7:
            return [i7]
        elif i8:
            return [i8]
        elif i9:
            return [i9]
        else:
            return []


    @dash_app.callback(
        Output("output-state", "children"), Input("btn-logout", "n_clicks")
    )
    def logout_page(n_clicks):
        if n_clicks > 0:
            from flask import redirect, url_for
            from flask import make_response, render_template
            logout_user()
            return render_template("login.html")
