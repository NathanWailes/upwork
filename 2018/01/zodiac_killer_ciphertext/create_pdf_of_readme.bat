REM - You'll need to install pandoc and MiKTeX as described here: https://pandoc.org/installing.html
REM - When I ran the command the first time MiKTeX asked me to install a bunch of other minor packages.

pandoc -V geometry:margin=1in README.md -o decode-zodiac-340-ciphertext.pdf -margin=1in --pdf-engine=xelatex