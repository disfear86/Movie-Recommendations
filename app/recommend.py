import pandas as pd
import numpy as np

# read csv
ratings = pd.read_csv('app/movie_ratings.csv')


def find_similar(df, id):
    """Find similarities between specific movie and dataset"""
    # user movie
    movie = df[id]

    # correlate with dataset
    similar = df.corrwith(movie).dropna()

    # group by movie id, get each movie total and mean
    stats = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})
    # keep movies with over 200 user ratings to eliminate false results
    above_100 = stats['rating']['size'] > 200

    # join the two dataframes on similarity
    df = stats[above_100].join(pd.DataFrame(similar, columns=['similarity']))
    # drop initial user movie from results
    df = df[df.similarity != float(1)]
    df = df.sort_values(['similarity'], ascending=False)
    return df
