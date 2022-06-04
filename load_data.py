import pandas as pd



class load_data:
    @classmethod
    def rating(self):
        rating = pd.read_csv("ratings.csv")
        rating = rating.groupby('movieId', as_index=False).mean().round(2)
        return rating
    @classmethod
    def link(self):
        link = pd.read_csv("links.csv", dtype={'imdbId': str, 'tmdbId': str})
        #link['tmbdId'] = link['tmbdId'].astype(str)
        #link['imbdId'] = link['imbdId'].astype(str)
        link['tmdbId'] = link['tmdbId'].fillna(0.0).astype(int)
        return link
    @classmethod
    def movies(self):
        movies = pd.read_csv("movies.csv")
        #genres = movies['genres'].str.split('|', expand=True)
        movies[['genre_0', 'genre_1', 'genre_2', 'genre_3', 'genre_4', 'genre_5', 'genre_6', 'genre_7', 'genre_8', 'genre_9']] = movies['genres'].str.split('|', expand=True)
        movies = movies.drop(['genres'], axis = 1)
        return movies
    @classmethod
    def tags(self):
        tags = pd.read_csv("tags.csv")
        tags = tags.drop(['userId', 'timestamp'], axis = 1)
        tags = tags.sort_values(by=['movieId'])
        return tags
    @classmethod
    def full_movie(self):
        movies = pd.read_csv("movies.csv")
        rating = pd.read_csv("ratings.csv")
        rating = rating.groupby('movieId', as_index=False).mean().round(2)
        movies_rating = pd.merge(movies, rating, how = 'left', on=['movieId'])
        link = pd.read_csv("links.csv", dtype={'imdbId': str, 'tmdbId': str})
        link['tmbdId'] = link['tmbdId'].astype(str)
        link['imbdId'] = link['imbdId'].astype(str)
        movies_rating_link = pd.merge(movies_rating, link, how = 'left', on = ['movieId'])
        tags = pd.read_csv("tags.csv")
        full_movie = pd.merge(movies_rating_link, tags, how='left', on=['movieId'])
        full_movie = full_movie.groupby(['title', 'tag'], as_index=False).max()
        full_movie.to_csv('movie_full.csv')
        return full_movie
    
