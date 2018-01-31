"""
The idea here is this:

Background idea:
Suppose we guess that the word "kill" was in the text, and we "dragged" that word across the entire ciphertext, such that
as the word was "dragged" to a new position, the symbols at that position would be assigned to represent those plaintext
letters of the alphabet. If we did this, then we could see which at position(s) having the word "kill" also made words
show up in the rest of the text.

However, there's a problem with that: because the word "kill" only uses three or four ciphertext symbols (depending on
whether the letter "l" is encoded as two different symbols or one repeated symbol), the only way that this method would
produce a recognizable word later in the passage is if

"""