import pandas as pd
import numpy as np

ratings = pd.read_csv('../data/ratings.csv')

'''
def above_four(df, id):
    "Retrieve movies rated >= 4 stars by user"
    r = df.loc[df['user_id'] == id]
    r4 = r.loc[r['rating'] >= 4]
    return r4


r = above_four(ratings, 1)

movie_ratings = ratings.pivot_table(index=['user_id'],
                                    columns=['movie_id'],
                                    values='rating')
'''


def find_similar(df, id):
    movie1 = movie_ratings[id]

    similar = movie_ratings.corrwith(movie1).dropna()

    stats = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})
    above_100 = stats['rating']['size'] > 100

    df = stats[above_100].join(pd.DataFrame(similar, columns=['similarity']))
    df = df.ix[2:]
    df = df.sort_values(['similarity'], ascending=False)
    df = df[:5]
    print df['similarity'][id]
