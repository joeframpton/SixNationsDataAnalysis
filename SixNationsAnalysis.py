import pandas as pd
import plotly.graph_objects as go
import numpy as np
import statsmodels.api as sm
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Data Processing

df = pd.read_csv('sixnationsstats_V3.csv')
df['score_margin'] = df['score'] - df['opp_score']
df['abs_score_margin'] = df['score_margin'].abs()
df['kick_margin'] = df['kicks'] - df['opp_kicks']
df['cards'] = df['yellow_cards'] + df['red_cards']
df['set_piece_success%'] = (df['scrums_won%'] + df['lineouts_won%']) / 2
df['opp_set_piece_success%'] = (df['opp_scrums_won%'] + df['opp_lineouts_won%']) / 2
df['total_kicks'] = df['kicks'] + df['opp_kicks']
df['total_tries'] = df['tries'] + df['opp_tries']

#dropnas
df = df.dropna(subset=['tries'])
df = df.dropna(subset=['score'])

key_stats = ['linebreaks', 'carries', 'to_won', 'tackles_made', 'tackle_success_rate%',
                   'kicks', 'kick_ratio', 'set_piece_success%', 'penalties_won', 'kick_ratio'] 

for stat in key_stats:
    new_col_name = stat + '_dom'
    opp_stat = 'opp_' + stat
    df[new_col_name] =  df[stat] > df[opp_stat]

def win_lose(margin):
    if margin > 0:
        return 'won'
    elif margin < 0:
        return 'lost'
    else:
        return None

def coded_win_lose(win_lose):
    if win_lose == 'won':
        return 1
    elif win_lose == 'lost':
        return 0
    
df['win_or_lose'] = df['score_margin'].map(win_lose)
df['coded_win_or_lose'] = df['win_or_lose'].map(coded_win_lose)   

#Beginning to pull charts together

stat_list_for_x = {'linebreaks':['Linebreaks','the Number of Linebreaks'],
                   'kick_ratio':['Kick to Pass Ratio','the Kick to Pass Ratio'],
                   'kicks':['Kicks','the Number of Kicks'],
                   'tackles_made':['Tackles','the Number of Tackles'],                        
                   'penalties_won':['Penalties Won','the Number of Penalties Won'],
                   'set_piece_success%':['Own Set Piece Retention (%)','Retaining Posession on Own Set Piece'],
                   'to_won': ['Turnovers Won','the Number of Turnovers Won'],
                  }

win_percentage = {}

for stat, title in stat_list_for_x.items():
    dom_stat = stat + '_dom'
    df_of_stat = df[dom_stat]
    win_percentage[title[0]] = round(len(df[(df[dom_stat] == True) & (df['win_or_lose'] == 'won')]) / df_of_stat.sum() * 100, 1)

win_percentage_dict = {
    'theta' : list(win_percentage.keys()),
    'r' : list(win_percentage.values())
    }

r = win_percentage.values()
theta = win_percentage.keys()

#Figure 1 
def create_polar_bar():
    color_no = [int(x*10) for x in r]

    fig = go.Figure(data=go.Barpolar(
        r = win_percentage_dict.get('r'),
        theta = win_percentage_dict.get('theta'),
        marker= dict(cmax=850,
                     cmin=350,
                     color=color_no,
                     colorscale='Greens',
                     line_width=0),
        opacity=1,
        hovertemplate= '%{theta}: <b>%{r}</b>%<extra></extra>',
        hoverlabel=dict(bgcolor='white',
                        font=dict(color="#0c0c28")
                        ),
    ))

    fig.update_layout(
        title = dict(text='Win percentage when a team dominates in a given statistic'),
        polar = dict(radialaxis = dict(range=[0, 100]),
                     bgcolor= "#11123b"),
        font=dict(color="#FFFFFF"),
        paper_bgcolor= "#11123b")

    return fig

# Setting and Prep for Figure 2

color_scheme = {
    'England' : '#ffffff',
    'France' : '#0000c0',
    'Ireland' : '#00845c',
    'Italy' : '#0076ff',
    'Scotland' : '#002a66',
    'Wales' : '#e32a2d',
    }

marker_sizes = {0: 8,
                1: 9.5,
                2: 11,
                3: 12.5,
                4: 14,
                5: 15.5,
                6: 17,
                7: 18.5,
                8: 20,
                9: 21.5
               }

# Creating the Dash App

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#11123b',
    'text': '#FFFFFF',
    'width': '99vw'
}

