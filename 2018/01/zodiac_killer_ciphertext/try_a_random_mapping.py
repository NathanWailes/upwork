"""
Based on the z340crack originally written in Perl by Bowie J. Poag, found here: http://www.perlmonks.org/?node_id=910936

"""
import csv
import json
import random

import os

from utils import alphabet

attempt_number = 0

while True:
    attempt_number += 1

    cipher_symbols = list("=>_-;:']{}&#%123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    ciphertext = list("YB91TMKOT2M]X3BF4FB5678R1]5V2=XXE>VUZ4-X9_]#M%G&XF:WBI;LOSHT'6;9{YOB}-C5ZO8AIK7X")

    zodiac_symbols_to_normal_letters = {symbol: [] for symbol in cipher_symbols}

    for symbol in cipher_symbols:
        zodiac_symbols_to_normal_letters[symbol] = random.choice(alphabet)

    # All letters in the normal alphabet now have a random number of zodiac symbols assigned to them.

    # For every letter of the normal alphabet, replace the symbols assigned to it in the cipher.
    translated_cipher_text = "".join([zodiac_symbols_to_normal_letters[symbol] for symbol in ciphertext])

    #  Look for pay dirt..
    #  The misspellings here are intentional, taken from known examples of the Zodiac killer's previous writings. A
    #  match on any of these words would be a hint of a significantly stronger "signal" among the noise.
    signal_words = ["children", "others", "around", "shall", "about", "people", "would", "missed", "police", "because",
                    "thing", "there", "could", "rather", "light", "school", "vallejo", "useing", "triger", "howers",
                    "cerous", "meannie", "killed", "victom", "speaking", "lyeing", "slaves", "afterlife", "zodiac",
                    "intersting", "idenity", "woeman", "untill"]

    signal_words_found = []

    for signal_word in signal_words:
        if signal_word in translated_cipher_text:
            signal_words_found.append(signal_word)

    if attempt_number % 100000 == 0:
        print("Processing: Pass %s" % str(attempt_number))

    if len(signal_words_found) >= 1:
        print("\n\n\nMATCH FOUND: %s (Count: %s, %s), cycle %s\n\n" % (ciphertext, len(signal_words_found),
                                                                       ",".join(signal_words_found), attempt_number))

        output_path = "/tmp/zodiac.csv"
        if not os.path.isfile(output_path):
            is_a_new_file = True
        else:
            is_a_new_file = False

        with open(output_path, "a", newline="") as outfile:
            writer = csv.writer(outfile)
            if is_a_new_file:
                writer.writerow(["attempt_number", "number_of_signal_words_found", "signal_words_found",
                                 "mapping_of_symbols_to_letters_used"])
            writer.writerow([attempt_number, len(signal_words_found), "|".join(signal_words_found),
                             json.dumps(zodiac_symbols_to_normal_letters)])
