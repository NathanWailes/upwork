"""
The purpose of this file is to just make it easy to see what a pure brute-force solution looks like.

There are two tricky things such a solution needs to do:
  1. It needs to be able to generate all of the different possible assignments of symbols to letters, and preferably do
     it in such a way that it isn't accidentally repeating work (e.g. generating the same possibility twice).
  2. It needs to be able to evaluate / score each of the different possible assignments of symbols to letters in such a
     way that the highest-scored possible assignment is the *real* assignment.

"""
from utils import get_ciphertext



def decode_with_simple_brute_force(path_to_file_with_ciphertext):
    data = get_ciphertext(path_to_file_with_ciphertext)
    symbols = set()
    for row in data:
        symbols = symbols.union(set(row))

    symbols_to_their_decoded_value = dict()



    while len(symbols_to_their_decoded_value.keys()) < symbols:
        symbols_to_choose_a_value_for = symbols.difference(set(symbols_to_their_decoded_value.keys()))

        # Not every letter in the alphabet appeared in 408, so you can't check to see if every letter in the
        # alphabet has received a symbol. And even if you could do that, you'd still be left with the question of
        # what to do with the symbols that had not been assigned a decoded value after all of the letters of the
        # alphabet had already received symbols assigned to them.


if __name__ == '__main__':
    path_to_file_with_ciphertext = './encoded_ciphertexts/408.txt'
    decode_with_simple_brute_force(path_to_file_with_ciphertext)
