import pandas as pd

r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('data/u.data', sep='\t',
                        names=r_cols, usecols=range(3))

m_cols = ['movie_id', 'title']
movies = pd.read_csv('data/u.item', sep='|', names=m_cols, usecols=range(2))

movie_ratings = pd.merge(ratings, movies)
movie_ratings.to_csv('app/movie_ratings.csv')
movie_ratings = movie_ratings.pivot_table(index=['user_id'],
                                            columns=['movie_id'],
                                            values=['rating'])


# restack and write to file
r = movie_ratings.stack()
r.to_csv('data/ratings.csv')
