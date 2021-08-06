import os
from datetime import datetime

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

client_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def main():
    playlist = sp.playlist('37i9dQZF1DX4JAvHpjipBk')
    output_rows = []
    for item in playlist['tracks']['items']:
        output_rows.append({
            'name': item['track']['name'],
            'artist': item['track']['artists'][0]['name'],
            'artist_profile_url': item['track']['artists'][0]['external_urls']['spotify']
        })

    # create dataset
    df = pd.DataFrame(output_rows, columns=['name', 'artist', 'artist_profile_url'])
    filename = 'new_music_friday_%s.csv' % datetime.today().strftime('%m-%d-%Y')
    output_csv_path = os.path.join('csvs', filename)
    df.to_csv(output_csv_path, sep=',')


if __name__ == '__main__':
    main()
