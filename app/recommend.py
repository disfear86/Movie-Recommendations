import pandas as pd

ratings = pd.read_csv('../data/ratings.csv').dropna()


def above_four(df, id):
    "Retrieve movies rated >= 4 stars by user"
    r = df.loc[df['user_id'] == id]
    r4 = r.loc[r['rating'] >= 4]
    return r4


r = above_four(ratings, 1)
#r45 = r.loc[r['rating'] >= 4]
print len(r)
