#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Source Code
# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

# Read the world bank  data into pandas dataframe
w = pd.read_csv("https://raw.githubusercontent.com/arthurozw/Historic-GDP-Data/main/worldstats2.csv")

   # Create a dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1("Country's GDP Percentile Ranking Over Time", style={"text_align":"centre", "color":"#503D36", "font-size":40}),
                                html.Div(["Select Country: ", dcc.Input(id="c1", value="Zimbabwe",type="text", style={"height":"50px", "font-size":35}),], 
                                style={"font-size":40}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id="scatter-plot", figure={})),#, figure={}
                                html.H4('A Ranking of 1 means that your selected GDP Per Capita is in the top 1% and a rating of 99 is in the bottom 1%',
                                       style={'text_align':'left','color':'red', 'text-indent': '100px'})


                               ])


# add callback decorator
@app.callback(Output(component_id="scatter-plot", component_property="figure"),
               Input(component_id="c1", component_property="value"))

# Add computation to callback function and return graph
def get_graph(entered_country):
    # Make Text in the country column lower case to make entered_country case insensitive
    w['country'] = w['country'].str.lower()

    # Select data based on the entered year
    w['pcgdp']= w["GDP"]/w["Population"]
    w['Ranking'] = w["pcgdp"].groupby(w['year']).rank(pct=True,ascending=False)*100
    
    #extract specific country's data and make text lowercase to make it case insensitive with str.lower
    df =  w[w['country']== str.lower(entered_country)]
    df

    scatter_data = df

    # 
    fig = px.line(scatter_data, x="year", y="Ranking", title="GDP Per Capita Percentile Ranking"
                   ,labels={"year":'Year',"Ranking":"Per Capita GDP Percentile Ranking"})
    return fig

# Run the app
if __name__ == '__main__':

#Use a port number other than 8050
    app.run_server(port=3012)


# In[ ]:




