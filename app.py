# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

cols_to_use = []
for i in range(20):
    cols_to_use.append(i)

df = pd.read_csv('https://raw.githubusercontent.com/lo1gr/GDPR/master/GDPR.csv', usecols=cols_to_use)
row_names = list(df.Policy)
gdpr_dim = list(df.loc[df['Policy'] == 'POLICY01'].iloc[:, 1:8])
# too long:
# tbc_law = list(df.loc[df['Policy'] == 'POLICY01'].iloc[:, 11:19])[::3]
tbc_law = ['TRANSPARENCY', 'BENEFITS', 'CONTROL']


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div(children=[
    html.H1(children='GDPR visualization', style={'textAlign': 'center'}),

    html.Div(children='''
        Using data graciously labeled by our Data Science class <3.
    ''', style = {'textAlign': 'center'}),

    html.H2(children='Zooming in on 1 Policy:', style={'textAlign': 'center'}),

    dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': v, 'value': v} for v in row_names
            ],
            value='Policy01',
            placeholder='Choose your policy',
            persistence=True,
            style={'textAlign': 'center'}
        ),

    html.Div([
        html.Div([
            dcc.Graph(id='tbc_radar')
        ], className="six columns"),

        html.Div([
            dcc.Graph(id='new_radar')
        ], className="six columns"),
    ], className="row"),

    html.Div([
        html.Div([
                html.P(id='TBC_score', style={'textAlign': 'center', 'border-style': 'solid', 'border-color': 'red'})
        ], className="six columns"),

        html.Div([
            html.P(id='GDPR_score', children='second score', style={'textAlign': 'center', 'border-style': 'solid', 'border-color': 'red'})
        ], className="six columns"),
    ], className="row"),

    html.H2(children='Comparing 2 Policies:', style={'textAlign': 'center'}),

    html.Div([
        html.Div([
            dcc.Dropdown(
                    id='dropdown2_1',
                    options=[
                        {'label': v, 'value': v} for v in row_names
                    ],
                    value='Policy01',
                    placeholder='Choose your policy',
                    persistence=True,
                    style={'textAlign': 'center'}
                ),
        ], className="six columns"),

        html.Div([
            dcc.Dropdown(
                id='dropdown2_2',
                options=[
                    {'label': v, 'value': v} for v in row_names
                ],
                value='Policy01',
                placeholder='Choose your policy',
                persistence=True,
                style={'textAlign': 'center'}
            ),
        ], className="six columns"),
    ], className="row"),





    generate_table(df)
])


@app.callback(
    Output(component_id='new_radar', component_property='figure'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_output_div(input_value):
    fig = [go.Scatterpolar(
            r=[int(x) for x in list(df.loc[df['Policy'] == str(input_value)].iloc[:, 1:8].iloc[0])],
            theta=gdpr_dim,
            fill='toself'
            )]
    layout = {'title': 'GDPR viz for ' + input_value}

    return {"data": fig, "layout": layout}

@app.callback(
    Output(component_id='TBC_score', component_property='children'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_output_div(input_value):
    test = list(df.loc[df['Policy'] == str(input_value)].iloc[:, 11:19].iloc[0])[::3]
    score = int(sum(test))

    return 'TBC score: {}'.format(score)

@app.callback(
    Output(component_id='GDPR_score', component_property='children'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_output_div(input_value):
    test = list(df.loc[df['Policy'] == str(input_value)].iloc[:, 1:8].iloc[0])
    score = int(sum(test))

    return 'GDPR score: {}'.format(score)

@app.callback(
    Output(component_id='tbc_radar', component_property='figure'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_output_div(input_value):
    fig = [go.Scatterpolar(
            r=[int(x) for x in list(df.loc[df['Policy'] == str(input_value)].iloc[:, 11:19].iloc[0])[::3]],
            theta=tbc_law,
            fill='toself'
            )]
    layout = {'title': 'TBC viz for ' + input_value}

    return {"data": fig, "layout": layout}


#
# @app.callback(
#     Output(component_id='new_radar', component_property='figure'),
#     [Input(component_id='dropdown2_1', component_property='value')
#      Input(component_id='dropdown2_2', component_property='value')]
# )
# def update_output_div(input_value):
#     fig = go.Figure()
#     fig = fig.add_trace([go.Scatterpolar(
#             r=[int(x) for x in list(df.loc[df['Policy'] == str(input_value)].iloc[:, 1:8].iloc[0])],
#             theta=gdpr_dim,
#             fill='toself'
#             )])
#     layout = {'title': 'GDPR viz for ' + input_value}
#
#     return {"data": fig, "layout": layout}
#
#
# fig.add_trace(go.Scatterpolar(
#       r=[1, 5, 2, 2, 3],
#       theta=categories,
#       fill='toself',
#       name='Product A'
# ))
# fig.add_trace(go.Scatterpolar(
#       r=[4, 3, 2.5, 1, 2],
#       theta=categories,
#       fill='toself',
#       name='Product B'
# ))


if __name__ == '__main__':
    app.run_server(debug=True)
