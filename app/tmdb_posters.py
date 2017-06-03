import requests

api_key = '<tmdb api key>'


def get_poster(imdb_id):
    base_url = "http://image.tmdb.org/t/p/"

    img_url = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
    r = requests.get(img_url.format(key=api_key, imdbid=imdb_id))
    api_response = r.json()

    img_path = api_response['posters'][0]['file_path']
    return base_url + 'w185' + img_path
