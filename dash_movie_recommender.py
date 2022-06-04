#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 14:56:12 2022

@author: chenzhiyi
"""

import dash_bootstrap_components as dbc
import pandas as pd
import requests
from dash import Dash, html, dcc, dash_table, Input, Output, State

import pickle
from os.path import exists

from load_data import load_data
from get_content import get_content
g = get_content()
rat = load_data.rating()
rat5 = rat.loc[rat["rating"] == 5.0]
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

heading = html.H1('Dash Movie Recommender', className='bg-primary text-white p-2')


#def load_movie_dataframe(path='movie_full.pkl'):
#    file_exists = exists(path)
#    if file_exists:
#        file = open(path, 'rb')
#        movie_full_ = pickle.load(file)
#        file.close()
#        return movie_full_
#    else:
#        file = open(path, 'wb')
#        movie_full_ = load_data.full_movie()
#        pickle.dump(movie_full_, file)
#        file.close()
#        return movie_full_

#movie_full = load_movie_dataframe()
#dff = pd.DataFrame(columns=['title', 'rating', 'genres', 'movieId', 'tmdbId'])
content = html.Div(
    [
         dbc.Row(
             [
                 dbc.Col(
                     dbc.Button("Search", id='search-val', color="primary", className = "me-1", n_clicks=0),
                     ),
                 dbc.Col(
                     dbc.Input(id='filtering', value = '', type = 'text', placeholder="Search by titles, genres, or tags"),
                     ),
                 ],
             align='center'
             ),
         dbc.Row(
             [
                 dbc.Col(
                     dbc.Carousel(id="carousel-placeholder",
                                  items=[],
                                  controls=True,
                                  indicators = True,
                                  className = "carousel-fade"), width=3,
                     ),
                 #dbc.Col(
                 #   dash_table.DataTable(
                 #       id='movie-table',
                 #       style_table={'overflowY': 'auto'},
                 #       data=dff.to_dict(orient='records'),
                 #       columns=[{'id': c, 'name': c} for c in dff.columns],
                 #       style_cell=dict(textAlign='left'),
                 #       editable=False,
                 #       filter_action="native",
                 #       sort_action="native",
                 #       column_selectable="single",
                 #       row_deletable=False,
                 #       page_action="native",
                 #       page_current=0,
                 #       page_size=12,
                 #       export_format="csv",
                 #   ), width=6
                #),
            ]
        ),
    ],
  )
             
                 
   
app.layout = dbc.Container(children=[heading, content])

@app.callback(
    Output('carousel-placeholder', 'items'),  
    #Output('movie-table', 'data'),          
    [Input('search-val', 'n_clicks'),
     State('filtering', 'value')]
    )

def searching(n_clicks, value):
    ratsmp = rat5.sample(20) # randomly sample movies
    general = ratsmp["movieId"].values.tolist()
    movies = []
    
    if n_clicks == 0: # before any user input
        #### randomly show 10 movies with 5.0 ratings
        for movieId in general:
            movie_information = g.load_content(movieId)
            carousel = { # carousel content
                'key': general.index(movieId), # movie index as the key
                'src': movie_information.get("image"), # image to be displayed
                'header': movie_information.get("title"), # movie title
                'caption': movie_information.get("rating"), # movie rating
            }
            movies.append(carousel)
        return movies
    elif n_clicks > 0: # when user has clicked the button
        category = get_content.get_category(value) # get category
        search_id = get_content.create_content(category, value) # get movie ids that match
        search_10 = get_content.get_rating(search_id)
        for movie_id in search_10:
            movie_information = g.load_content(movie_id)
            carousel = { # carousel content
                'key': search_10.index(movie_id), # movie index as the key
                'src': movie_information.get("image"), # image to be displayed
                'header': movie_information.get("title"), # movie title
                'caption': movie_information.get("rating"), # movie rating
            }
            movies.append(carousel)
        return movies
    
    

if __name__ == '__main__':
    app.run_server(debug=True)
    