header = 'Do teams kick too much? Is kicking making rugby boring?'
pre_text = 'There\'s a lot of disscussion about kicking in the modern game with some pundits arguing that'\
            ' kicking is killing the game. Have a look through the stats yourself to see if they\'re right.'
first_text = 'Note: A team is dominant in a stat when they simply outnumber or outscore their opposition in that stat. i.e. they' \
             ' made more tackles or kicked more times.'
second_text = '"Okay, teams that kick more win more. But I don\'t want to watch a boring match. I want excitement'\
            ' - lots of tries and high scores!"'
third_text = 'Have a look for yourself - which of these stats tend towards a higher score with more tries?'
fourth_text = 'Note: The bigger the circle, the more tries that the team has scored. You can hover over to see which match'\
            ' it relates to.'


#Arranging the Layout
app.layout = dbc.Container(
    style={'backgroundColor': colors['background'],
           'color': colors['text'],           
          },
    children=[
        html.Div(className= 'm-2',
                children=[
                html.H1([header], style={'text-align': 'center'}, className='m-4 p-1'),
                html.Div(children=[
                    html.H6(pre_text),
                    html.P(html.Small(html.I(first_text)))
                ]),
#Figure One
                dcc.Graph(id='polar',
                         figure=create_polar_bar()),

                html.Div(children=[
                    html.P(html.I(html.B(second_text)), style={'text-align': 'center'}),
                    html.H6(third_text),
                    html.P(html.Small(html.I(fourth_text)))
                ]),


                dbc.Row(
                    [
                        dbc.Col([
                            dbc.Label('Select a Stat:', html_for='scatter_dropdown'),
                            dcc.Dropdown(id='scatter_dropdown',
                                
                                options=[{'label': title[0], 'value': stat} for stat, title in stat_list_for_x.items()],
                                value = 'kicks',
                                optionHeight= 45,
                                searchable = False,
                                placeholder = 'Please select a stat',
                                clearable = False,
                                style={'width': "95%", 'color':colors['background']})
                        ], width=2),
#Figure 2
                        dbc.Col([
                            dcc.Graph(id='scatter'),
                        ], width=10),

                    ], align='center'
                ),

            ])
    ])

#Function for creating Figure 2
@app.callback(
    Output(component_id='scatter', component_property='figure'),
    [Input(component_id='scatter_dropdown', component_property='value')]
)
def create_graph(stat):
    graph_df = df
    
    title = stat_list_for_x.get(stat)
    fig = go.Figure()
   
    for team, color in color_scheme.items():
        df_team = graph_df[graph_df['team'] == team]
        sizes = df_team['tries'].map(marker_sizes).fillna(10)
        
        #Add a trace per team
        trace = go.Scatter(
                x= df_team[stat],
                y= df_team['score'],
                customdata= np.stack((df_team['team'], df_team['opp_team'], df_team['year'], df_team['tries']), axis=1),
                name= team,
                mode='markers',
                marker=dict(size= sizes, 
                            color= color,
                            opacity= 0.9,
                            ),  
                hoverlabel=dict(bgcolor='white',
                                font=dict(color="#0c0c28")),
                hovertemplate='<b>%{customdata[0]}</b> against %{customdata[1]}, %{customdata[2]}<br>'\
                                '<b>%{customdata[3]}</b> tries<extra></extra>',
        )
        
        fig.add_trace(trace)
    
    #Add a trendline    
    x = sm.add_constant(df[stat])
    y = df['score'].values.reshape(-1, 1)
    model = sm.OLS(y, x).fit()
    trendline_R2 = model.rsquared
    m = model.params[1]
    b = model.params[0]

    trendline_x = np.array([df[stat].min(), df[stat].max()])
    trendline_y = m * trendline_x + b
    
    fig.add_trace(go.Scatter(x=trendline_x, y=trendline_y, mode='lines', 
                             line=dict(color='#d97f43', width=2),
                             name= "Overall Trend",
                             hoverinfo='skip'
                             ))
    
    
    #Add a title, format & label axes
    fig.update_layout(title=f'Impact of {title[1]} has on the Score', 
                      font=dict(color="#FFFFFF"),
                      paper_bgcolor="#11123b",
                      plot_bgcolor= "#0c0c28",
                     )
    
    x_axis_min = 0
    if df[stat].min() == 0:
        x_axis_min = -1.5
        
    x_axis_max = df[stat].max()*1.05
        
    fig.update_xaxes(title_text=title[0].title(), 
                     range=[x_axis_min, x_axis_max]
                    )
    fig.update_yaxes(title_text='Score',                    
                     range=[-5,75]
                    )

    return (fig)

if __name__ == '__main__':
    app.run_server(debug=True)