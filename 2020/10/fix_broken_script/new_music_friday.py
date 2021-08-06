import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

client_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def main():
    ids = get_track_ids('Spotify', '37i9dQZF1DX4JAvHpjipBk')
    print(len(ids))
    print(ids)

    # loop over track ids
    tracks = []
    for i in range(len(ids)):
        time.sleep(.5)
        track = get_track_features(ids[i])
        tracks.append(track)

    # create dataset
    df = pd.DataFrame(tracks, columns=['name', 'artist'])
    df.to_csv("new_music_friday.csv", sep=',')


def get_track_ids(user, playlist_id):
    ids = []
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        if track:
            ids.append(track['id'])
    return ids


def get_track_features(id):
    meta = sp.track(id)

    # meta
    name = meta['name']
    artist = meta['album']['artists'][0]['name']

    track = [name, artist]
    return track


if __name__ == '__main__':
    main()
