import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import plotly.offline as pyo
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from dash.dependencies import  Input, Output, State
import joblib
import markdown

###################
### Data Import ###
###################
path = 'Data/product_reviews.csv'
data = pd.read_csv(path)

######################
### Loading Models ###
######################

nmf_neg = joblib.load('Models/nmf_neg.sav')
nmf_pos = joblib.load('Models/nmf_pos.sav')
tfidf_neg = joblib.load('Models/tfidf_neg.sav')
tfidf_pos = joblib.load('Models/tfidf_pos.sav')

# Create app obj
app = dash.Dash()
server = app.server

#################
### App Layut ###
#################

app.layout = html.Div([
                dcc.Tabs(
                    id='tabs',
                    value='tab-1',
                    children=[
                        dcc.Tab(label='Motivation',
                                value='tab-1'),
                        dcc.Tab(label='General Information',
                                value='tab-2'),
                        dcc.Tab(label='Visualizations',
                                value='tab-3')
                    ]),
                html.Div(id='content')
            ])

###############
### Figures ###
###############
topics_dict = {0:'Music/Video/Screen',
               1:'Ease of Use/Setup',
               2:'House/Family - Gift/Christmas',
               3:'Voice/Screen/Setup Problems'}

traces_scatter = [go.Scatter(
            x=data[data['topic'] == topic]['reviews.rating'] +
            0.05*np.random.randn(len(data[data['topic'] == topic]['reviews.rating'])),
            y=data[data['topic'] == topic]['compound'],
            mode='markers',
            name=topics_dict[topic],
            marker={'opacity':0.65,
                   'size':7},
        ) for topic in data['topic'].unique()]

layout_scatter = go.Layout(
            title='Product Reviews Sentiment Analysis and Topic Modeling',
            xaxis=dict(title='Review Score'),
            yaxis=dict(title='Sentiment Score'),
            hovermode='closest',
            height=650
            )

fig_scatter = go.Figure(data=traces_scatter, layout=layout_scatter)

fig_scatter.add_trace(go.Scatter(x=[0.5, 4.2], #Avg Lines Labels
                   y=[0.65,-0.9],
                   text=['Avg Sentiment \n Score',
                        'Avg Review Score'],
                   mode='text',
                   hoverinfo='skip',
                    name=None))

fig_scatter.add_shape(
    # Average Sentiment Score
    type='line',
    x0=0,
    y0=data['compound'].mean(),
    x1=5.5,
    y1=data['compound'].mean()
)

fig_scatter.add_shape(
    # Average Review Score
    type='line',
    x0=data['reviews.rating'].mean(),
    y0=-1,
    x1=data['reviews.rating'].mean(),
    y1=1
)

topics_df = data.groupby('comp_score').mean()

fig_bar = px.bar(data_frame=topics_df, x=topics_df.index, y='reviews.rating', hover_data=['compound', 'reviews.doRecommend'], color=topics_df.index)

fig_bar.update_xaxes(title='Sentiment Score')
fig_bar.update_yaxes(title='Average Review Score')
fig_bar.update_layout(title='Review Sentiment', height=625)

topics_list = []
for index,topic in enumerate(nmf_pos.components_):
    topics_list.append([tfidf_pos.get_feature_names()[i] for i in topic.argsort()[-10:]])

for index,topic in enumerate(nmf_neg.components_):
    topics_list.append([tfidf_neg.get_feature_names()[i] for i in topic.argsort()[-10:]])

topics = data['topic_desc'].unique()

fig_table = go.Figure(data=[go.Table(
    header=dict(values=['Topic','Most Frequent Words in Reviews'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[[topics[i]for i in range(len(topics))],
                        [topics_list[i] for i in range(len(topics))]],
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
])

fig_table.update_layout(width=900, height=300)

################################
### Loading Markdown Content ###
################################

### Tab 1
md_mot = open('Files/Motivation.md', 'r')
motivation_string = md_mot.read()
md_mot.close()


### Tab 2
md_file = open('Files/README.md', 'r')
file_string = md_file.read()
md_file.close()

### tab 3

md_insights = open('Files/Insights.md', 'r')
insights_string = md_insights.read()
md_insights.close()

#################
### Callbacks ###
#################

@app.callback(Output('content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):

    if tab == 'tab-1':
        return html.Div([
                dcc.Markdown(
                    id='mrkdwn-tab1',
                    children=[motivation_string]
                )
            ])

    elif tab == 'tab-2':
        return html.Div([
            html.H1('Context For Understanding the Dashboard'),
            dcc.Markdown(
                id='mrkdwn-tab2',
                children=[file_string]
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
                    html.Div([
                        dcc.Graph(
                            id='scatter',
                            figure=fig_scatter
                            ),
                    ], style={
                        'width':'50%',
                        'height':'135%',
                        'display':'inline-block'
                        }),
                    html.Div([
                        dcc.Graph(
                            id='bar',
                            figure=fig_bar
                        )
                    ], style={
                        'width':'50%',
                        'height':'135%',
                        'display':'inline-block',
                        'verticalAlign':'paddingRight'
                        }),
                    html.Div([
                        dcc.Graph(
                        id='table',
                        figure=fig_table
                        )
                    ], style={
                        'display':'inline-block',
                        }),
                    html.Div([
                        html.H3('Key Insights:'),
                        dcc.Markdown(
                            id='mrkdwn-tab3',
                            children=[insights_string]
                        )
                    ])
        ])


if __name__ == '__main__':
    app.run_server()
