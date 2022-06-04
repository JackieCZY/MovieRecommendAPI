#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 11:07:43 2022

@author: chenzhiyi
"""


import pandas as pd
from load_data import load_data
import requests

class get_content: #search by genre, tag, and title of the movie
    movies = load_data.movies()
    link = load_data.link()
    rating = load_data.rating()
    tags = load_data.tags()
    
    def get_category(value):
        genres = get_content.movies.drop(["movieId", "title"], axis = 1)
        title = get_content.movies[["movieId", "title"]]
        
        if value in genres.values:
           
            return "genre"
        elif title['title'].str.contains(value, case = False).any():
            
            return "title"
        else:
        
            return "tag"
        
    def get_rating(movie_id):
        rating=get_content.rating
        list1 = []
        for i in movie_id:
            list1.append(rating.loc[rating['movieId'] == i])
        data = pd.concat(list1)
        data = data.sort_values(by=["rating"], ascending = False)
        top10 = data.iloc[:10]
        top10 = top10["movieId"].values.tolist()
        return top10

    def create_content(search_cat, match_val):
        if search_cat == "genre":
            movies=get_content.movies
            
            movie_data = movies.loc[movies.values == match_val]
            movie_id = movie_data['movieId'].values.tolist()
            return movie_id
        elif search_cat == "tag":
            tags = get_content.movies
            tags_data = tags.loc[tags['tag'].str.contains(match_val, case = False)]
            movie_id = tags_data['movieId'].values.tolist()
            return movie_id
        elif search_cat == "title":
            title = get_content.movies
            title_data = title.loc[title['title'].str.contains(match_val, case = False)]
            movie_id = title_data['movieId'].values.tolist()
            return movie_id
        else: return None
        
    def create_image(movie_id):
        movie_db_api_key = "120ce5dc845c1d9da58d8f81ae5ba367"
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={movie_db_api_key}&language'
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            poster_path = data['poster_path']
            full_path = 'https://via.placeholder.com/150' if not poster_path \
                else f'https://image.tmdb.org/t/p/w500/{poster_path}'
        else:
            full_path = 'https://via.placeholder.com/150'
        return full_path
    
    def load_content(self, movie_id):
        #movies_to_display = []
        movie_information = {}
        movie = get_content.movies.loc[get_content.movies['movieId']==movie_id]
        title = movie['title'].values[0]
        movie_con = movie.drop(['movieId', 'title'], axis = 1)
        genre_list = []
    
        for (columnName, columnData) in movie_con.iteritems():
            if columnData.values[0] != None:
                genre_list.append(columnData.values[0])
                continue
            else: break
        
        tmdbid = get_content.link.loc[get_content.link['movieId'] == movie_id]
        tmdbid = tmdbid['tmdbId'].values[0]
        image = get_content.create_image(tmdbid)
        
        rating= get_content.rating.loc[get_content.rating['movieId'] == movie_id]
        rating = rating['rating'].values[0]
        
        tags = get_content.tags.loc[get_content.tags['movieId']==movie_id]
        tag = tags['tag'].to_list()
        
        movie_information.update({
            'movieId':movie_id,
            'title': title,
            'genres': genre_list,
            'image': image,
            'rating':rating,
            'tag': tag,
            })
        return movie_information


def main():
    movie_id= 1
    g= get_content()
    g.load_content(movie_id)

if __name__ == "__main__":
    main()         