"""
The idea here is this:

Suppose we guess that the word "kill" was in the text, and we "dragged" that word across the entire ciphertext, such that
as the word was "dragged" to a new position, the symbols at that position would be assigned to represent those plaintext
letters of the alphabet. If we did this, then we could see which at position(s) having the word "kill" popped up two or
more letters later in the text that were positioned relative to each other such that they could produce the word "kill"
again. We could then return the position (or top N positions) that maximizes the number of future occurrences.

Doing this with the 408 works.

"""




