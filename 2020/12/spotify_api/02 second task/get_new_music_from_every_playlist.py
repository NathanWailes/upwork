import configparser
import csv
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
    with open('playlists.csv', 'r') as input_file:
        reader = csv.DictReader(input_file)
        playlist_names_and_ids = [row for row in reader]

    a_folder_was_renamed = False
    for playlist_name_and_id in playlist_names_and_ids:
        print('Now handling playlist: %s' % playlist_name_and_id['name'])
        playlist = sp.playlist(playlist_name_and_id['spotify_id'])
        output_rows = []
        for item in playlist['tracks']['items']:
            if item and isinstance(item, dict) and 'track' in item.keys() and 'artists' in item['track']:
                output_rows.append({
                    'name': item['track']['name'],
                    'artist': item['track']['artists'][0]['name'],
                    'artist_profile_url': item['track']['artists'][0]['external_urls']['spotify']
                })
        the_folder_was_renamed = _rename_playlist_folder_if_necessary(playlist['name'], playlist_name_and_id['name'])
        if the_folder_was_renamed:
            playlist_name_and_id['name'] = playlist['name']
            a_folder_was_renamed = True

        df = pd.DataFrame(output_rows, columns=['name', 'artist', 'artist_profile_url'])
        filename = '%s_%s.csv' % (playlist['name'], datetime.today().strftime('%m-%d-%Y'))

        path_to_output_file = os.path.join('playlist_results', playlist['name'], 'csvs', filename)

        if not os.path.exists(os.path.dirname(path_to_output_file)):
            os.makedirs(os.path.dirname(path_to_output_file))

        df.to_csv(path_to_output_file, sep=',')

    if a_folder_was_renamed:
        with open('playlists.csv', 'w', newline='') as output_file:
            field_names = ['name', 'spotify_id']
            writer = csv.DictWriter(output_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(playlist_names_and_ids)


def _rename_playlist_folder_if_necessary(desired_playlist_name, existing_playlist_name):
    path_to_desired_playlist_folder_name = os.path.join('playlist_results', desired_playlist_name)
    if not os.path.exists(path_to_desired_playlist_folder_name):
        if os.path.exists(os.path.join('playlist_results', existing_playlist_name)):
            path_to_old_playlist_folder_name = os.path.join('playlist_results', existing_playlist_name)
            os.rename(path_to_old_playlist_folder_name, path_to_desired_playlist_folder_name)
            return True
    return False


if __name__ == '__main__':
    main()
