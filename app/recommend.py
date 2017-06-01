import pandas as pd
import numpy as np

ratings = pd.read_csv('app/movie_ratings.csv')


def find_similar(df, id):
    movie = df[id]

    similar = df.corrwith(movie).dropna()

    stats = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})
    above_100 = stats['rating']['size'] > 100

    df = stats[above_100].join(pd.DataFrame(similar, columns=['similarity']))
    df = df[df.similarity != float(1)]
    df = df.sort_values(['similarity'], ascending=False)
    return df.head()
