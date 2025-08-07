import requests
import os
from urllib.parse import quote

OMDB_API_KEY = os.getenv('OMDB_API_KEY')


def fetch_movie_data(title):
    try:
        response = requests.get(
            f'http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={quote(title)}'
        )
        response.raise_for_status()
        data = response.json()

        if data.get('Response') == 'True':
            return {
                'name': data.get('Title', ''),
                'director': data.get('Director', 'N/A'),
                'year': int(data.get('Year', '0').split('–')[0]),
                'poster_url': data.get('Poster', '')
            }
        return None
    except requests.RequestException as e:
        print(f"Error fetching movie data: {e}")
        return None