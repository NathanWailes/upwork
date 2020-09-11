import csv
import os
from datetime import datetime

new_csv_filename = 'playlist_%s.csv' % datetime.today().strftime('%m-%d-%Y')
with open(new_csv_filename, 'r') as infile:
    reader = csv.DictReader(infile)
    artist_names_in_the_new_csv = {record['artist'] for record in reader}

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

output_filename = 'playlist_results_%s.csv' % datetime.today().strftime('%m-%d-%Y')
output_filepath = os.path.join('results', output_filename)
if not os.path.exists('results'):
    os.makedirs('results')
with open(output_filepath, 'w') as outfile:
    outfile.write('artist\n')
    for name in sorted(new_names):
        outfile.write(name + '\n')
