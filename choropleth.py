'''
Assignment 7
Name: Nika Kolin Melocoton
Student ID: 211015210
Class: CP321
Date: 04-01-25
Code Purpose: Creating jupyter notebook to python to be able to render
'''
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1(children = 'FIFA Winners Dashboard', style = {'textAlign':'center'}),
    html.Div([
        html.Label('Select Year'),
        dcc.Dropdown(
            id = 'year-selector',
            options = [
            {'label':'All FIFA Winners', 'value':'All'},
            {'label':'1930', 'value':1930},
            {'label':'1934', 'value':1934},
            {'label':'1938', 'value':1938},
            {'label':'1950', 'value':1950},
            {'label':'1954', 'value':1954},
            {'label':'1958', 'value':1958},
            {'label':'1962', 'value':1962},
            {'label':'1966', 'value':1966},
            {'label':'1970', 'value':1970},
            {'label':'1974', 'value':1974},
            {'label':'1978', 'value':1978},
            {'label':'1982', 'value':1982},
            {'label':'1986', 'value':1986},
            {'label':'1990', 'value':1990},
            {'label':'1994', 'value':1994},
            {'label':'1998', 'value':1998},
            {'label':'2002', 'value':2002},
            {'label':'2006', 'value':2006},
            {'label':'2010', 'value':2010},
            {'label':'2014', 'value':2014},
            {'label':'2018', 'value':2018},
            {'label':'2022', 'value':2022},
        ],
            value = 'All'),
        dcc.Graph(id = 'choropleth-fig')
    ])
], style = {'padding': '50px'})

@callback(
    Output('choropleth-fig','figure'),
    Input('year-selector','value')
)

def update_graph(chosen_year):
    fig = go.Figure()
    data = pd.read_csv('data.csv')
    winners = list(data['Winner'])
    winners_counts = {}
    for winner in winners:
        if winner not in winners_counts:
            winners_counts[winner] = 1
        else:
            winners_counts[winner] = winners_counts[winner] + 1
    new_data = pd.DataFrame({'Countries': list(winners_counts.keys()),
                             'Wins': list(winners_counts.values())})

    if chosen_year == 'All':
        fig = px.choropleth(
            new_data,
            locations = 'Countries',
            locationmode = 'ISO-3',
            color = 'Wins',
            scope = 'world',
            title = 'FIFA World Cup Winners'
        )
    else:
        selected_game = data.loc[data['Year']==chosen_year]
        countries = list([selected_game.loc[selected_game.index[0],'Winner'],selected_game.loc[selected_game.index[0],'Runner-Up']])
        final_status = list(selected_game.columns[1:])
        new_data = pd.DataFrame({
            'Countries':countries,
            'Final Status':final_status
        })
        fig = px.choropleth(
            new_data,
            locations = 'Countries',
            locationmode = 'ISO-3',
            color = 'Final Status',
            scope = 'world',
            title = f'FIFA World Cup {chosen_year}'
        )
    
    fig.update_layout(
        title_x = 0.5
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
