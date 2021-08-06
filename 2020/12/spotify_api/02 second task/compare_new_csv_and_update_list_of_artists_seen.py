import csv
import os
from collections import defaultdict
from datetime import datetime


def main():
    seen_artists_across_all_playlists = _get_seen_artists()
    new_names_across_all_playlists = defaultdict(list)
    artist_to_row_across_all_playlists = dict()

    with open('playlists.csv', 'r') as input_file:
        reader = csv.DictReader(input_file)
        playlist_names_and_ids = [row for row in reader]

    for playlist_name_and_id in playlist_names_and_ids:
        filename = '%s_%s.csv' % (playlist_name_and_id['name'], datetime.today().strftime('%m-%d-%Y'))
        csv_path = os.path.join('playlist_results', playlist_name_and_id['name'], 'csvs', filename)
        with open(csv_path, 'r') as infile:
            reader = csv.DictReader(infile)
            artists_to_rows = {row['artist']: row for row in reader}
            artist_names_in_the_new_csv = {row['artist'] for row in artists_to_rows.values()}

            for artist_name in artists_to_rows.keys():
                if artist_name not in artist_to_row_across_all_playlists:
                    artist_to_row_across_all_playlists[artist_name] = artists_to_rows[artist_name]

        seen_artist_names = _get_seen_artists(playlist_name_and_id['name'])

        new_artist_names = artist_names_in_the_new_csv.difference(seen_artist_names)
        print(new_artist_names)
        if new_artist_names:
            seen_artist_names.update(new_artist_names)

            _write_seen_artists(seen_artist_names, playlist_name_and_id['name'])

            for artist_name in new_artist_names:
                if artist_name not in seen_artists_across_all_playlists:
                    seen_artists_across_all_playlists.add(artist_name)
                    new_names_across_all_playlists[artist_name].append(playlist_name_and_id['name'])
        _write_output_file(new_artist_names, artists_to_rows, playlist_name_and_id['name'])

    _write_seen_artists(seen_artists_across_all_playlists)
    _write_output_file(new_names_across_all_playlists.keys(), artist_to_row_across_all_playlists, artist_to_playlists=new_names_across_all_playlists)


def _get_seen_artists(playlist_name=None):
    if playlist_name is not None:
        path_to_seen_artists_file = os.path.join('playlist_results',
                                            playlist_name,
                                            'seen_artists.txt')
    else:
        path_to_seen_artists_file = os.path.join('main_results',
                                            'seen_artists.txt')
    seen_artist_names = set()
    if os.path.exists(path_to_seen_artists_file):
        with open(path_to_seen_artists_file, 'r') as infile:
            seen_artist_names = {name.strip() for name in infile.readlines()}
    return seen_artist_names


def _write_seen_artists(seen_artist_names, playlist_name=None):
    if playlist_name is not None:
        path_to_seen_artists_file = os.path.join('playlist_results',
                                            playlist_name,
                                            'seen_artists.txt')
    else:
        path_to_seen_artists_file = os.path.join('main_results',
                                            'seen_artists.txt')

    with open(path_to_seen_artists_file, 'w') as outfile:
        for name in sorted(seen_artist_names):
            outfile.write(name + '\n')


def _write_output_file(new_names, artists_to_rows, playlist_name=None, artist_to_playlists=None):
    if playlist_name is not None:
        output_directory = os.path.join('playlist_results', playlist_name, 'results')
    else:
        output_directory = os.path.join('main_results', 'results')

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_filename = 'new_music_friday_results_%s.csv' % datetime.today().strftime('%m-%d-%Y')
    output_filepath = os.path.join(output_directory, output_filename)

    with open(output_filepath, 'w', newline='') as outfile:
        fieldnames = ['artist', 'artist_profile_url']
        if artist_to_playlists is not None:
            fieldnames.append('playlists_appeared_in')
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        new_artists_data = [{'artist': artists_to_rows[artist]['artist'],
                             'artist_profile_url': artists_to_rows[artist]['artist_profile_url']}
                            for artist in new_names]
        if artist_to_playlists is not None:
            for artist_dict in new_artists_data:
                artist_dict['playlists_appeared_in'] = artist_to_playlists[artist_dict['artist']]
        writer.writerows(new_artists_data)


if __name__ == '__main__':
    main()
