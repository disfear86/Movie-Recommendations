import pandas as pd

r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('data/u.data', sep='\t',
                        names=r_cols, usecols=range(3))

m_cols = ['movie_id', 'title']
movies = pd.read_csv('data/u.item', sep='|', names=m_cols, usecols=range(2))

movie_ratings = pd.merge(movies, ratings)
movie_ratings.to_csv('app/movie_ratings.csv')
