
# How to use the program

1. Look for the exe that says "dons_requested_program.exe" and run that, and a window should pop up that
shows hits.
1. A "settings.ini" file should get created in the same folder the first time you run the program, and
you can open it up to make changes to how the script runs.
1. Hits are saved to a file in that folder called "hits.csv". You can change the path in the
settings.ini file.

# Viewing the plaintext hits

- You can view the plaintext solutions in a nice way by using the two tools below:

## Cipher Explorer

- URL: http://zodiackillerciphers.com/cipher-explorer/
- Once there, click "Edit" --> "Edit cipher text", select all of the existing text, and paste in the
plaintext you see in the hit you're interested in (in hits.csv).

## CryptoScope

- URL: http://zodiackillerciphers.com/webtoy/stats.html
- Once there, click on the ciphertext and just paste in the plaintext from the hit you're interested in.



# Making changes to the settings


## SearchOptions

- `check_only_a_quadrant` - This will allow you to have the program search for hits only within a certain
quadrant of the 340 cipher. Set it to "True" or "Yes" or "y" for it to be enabled.
- `quadrant_to_check` - If `check_only_a_quadrant` is set to `True`, then the program will look for an
integer in this setting (`quadrant_to_check`) and only look for hits in that quadrant.

## Output

- To change the output's datetime format, change the "Output --> datetime_format" setting in settings.ini.
  - Use [this website](http://strftime.org/) to see the different formats available.
  - You must use two percent-signs instead of the usual 1 because of the way the program works that
  takes in the .ini file.  (So, "%%Y" instead of "%Y".)