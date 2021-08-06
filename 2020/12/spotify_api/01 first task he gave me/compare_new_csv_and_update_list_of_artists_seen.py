import csv
import os
from datetime import datetime

filename = 'new_music_friday_%s.csv' % datetime.today().strftime('%m-%d-%Y')
new_csv_filename = 'new_music_friday_%s.csv' % datetime.today().strftime('%m-%d-%Y')
csv_path = os.path.join('csvs', filename)
with open(csv_path, 'r') as infile:
    reader = csv.DictReader(infile)
    artists_to_rows = {row['artist']: row for row in reader}
    artist_names_in_the_new_csv = {row['artist'] for row in artists_to_rows.values()}

seen_artist_names = set()
if os.path.exists('seen_artists.txt'):
    with open('seen_artists.txt', 'r') as infile:
        seen_artist_names = {name.strip() for name in infile.readlines()}

new_names = artist_names_in_the_new_csv.difference(seen_artist_names)
print(new_names)
if new_names:
    seen_artist_names.update(new_names)
    with open('seen_artists.txt', 'w') as outfile:
        for name in sorted(seen_artist_names):
            outfile.write(name + '\n')

output_filename = 'new_music_friday_results_%s.csv' % datetime.today().strftime('%m-%d-%Y')
output_filepath = os.path.join('results', output_filename)
if not os.path.exists('results'):
    os.makedirs('results')
with open(output_filepath, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['artist', 'artist_profile_url'])
    writer.writeheader()
    new_artists_data = [{'artist': artists_to_rows[artist]['artist'],
                         'artist_profile_url': artists_to_rows[artist]['artist_profile_url']}
                        for artist in new_names]
    writer.writerows(new_artists_data)
