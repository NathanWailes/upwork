import csv
import os

full_set_of_artist_names = set()
for filename in os.listdir('csvs'):
    if filename.endswith('.csv'):
        with open(os.path.join('csvs', filename), 'r') as infile:
            reader = csv.DictReader(infile)
            artist_names = {record['artist'] for record in reader}
            full_set_of_artist_names.update(artist_names)

with open('seen_artists.txt', 'w') as outfile:
    for name in sorted(full_set_of_artist_names):
        outfile.write(name + '\n')
