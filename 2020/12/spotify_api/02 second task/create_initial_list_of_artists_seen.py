import csv
import os


def main():
    full_set_of_artist_names_across_every_playlist = _create_artists_seen_file_for_each_playlist()
    _create_combined_artists_seen_file(full_set_of_artist_names_across_every_playlist)


def _create_artists_seen_file_for_each_playlist():
    playlist_names_and_ids = _get_playlist_names_and_ids()
    full_set_of_artist_names_across_every_playlist = set()

    for playlist_name_and_id in playlist_names_and_ids:
        full_set_of_artist_names_for_this_playlist = _get_full_set_of_artist_names_for_playlist(playlist_name_and_id)

        path_to_seen_artists = os.path.join('playlist_results', playlist_name_and_id['name'], 'seen_artists.txt')
        with open(path_to_seen_artists, 'w') as outfile:
            outfile.write("\n".join(sorted(full_set_of_artist_names_for_this_playlist)))



        full_set_of_artist_names_across_every_playlist.update(full_set_of_artist_names_for_this_playlist)
    return full_set_of_artist_names_across_every_playlist


def _get_playlist_names_and_ids():
    with open('playlists.csv', 'r') as input_file:
        reader = csv.DictReader(input_file)
        playlist_names_and_ids = [row for row in reader]
    return playlist_names_and_ids


def _get_full_set_of_artist_names_for_playlist(playlist_name_and_id):
    full_set_of_artist_names_for_this_playlist = set()
    path_to_csvs = os.path.join('playlist_results', playlist_name_and_id['name'], 'csvs')
    for filename in os.listdir(path_to_csvs):
        if filename.endswith('.csv'):
            with open(os.path.join(path_to_csvs, filename), 'r') as infile:
                reader = csv.DictReader(infile)
                artist_names = {record['artist'] for record in reader}
                full_set_of_artist_names_for_this_playlist.update(artist_names)
    return full_set_of_artist_names_for_this_playlist


def _create_combined_artists_seen_file(full_set_of_artist_names_across_every_playlist):
    path_to_main_results_directory = 'main_results'
    if not os.path.exists(path_to_main_results_directory):
        os.makedirs(path_to_main_results_directory)
    path_to_seen_artists = os.path.join(path_to_main_results_directory, 'seen_artists.txt')
    with open(path_to_seen_artists, 'w') as outfile:
        outfile.write("\n".join(sorted(full_set_of_artist_names_across_every_playlist)))


if __name__ == '__main__':
    main()
