import csv
import random
import time
import os

from datetime import datetime

from utils import alphabet_capitalized, z340, z340_symbols, z340_first_quadrant, z340_second_quadrant, z340_third_quadrant, z340_fourth_quadrant
import configparser


def main(path_to_settings_file='settings.ini'):
    attempt_number = 0

    if not os.path.isfile(path_to_settings_file):
        create_settings_file(path_to_settings_file)
    settings = get_settings(path_to_settings_file)

    datetime_start = datetime.now()

    while True:
        datetime_end = datetime.now()
        minutes_since_last_check_of_settings = (datetime_end - datetime_start).total_seconds() / 60.0
        if float(settings['General']['check_settings_file_every_x_minutes']) <= minutes_since_last_check_of_settings:
            settings = get_settings(path_to_settings_file)
            minutes_since_last_check_of_settings = 0

        attempt_number += 1

        cipher_symbols = z340_symbols

        if settings['SearchOptions']['check_only_a_quadrant'].lower() in ('true', 'yes', 'y'):
            if settings['SearchOptions']['quadrant_to_check'] == '1':
                ciphertext = list("".join(z340_first_quadrant))
            elif settings['SearchOptions']['quadrant_to_check'] == '2':
                ciphertext = list("".join(z340_second_quadrant))
            elif settings['SearchOptions']['quadrant_to_check'] == '3':
                ciphertext = list("".join(z340_third_quadrant))
            elif settings['SearchOptions']['quadrant_to_check'] == '4':
                ciphertext = list("".join(z340_fourth_quadrant))
        else:
            ciphertext = list("".join(z340))

        zodiac_symbols_to_normal_letters = {symbol: [] for symbol in cipher_symbols}

        for symbol in cipher_symbols:
            zodiac_symbols_to_normal_letters[symbol] = random.choice(alphabet_capitalized)

        # All letters in the normal alphabet now have a random number of zodiac symbols assigned to them.

        # For every letter of the normal alphabet, replace the symbols assigned to it in the cipher.
        translated_ciphertext_on_one_line = "".join([zodiac_symbols_to_normal_letters[symbol] for symbol in ciphertext])

        #  Look for pay dirt..
        #  The misspellings here are intentional, taken from known examples of the Zodiac killer's previous writings. A
        #  match on any of these words would be a hint of a significantly stronger "signal" among the noise.
        signal_words = settings['SearchOptions']['words_to_look_for'].split(',')

        signal_words_found = []

        for signal_word in signal_words:
            if signal_word in translated_ciphertext_on_one_line.lower():
                signal_words_found.append(signal_word)

        if attempt_number % int(settings['ConsoleOutput']['print_attempt_number_every_x_attempts']) == 0:
            print("Processing: Pass %s" % str(attempt_number))

        if len(signal_words_found) >= int(settings['Hits']['number_of_keyword_matches_required']):
            translated_ciphertext_separated_by_newlines = "\n".join(["".join([zodiac_symbols_to_normal_letters[symbol] for symbol in line]) for line in z340])
            output_hit(ciphertext, translated_ciphertext_separated_by_newlines, signal_words_found, attempt_number, settings)


def create_settings_file(path_to_settings_file):
    config = configparser.ConfigParser(interpolation=None)
    config['General'] = {'check_settings_file_every_x_minutes': '0.5'}
    config['SearchOptions'] = {'check_only_a_quadrant': 'False',
                            'quadrant_to_check': '3',
                            'words_to_look_for': ",".join(["children", "others", "around",
                                "shall", "about", "people", "would", "missed", "police", "because", "thing", "there",
                                "could", "rather", "light", "school", "vallejo", "useing", "triger", "howers", "cerous",
                                "meannie", "killed", "victom", "speaking", "lyeing", "slaves", "afterlife", "zodiac",
                                "intersting", "idenity", "woeman", "untill"])}
    config['ConsoleOutput'] = {'print_attempt_number_every_x_attempts': '50000'}
    config['Hits'] = {'number_of_keyword_matches_required': '1'}
    config['Output'] = {'path': './hits.csv',
                        'datetime_format': "%%Y-%%m-%%d %%H:%%M:%%S"}

    with open(path_to_settings_file, 'w') as configfile:
        config.write(configfile)


def get_settings(path_to_settings_file):
    config = configparser.ConfigParser()

    while True:
        try:
            config.read(path_to_settings_file)
        except WindowsError:
            print("Unable to read from the settings file. It's probably open in another program. Close it.")
            time.sleep(5)
        else:
            break
    return config


def output_hit(ciphertext, translated_cipher_text, signal_words_found, attempt_number, settings):
    print("\n\n\nMATCH FOUND:\n%s\n(Count: %s, %s), cycle %s\n\n" % (translated_cipher_text, len(signal_words_found),
                                                                   ",".join(signal_words_found), attempt_number))

    output_path = settings['Output']['path']
    if not os.path.isfile(output_path):
        is_a_new_file = True
    else:
        is_a_new_file = False

    while True:
        try:
            with open(output_path, "a", newline="") as outfile:
                writer = csv.writer(outfile)
                if is_a_new_file:
                    writer.writerow(["attempt_number", "datetime", "number_of_signal_words_found",
                                     "signal_words_found", "plaintext"])
                datetime_string = datetime.now().strftime(settings['Output']['datetime_format'])
                writer.writerow([attempt_number, datetime_string,
                                 len(signal_words_found), "|".join(signal_words_found), translated_cipher_text])
        except WindowsError:
            print("Unable to write to the CSV file. It's probably open in another program. Close it.")
            time.sleep(5)
        else:
            break


if __name__ == "__main__":
    path_to_settings_file = 'settings.ini'
    main(path_to_settings_file)
