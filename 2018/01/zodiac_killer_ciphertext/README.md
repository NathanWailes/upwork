# decode-zodiac-ciphertexts
Attempt to decode ciphertexts written by the Zodiac Killer. In particular, try to decode the 340 ciphertext.

# Table of contents
- [Background on the murders](#background-on-the-murders)
- [Background on prime suspect Arthur Leigh Allen](#background-on-prime-suspect-arthur-leigh-allen)
  * [Summary of the evidence that he is the Zodiac](#summary-of-the-evidence-that-he-is-the-zodiac)
  * [Summary of evidence that he is not the Zodiac](#summary-of-evidence-that-he-is-not-the-zodiac)
- [Background on the letters](#background-on-the-letters)
- [Background on the ciphertexts](#background-on-the-ciphertexts)
  * [General](#general)
  * [The 408](#the-408)
  * [The 340](#the-340)
  * [The 13 / "My name is"](#the-13----my-name-is-)
- [Others' attempts at solving the 340](#others--attempts-at-solving-the-340)
  * [Compilations](#compilations)
  * [Misc people](#misc-people)
    + [Attempts listed on the ZodiacKillerCiphers wiki's page on research papers](#attempts-listed-on-the-zodiackillerciphers-wiki-s-page-on-research-papers)
  * [Cryptocrack](#cryptocrack)
  * [zodiacdecoder (University of North Texas)](#zodiacdecoder--university-of-north-texas-)
  * [zkdecrypto - Brax Cisco, Wesley Hopper, Michael Eaton](#zkdecrypto---brax-cisco--wesley-hopper--michael-eaton)
  * [Craig Bauer](#craig-bauer)
  * [Dan Olson (FBI)](#dan-olson--fbi-)
  * [Nick Pelling](#nick-pelling)
  * [USC (Sujith Ravi, Kevin Knight)](#usc--sujith-ravi--kevin-knight-)
  * [David Oranchak](#david-oranchak)
- [Communities / websites of particular interest](#communities---websites-of-particular-interest)
- [Online tools / resources](#online-tools---resources)
  * [Tools](#tools)
  * [Compilations](#compilations-1)
  * [Individual tools](#individual-tools)
  * [Resources](#resources)
  * [Research papers](#research-papers)
    + [Compilations](#compilations-2)
  * [Individual papers](#individual-papers)
    + [Others](#others)
- [Clues](#clues)
- [Interesting features of the 408](#interesting-features-of-the-408)
- [How the 408 was solved](#how-the-408-was-solved)
- [Differences between the 340 from the 408](#differences-between-the-340-from-the-408)
- [Interesting features of the 340](#interesting-features-of-the-340)
- [Predictions](#predictions)
- [Why the 340 seems to be using a homophonic cipher](#why-the-340-seems-to-be-using-a-homophonic-cipher)
- [What kind of encryption the 340 is almost certainly *not* using](#what-kind-of-encryption-the-340-is-almost-certainly--not--using)
- [Assumptions](#assumptions)
- [Ideas](#ideas)
  * [Cribs](#cribs)
  * [Pruning](#pruning)
  * [Scoring function](#scoring-function)
  * [Frequency analysis](#frequency-analysis)
- [Misc](#misc)
- [Questions](#questions)
- [Terms / Concepts](#terms---concepts)
  * [Methods of encryption](#methods-of-encryption)
  * [Methods of Cryptanalysis](#methods-of-cryptanalysis)
- [Sources](#sources)
  * [The evaluation function](#the-evaluation-function)
- [Notable researchers](#notable-researchers)

# Background on the murders

# Background on prime suspect Arthur Leigh Allen
- [Undated - ZodiacCipers.com - Arthur Leigh Allen](http://www.zodiacciphers.com/arthur-leigh-allen.html)
- [Undated - ZodiacKillerFacts - The truth about the prime suspect in David Fincher's ZODIAC](http://zodiackillerfacts.com/zodiac-theories/the-accused-the-accusers/allen-primed-suspect/allen-the-movie/)
- [1991 - Excerpt from an interview with Arthur Leigh Allen](https://www.youtube.com/watch?v=IivYpSsv3Eo)
- [1991 - A Current Affair (TV show) - Branded a Butcher](https://www.youtube.com/watch?v=z17Tsjnm5xQ)
- [2008 - His Name Was Arthur Leigh Allen (Documentary)](https://www.youtube.com/watch?v=uY_tqjdnDVk)
  - 37:00 - In 1990 the detective who took over the Zodiac case took a photo of Arthur Leigh Allen to
  Michael Mageau, a survivor from the Blue Rock Springs attack, as part of a line-up, and "after about 20 seconds"
  Michael identified Arthur Leigh Allen as the person who shot him.
  - 38.20:
    > With that I was able to write a search warrant that was ultimately signed by a judge. And we searched the
    > house, and we found hidden in the basement: bombs--completed pipe bombs--formulas for making fuel oil bombs as the
    > Zodiac had described in one of his letters where he was gonna blow up school buses with little children in them, the
    > same type of bombs--formulas for making that stuff.
  - 39:05:
    > We were gonna charge him with possession of the explosives and the killing at Blue Rock Springs. We actually had a
    > meeting set up to go to the district attorney's office and about a week before the meeting I got a call from a
    > police officer named Terry Barren(sp?). I was at home and he asked me if I was still looking at Arthur Leigh Allen
    > as the responsible in the killing at Blue Rock Springs of Darlene Ferrin?", and I said "Yeah". And being kind of
    > a smart aleck, the police officer said to me, "Well, I'm standing in his house and he's laying on the floor." And
    > I said, "What do you mean?", and he says, "Yeah, he's laying on the floor, but he's dead".  They weren't even
    > gonna have an autopsy because he was under doctor's care. I insisted, and they did do an autopsy and he died of
    > a heart attack.

## Summary of the evidence that he is the Zodiac

- A somewhat-close friend of his came forward to police and reported many, many details of conversations and activities that he
participated in with Leigh Allen that pointed strongly to Leigh Allen being the Zodiac.
- He lived an 8 minute walk from where the first phone call to police was made.
- He apparently had the same shoe size as that found at the upstate murder scene.
- He had somewhat the same build as that described by living witnesses, of being overweight.
- In a search of his home after his death, police apparently found pistols, pipe bombs, and formulas for the types of bombs described
by the Zodiac in letters.

## Summary of evidence that he is not the Zodiac

- A woman who received a call from the Zodiac said that Leigh Allen's voice did not match the voice she heard.
- A police officer who seems to have seen the Zodiac after the Stine murder in SF says that the photo of Leigh Allen that he
saw showed a man who was "about 100 lbs" heavier than the man the officer saw. Also, the officer reported the man to be about 5'8",
but Leigh Allen is at least 6' tall.

# Background on the letters

- [The Quester Files - Zodiac: Poison Pen Pal](http://www.thequesterfiles.com/poison_pen_pal___the_zodiac_ki.html)

# Background on the ciphertexts

## General

- [Security.StackExchange - Why haven't (most of) the Zodiac Killer's letters been decrypted?](https://security.stackexchange.com/questions/122607/why-havent-most-of-the-zodiac-killers-letters-been-decrypted)

## The 408

- [An image of the ciphertext with the decoded plaintext above each line of ciphertext](http://mk-zodiac.com/images/cipher%2007-31-69.jpg)
- [ZodiacCiphers.com - The Complete 408 Cipher](http://www.zodiacciphers.com/complete-408-cipher.html)
- [2012.12.20 - ZodiacKillerCiphers - Detailed analysis of the 408 solution](http://www.zodiackillerciphers.com/?p=233)

## The 340

- [Undated - ZodiacCiphers.com - The 340 Cipher](http://www.zodiacciphers.com/340-cipher.html)

## The 13 / "My name is"

- [An image of the letter](http://cdn.history.com/sites/2/2017/11/5_-San-Francisco-Chronicle-My-Name-Is-letter-April-20-1970-COLOR.jpg)

# Others' attempts at solving the 340

- [2017.05.17 - ZodiacKillerSite Forums - Is anyone attempting a 'brute force' type of solution?](http://zodiackillersite.com/viewtopic.php?f=81&t=3397)
  - David Oranchak explains the problem with trying to solve with a brute-force approach.

## Compilations

- [ZodiacKillerCiphers - Discredited or inconclusive solution attempts](http://zodiackillerciphers.com/wiki/index.php?title=Main_Page#Discredited_or_inconclusive_solution_attempts)

## Misc people

- [Jos F. Kirps - Cracking the Zodiac Killer's 340 Cipher](https://web.archive.org/web/20160304171422/http://www.kirps.com:80/web/main/resources/various/zodiac340/)
  - Referenced in the "HEURISTIC SEARCH CRYPTANALYSIS OF THE ZODIAC 340 CIPHER" paper.
  - > To perform my brute force attack I wrote a small program (a shell script in fact) that sequentially tests keywords
   often used by the Zodiac in various positions and then runs a 1000 word dictionary to see if the chosen
   combinations allow a maximum of common words to be placed, followed by a ranking algorithm to highlight the most
   promising results. I ran about 250 million tests on the cipher, without any results.

### Attempts listed on the ZodiacKillerCiphers wiki's page on research papers

- [2007 - Dao, Thang. Analysis of the zodiac 340-cipher. Diss. San Jose State University, 2007.](http://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=4566&context=etd_theses&sei-redir=1)
- [2009 - Basavaraju, Pallavi Kanagalakatte. "Heuristic Search Cryptanalysis of the Zodiac 340 Cipher." (2009)](http://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=1055&context=etd_projects)
  - This was for a master's degree.
  - The guy's best solution for the 408 only revealed 25% of the characters, such that it was still basically
  unrecognizable as being English.
  - The paper looks easy to understand.
- [2010 - Raddum, Håvard, and Marek Sýs. "The zodiac killer ciphers." Tatra Mountains Mathematical Publications 45.1 (2010): 75-91.](http://tatra.mat.savba.sk/Full/45/12ra-sy.pdf)
- [2011 - Dhavare, Amrapali. Efficient attacks on homophonic substitution ciphers. Diss. San Jose State University, 2011.](http://www.cs.sjsu.edu/faculty/stamp/students/dhavare_amrapali.pdf)
- [2013 - Berg-Kirkpatrick, Taylor, and Dan Klein. "Decipherment with a Million Random Restarts." EMNLP. 2013.](http://www.cs.berkeley.edu/~tberg/papers/emnlp2013.pdf)
  - [Wikipedia - Expectation-maximization algorithm](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm)
  - > **We make two arguments supporting the claim that Zodiac 340 is not a homophonic cipher with row-major reading
  order**: the first is statistical, based on the success rate of attempts to crack similar synthetic ciphers; the
  second is qualitative, comparing distributions of local optimum likelihoods.
  - > If Zodiac 340 is a homophonic cipher should we expect to crack it? In order to answer this question we generate
  100 more ciphers in the same way we generated Synth 340. We use 10K random restarts to attack each cipher, and
  compute accuracies by best model score. The average accuracy across these 100 ciphers was 75% and the minimum
  accuracy was 36%. All but two of the ciphers were deciphered with more than 51% accuracy, which is usually
  sufficient for a human to identify a decode as partially correct.
  - > We attempted to crack Zodiac 340 using a rowmajor reading order and 1M random restarts, but the decode with
  best model score was nonsensical. This outcome would be unlikely if Zodiac 340 were like our synthetic ciphers,
  so Zodiac 340 is probably not a homophonic cipher with a row-major order. Of course, it could be a homophonic
  cipher with a different reading order. It could also be the case that a large number of salt tokens were
  inserted, or that some other assumption is incorrect.

## Cryptocrack

- [Google Sites - Cryptocrack - A cipher-solving program](https://sites.google.com/site/cryptocrackprogram/)

## zodiacdecoder (University of North Texas)

- [Google Code - zodiacdecoder](https://code.google.com/archive/p/zodiacdecoder/)class
  - Email: joeyliechty@gmail.com

## zkdecrypto - Brax Cisco, Wesley Hopper, Michael Eaton

- [Google Code - zkdecrypto](https://code.google.com/archive/p/zkdecrypto/)
- [2008.02.08 - Oranchak.com - New cipher-solving program available](http://www.oranchak.com/?p=389)
- [2012.07.19 - ZodiacKillerCiphers - Comment by David](http://www.zodiackillerciphers.com/?p=58)
  - > Yes, some folks have tried other languages. zkdecrypto, a cipher-solving utility, is able to solve the
  > 408-character cipher (which contains misspellings), as well as many other test ciphers that intentionally
  > include misspellings. So, if the 340-character cipher has normal English plaintext with some misspellings,
  > the program would probably have found a solution. It also includes language statistics for French, German,
  > Italian, and Spanish, and still no solutions have been found.
- [2012.09.18 - ZodiacKillerCiphers - zkdecrypto: lite edition](http://www.zodiackillerciphers.com/?p=197)
  - > the current version of zkdecrypto can only work on one cipher at a time, and you have to click around in
  the user interface to kick off its search for solutions. Dan needed a way to simplify and speed up the
  process, so he hacked together a command-line version called zkdecrypto-lite.
  - > When I run the above example on the solved 408 cipher, the program takes only a second and a half to
  find the (mostly) correct solution!

## Craig Bauer

- [2017.12.14 - CipherMysteries - Craig Bauer's Z340 cipher "crack"](http://ciphermysteries.com/2017/12/14/hunt-zodiac-killer-season-finale-craig-bauers-z340-cipher-crack)
  - "this is just about as bad as it gets."
  - "Sorry, but from what I can see, this Z340 ‘solution’ isn’t even close to being close."
- [2017.12.17 - ZodiakKillerCiphers - Craig Bauer's solution to Z340](http://www.zodiackillerciphers.com/?p=758)
  - David doesn't comment on it, instead linking to others' articles on it. It seems certain that he does
  not agree that it is the correct decoding.

## Dan Olson (FBI)

- [YouTube - MysteryQuest Season 1 Episode 3 - San Francisco Slaughter](https://www.youtube.com/watch?v=uG2M3NOyCB4&t=7m42s)
  - "He and his team have spent a great deal of time studying the Zodiac's ciphers."
  - > Olson: The Zodiac case is the most fascinating code case in American history because there are three ciphers
  that remained unsolved, first of all. Secondly, the crime remains unsolved, so there's always the hope that breaking
  one of the ciphers may finally reveal who the killer is.
  - > Olson: This is the Zodiac 340 message; the message that's been on our top-10 list for forty years.
  - > There are indications that this cipher may actually be split in two, with the first ten lines consituting the
  first part, and the next ten lines for the second part.
  - > Olson believes there is a pattern that contains a message in six of these lines that is revealed when they are
  placed side-by-side.
  - > Olson: We can duplicate this message and place the duplicate right next to it. Now, if we shift that duplicate
  up, we've essentially taken line 1 and line 11 and made a continuous stream across. We believe a message is
  contained in these three lines. The remaining lines may also contain a message, or may also be fake. But these
  three lines, we have high confidence that a message exists in there. It's our hope that revealing this new theory
  to the public may be the inspiration and provide that missing piece that someone out there needs to help solve
  this cipher.
- [Letter from Dan Olson to Tom Voigt](http://zodiackillerciphers.com/wiki/index.php?title=FBI_analysis_from_Dan_Olson)
  - > I dont have a graphic to share but here are more details you can post instead: Statistics for repeated
  characters for each line of text show a distinct higher randomness with the lines we've discussed (1-3 and
  11-13). The higher randomness may be due in part or whole to greater care by the writer to not repeat characters
  on these lines. This indicates homophonic substitution. The opposite is true for lines 4, 10, 14, 17 and 18, these
  lines have many repeats. Additionally, there is far greater randomness for rows versus columns. This rules out any
  form of columnar or diagnal transpositions (a big step forward).
  - > These same statistical tests were done on Z408. The results suggest that 340 is similar to 408 except for the
  bogus rows: overall randomness of 408 is .48, 340 is .50. Row randomness of 408 is .22, 340 is .19. Column
  randomness of 408 is .48, 340 is .68. By way of comparison, row and column randomness should be near identical if
  the 340 does not contain any message, or if there is a message that is evenly scrambled.
  - > My name is Dan Olson. I am the Unit Chief of the Cryptanalysis and Racketeering Records Unit that was featured
  on MysteryQuest episode. I wanted to pass to you the reasons behind the Z340 theories I presented on the episode
  last night. I believe these are important discoveries that may assist skilled codebreakers find a solution.
    - > Statistical tests indicate a higher level of randomness by row, than by column. This indicates that the
    cipher is written horizontally and rules out any transposition patterns that are not strictly horizontal.
    - > Lines 1-3 and 11-13 contain a distinct higher level of randomness than lines 4-6 and 14-16. This appears to
     be intentional and indicates that lines 1-3 and 11-13 contain valid ciphertext whereas lines 4-6 and 14-16 may
     be fake.
      - NW: But in the 408, there were only six lines that contained the higher level of randomness, but the entire
      message (except for the last line) contained valid ciphertext.
    - > Because of the vertical symmetry of the statistical observations, the message may have been written, then
    split into two equal size parts and placed top over bottom.

## Nick Pelling

- [2011.09.13 - CipherMysteries - Thoughts on the Zodiac Killer Z408 and Z340 ciphers..](http://ciphermysteries.com/2011/09/13/thoughts-on-the-zodiac-killer-z408-and-z340-ciphers)
  - > Even though it was originally a crib which helped to crack it, Z408 has other weaknesses, most notably
  the way it sequentially cycles through homophones
  - > Moving on to the uncracked Z340 cipher, I have to say that what strikes me most is the difference between
  its top half (lines 1-10) and its bottom half (lines 11-20). It turns out that back in 2009, FBI codebreaker
  Dan Olson pointed out to Tom at zodiackiller.com that lines 1-3 and 11-13 contained very few repeats: other
  people have wondered whether this points to some kind of block-level transposition going on. Me, I suspect
  there’s a far stronger inference to be made: that even though they share nearly all the same character shapes,
  I’m pretty sure that the top and bottom halves of Z340 use completely different cipher letter assignments, and
  hence may well need to be cracked independently. Further, I suspect that the Zodiac may well have intended to
  send them out separately (Z408 was sent as three independent sections), but (for some reason) ended up sending
  them both as a single cipher.
  - > "Right now, I think that a constructive first big step would be to search for statistically significant
  homophone sequences in the top and bottom halves of Z340, because we can be reasonably sure that the most
  frequent letters will probably have four or more homophones, just as with the Z408 cipher."
  - There's a lot of back-and-forth in the comments.

## USC (Sujith Ravi, Kevin Knight)

- These are the guys who decoded the Copiale Cipher.
- [Bayesian inference for Zodiac and other homophonic ciphers](http://www.aclweb.org/anthology/P/P11/P11-1025.pdf)
  - Linked to by David Oranchak [here](http://www.zodiackillerciphers.com/?p=220)
  - TODO: Read this.

## David Oranchak

- [ZodiacKillerCiphers Wiki](http://zodiackillerciphers.com/wiki/index.php?title=Main_Page)
  - [List of all pages on the wiki](http://zodiackillerciphers.com/wiki/index.php?title=Special:AllPages)
  - Below I've listed the interesting pages:
  - [Brute-force search for homophone sequences](http://zodiackillerciphers.com/wiki/index.php?title=Brute_force_search_for_homophone_sequences#Results_for_340_cipher)
  - [Catalog of repeating fragments](http://zodiackillerciphers.com/wiki/index.php?title=Catalog_of_repeating_fragments)
  - [Cipher legitimacy](http://zodiackillerciphers.com/wiki/index.php?title=Cipher_Legitimacy)
  - [Comparison of character repetition rates](http://zodiackillerciphers.com/wiki/index.php?title=Comparison_of_character_repetition_rates)
  - [Corpus search results - A search for words and phrases shared between Zodiac's writings and a large corpus](http://zodiackillerciphers.com/wiki/index.php?title=Corpus_search_results)
  - [Encyclopedia of observations](http://zodiackillerciphers.com/wiki/index.php?title=Encyclopedia_of_observations)
  - [Hypothesis testing](http://zodiackillerciphers.com/wiki/index.php?title=Hypothesis_Testing)
  - [Pivots](http://zodiackillerciphers.com/wiki/index.php?title=Pivots)
  - [Quadrant analysis](http://zodiackillerciphers.com/wiki/index.php?title=Quadrant_analysis)
  - [Research papers](http://zodiackillerciphers.com/wiki/index.php?title=Research_papers)
  - [Zodiac's repeated text](http://zodiackillerciphers.com/wiki/index.php?title=Zodiac%27s_repeated_text)
    - NW: For some reason David included the three identical letters to the different newspapers with his
    first cryptogram as separate documents, so a lot of the matches are just matching those documents against each
    other.
  - [Substring ranking](http://zodiackillerciphers.com/wiki/index.php?title=Substring_ranking)
  - 408-specific:
    - [Word frequency analysis (408)](http://zodiackillerciphers.com/wiki/index.php?title=Word_frequency_analysis_(408))
    - [Letter frequency analysis (408)](http://zodiackillerciphers.com/wiki/index.php?title=Letter_frequency_analysis_(408))
  - 340-specific:
    - [Quadrant analysis (340)](http://zodiackillerciphers.com/wiki/index.php?title=Quadrant_analysis_(340))
- [2007.11.14 - Oranchak.com - Can evolution reveal a killer’s mind?](http://www.oranchak.com/?p=367)
  - > In my free time (what little there is), I’ve been running experiments using ECJ, a Java-based evolutionary
  computing framework. So far, **my focus has been on trying to get the algorithm to solve Zodiac’s 408-character
  cipher, which has a known solution. Using a dictionary-oriented approach, the algorithm was able to find the
  correct solution using a limited 400-word dictionary.** Now I am trying to improve this by adding more words to
  the dictionary used by the algorithm. The basic idea is to get this test case working well before attempting to
  have it solve the really difficult 340-character cipher. This has proven to be very difficult, because the search
  space (number of possible solutions) is extremely large, and there is exactly one correct solution. The needle is
  tiny, and the haystack is vast. Evolutionary computing methods tend to be better-suited for finding really good
  solutions, rather than the one best solution, so this approach is quite challenging (if not flawed).
  I’m glad that many people are still working on this problem; it would be nice to finally find a solution. Still,
  there is still a strong possibility that there is no solution, and the cipher is just gibberish designed to keep
  people unnecessarily busy. If so, then the Zodiac killer succeeded beyond his wildest dreams.
- [2008.03.20 - Oranchak.com - The joys of breeding](http://www.oranchak.com/?p=396)
  - > We present a dictionary-based attack using a genetic algorithm that encodes solutions as plaintext word
  placements subjected to constraints imposed by the cipher symbols. For a test case to develop the technique,
  we use a famous cipher (with a known solution) created by the Zodiac serial killer. We present several
  successful decryption attempts using moderate dictionary sizes of up to ﬁve hundred words. Attempts are ongoing
  to increase the robustness of this technique by making it work with larger dictionaries and a variety of test
  ciphers.
- [2008.07.10 - Oranchak.com - GECCO @ Hotlanta](http://www.oranchak.com/?p=440)
  - He has a link to his poster, which is very interesting.
  - > We use a dictionary-based attack: Palce words in one section of cipher to impose constraints on other sections
  of cipher. Correct placements produce partial word decodings in other sections of cipher text. Dictionary is
  indexed by constraints for fast lookup.
  - > Reduce the search space by concentrating attack on a small section of ciphertext.
  - > Evolutionary approach:
    >  - Genome encodes attacks as (word, position) tuples. Words are drawn from a fixed dictionary.
    >  - Infeasible encodings are immediately rejected.
    >  - Each individual starts with a single tuple. Subsequent generations add more tuples via crossover and
         mutation.
  - > Conflicting decodings arise when we look up partial word matches. We seek a maximual set of words that produces
  no conflicts. This is a vertex cover problem. To find a factor-2 approximation of vertex cover quickly, we find
  maximal matchings in the conflict graphs.
  - > Results: For dictionary sizes up to 1600 words, algorithm was able to find correct decodings for the
  408-character cipher. 340-character cipher remains unsolved. We are working on making our technique more robust for
  future attacks.
- [2012.06.02 - Zodiac's favorite words](http://www.zodiackillerciphers.com/?p=22)
- [2012.06.03 - Is the 340-character cipher real?](http://www.zodiackillerciphers.com/?p=38)
- [2012.06.24 - Throw the book at him! (Part 1)](http://www.zodiackillerciphers.com/?p=58)
- [2012.07.04 - Throw the book at him! (Part 2)](http://www.zodiackillerciphers.com/?p=86)
- [2012.08.09 - Throw the book at him! (Part 3)](http://www.zodiackillerciphers.com/?p=144)
- [2012.08.11 - Gutenberg addendum: Small ciphers](http://www.zodiackillerciphers.com/?p=152)
- [2012.08.12 - In his own words](http://www.zodiackillerciphers.com/?p=173)
- [2012.12.07 - Who is the 'Concerned Citizen'?](http://www.zodiackillerciphers.com/?p=224)
- [2012.12.20 - Detailed analysis of the original 408 solutions](http://www.zodiackillerciphers.com/?p=233)
- [2013.01.05 - Did Zodiac use Kahn's "Codebreakers" book?](http://www.zodiackillerciphers.com/?p=256)
- [2013.03.22 - Klaus Schmeh's book of famous unsolved codes](http://www.zodiackillerciphers.com/?p=307)
  - > Klaus describes the effect the Hardens’ success had on them. Reportedly, Bettye Harden had trouble dealing with
   all of the sudden attention and fame, and developed a manic-depressive personality disorder. Here are some of
   the other bits of info Klaus mentions:
    - > Donald Harden was asked to work on the 340-character cryptogram, but refused. However, Bettye “barricaded
    herself in her room for weeks” to try to solve it, but failed. The CIA and NSA also failed to crack the code.
    - > Robert Graysmith points out in his book “Zodiac” several cryptography books that were available at the time
    of the crimes: “The Codebreakers” by David Kahn, and “Codes and Ciphers” by John Laffin.
- [2013.03.25 - Are the ciphers prime-phobic?](http://www.zodiackillerciphers.com/?p=319)
  - Summary: the two most-common symbols in the 340's ciphertext land on primes far less likely than would be expected
  if their positions were decided by pure chance.
- [2013.07.31 - Attacking the 340 using genetic programming](http://www.zodiackillerciphers.com/?p=394)
- [2013.08.03 - Route patterns](http://www.zodiackillerciphers.com/?p=401)
- [2013.08.18 - Zodiac at the ACL 2013 conference](http://www.zodiackillerciphers.com/?p=448)
- [2013.09.15 - My name is...Sarah the Horse?](http://www.zodiackillerciphers.com/?p=467)
- [2013.09.20 - Mountain of evidence?](http://www.zodiackillerciphers.com/?p=485)
- [2013.09.21 - New Scientist](http://www.zodiackillerciphers.com/?p=490)
- [2013.10.03 - Try, try again](http://www.zodiackillerciphers.com/?p=504)
- [2014.12.26 - How to know that you haven't solved the Zodiac-340 cipher](http://www.zodiackillerciphers.com/?p=602)
- [2015.11.01 - The Zodiac ciphers -- What do we know, and when do we stop trying to solve them?](http://www.zodiackillerciphers.com/?p=629)
  - [Link to the YouTube video](https://www.youtube.com/watch?v=BV5R3TBMWJg)
  - 0:00 - 0:30 - Intro of who David is.
  - 0:35 - 1:12 - David explains what the Zodiac Cipher is and how he got interested in it.
  - 0:15 - Since I couldn't solve it, I started collecting information on the four ciphers Zodiac sent, to get a very
  clear understanding of what is already known about them.
  - 1:27 - The second question I want to explore is, "When can we stop trying to solve them?", and to address that I'm
  going to talk about a technique I came up with to rule out possibilities of how the 340 may have been enciphered.
  - 1:40 - Quick background on the Zodiac killer.
  - 2:30 - David introduces the four ciphertexts.
  - 3:04 - David discusses the 13-character ciphertext: when it came out, the 408 had already come out and been solved,
  and the 340 had come out several months previously and had not been solved. The 13 has quite a few repeated symbols.
  You can come up with a lot of possible names, and there's no way to distinguish a real solution from a fake one.
  - 3:59 - The 32-symbol "map" cipher has the same issue of many possible solutions. 29 of the 32 symbols only appear
  once, making it close to being a one-time pad.
  - 4:30 - Later he sent another letter with a hint, but there are still too many possible solutions.
  - 5:05 - For the 408, Zodiac split the message into three equal pieces and sent them to different newspapers,
  demanding that they publish the cryptogram, and the newspapers did so.
  - 5:17 - In less than a week a high school teacher and his wife decrypted the cryptograms.
  - 5:30 - The key they came up with breaks down at the end; there's a sequence of 18 symbols that's gibberish.
  - 5:44 - The cipher is a homophonic substitution cipher. There are multiple symbols to each letter to hide the letter
  frequencies.
  - 6:01 - The Hardens (who decoded the message) guessed that the word "kill" would show up in the message, and they
  were looking for patterns where the word would fit. <He shows an image of the 408 with the most-common bigrams
  highlighted.> And after guessing what these symbols stand for and replacing them in the entire message, you'll be on
  your way to recovering the entire message.
  - 6:35 - Regarding the 18 nonsense characters: in the letter that accompanied the cryptogram, the Zodiac said that the
  message would contain his identity. And so because the plaintext up until the last 18 characters doesn't reveal his
  identity, people speculated that his name might be in those last eighteen characters (NW: the plaintext clearly says
  that the Zodiac has no intention to reveal his identity.) And so people tried looking at anagrams of those characters.
  - 7:40 - Another explanation for the last eighteen characters is that the Zodiac just wanted to fill out the last
  section of ciphertext so that when he split it into three sections, it wouldn't give any hints about which section
  came last. So if you look at the bottom row, it looks like he may be copying letters from the same column but in
  rows further up. This happens with randomly-shuffled text, but what is especially interesting is that the sequence
  "QEHM" is perfectly preserved.
  - 8:25 - Zodiac was known to make numerous spelling errors in his letters, and the Hardens discovered similar
  misspellings in the plaintext of the cryptogram. What's interesting is that the "correct" symbols tend to resemble the
  symbols that were mistakenly used instead.
  - 9:20 - In homophonic substitution ciphers you can look for a pattern of a group of symbols that cycle, and that
  often indicates that the symbols all stand for the same plaintext letter. We see many patterns like this in the 408.
  - 10:00 - The 340 seems very similar to the 408. He removed a few symbols and added a bunch of new ones. By adding
  new symbols and providing a shorter ciphertext the Zodiac made the 340 far harder to solve.
  - 10:20 - We want to know what direction the message is written in. One way to do that is to look at how many symbols
  repeat in each row and how many repeat in each column. Because the creator of the ciphertext will tend to change the
  symbol used to represent a particular letter each time the letter shows up, you'll tend to see that the average
  duration between multiple occurrences of the same symbol will tend to be higher in the direction that the text is
  meant to be read. And what you see is that in the 408, there are actually six rows that have no repeating symbols,
  and in the 340 there are nine rows with no repeating symbols. So that would seem to support the idea that the 340 is
  meant to be read horizontally.
  - 11:14 - Dan had an idea: if you look at the 340, the first three lines of the ciphertext and the first three lines
  after the midpoint both have no repeating symbols. And so he speculated that maybe the ciphertext was originally
  written out with the top half and bottom half positioned next to each other horizontally, and then the "right half"
  was moved down below the "left half".
    - NW: That doesn't make sense to me, because that would seem to eliminate the pattern of no repeated symbols in the
    row.
  - 11:44 - Another example of sloppiness: the Zodiac first wrote a forward "K" on the 340, and then scratched it out
  and replaced it with a backwards "K".
  - 11:57 - Another way to investigate the reading direction of the message is to look at the repeated bigrams. In the
  408 there are quite a lot of repeated bigrams, and in the 340 there are not nearly so many, only 25. And if you do a
  random shuffle, you get on average about 20. If there was a message perfectly preserved in the 340 in the same reading
  direction as the 408, you'd probably see more repeating bigrams.
    - NW: What if the Zodiac was purposely trying to avoid repeating bigrams? Didn't the Hardens reveal that they'd used
    those to crack the first message? (Later: Yep, David makes that point the next minute or two.)
  - 12:37 - If you draw a line dividing the 340 in half (top and bottom), you'll see that the top half has many more
  repeating bigrams than the bottom half. So something in the encipherment is disturbing the repeating bigrams.
  - 12:57 - Now, looking at trigrams: the 408 has a lot of trigrams. The 340 shows two repeating trigrams, which does
  favor a horizontal repeating direction. So whatever is disturbing the bigram count doesn't seem to be disturbing the
  trigram count. So maybe what was happening was that the Zodiac was purposely trying to disguise the bigrams, but
  didn't think to worry about the trigram count.
  - 13:40 - Another interesting thing about the repeating trigrams is that the IOF repeats directly above the other one,
  just as the QEHM repeats directly above the previous one. So maybe the 340 has some kind of filler section.
  - 14:04 - There's another way to count bigrams: you can count bigrams where the two symbols are separated by one or
  more other symbols. At distance 1 (which we've already discussed), there are 25 repeated bigrams. At distance 19,
  there are 37 repeated bigrams. And at distance 14, reading right to left, there are forty repeated bigrams. Using
  random shuffles, the peak number you'd expect is only about 30.
  - 14:47 - We discussed earlier the ability to look for groups of symbols that cycle, and we can do this with the 340.
  There are two sets of two symbols in particular that show this pattern. Unfortunately shuffle tests show that it isn't
  that hard to come up with this behavior by chance. But there are other patterns like this in the ciphertext. "There
  seems to be a higher distribution of them in the 340 than there are in random ciphertexts."
  - 15:42 - There are these patterns I call "pivots" where you see the same pattern of symbols appear both horizontally
  and vertically, and meet at the same point. I did some calculations and saw that if the symbols were assigned
  randomly, there was a 1 in 50,000 chance that this kind of coincidence of letters would be preserved into the
  ciphertext. So this makes me wonder if this has something to do with how the ciphertext was put together.
  - 16:25 - Another pattern I call "the box corners" seem to indicate sections of the code. And two of them appear in
  the middle of an "O" and a "C" symbol.
  - 16:54 - People do word searches with the ciphertext. Most of them look meaningless, but the last one very much
  looks like the Zodiac is signing the ciphertext with his name.
  - 17:17 - Another interesting thing is happening with the odd and even positions in the ciphertext. I pulled all the
  odd symbols into one meta-ciphertext and all the even symbols into a different meta-ciphertext, and then counted the
  number of repeating bigrams, and there's a big discrepancy between them: there are very few repetitions in the odd
  positions, and very many in the even positions. If you do random trials, less than 1% show this wide of a spread
  between the odd and even positions.
  - 18:05 - So, when can we stop trying to solve this thing? 1) Obviously if someone solves it, or 2) if someone comes
  up with evidence that it was probably a hoax. Until then, let's try to find a solution. The way to do that is to try
  out different ideas for how it might be enciphered. I hadn't seen a robust way to go through these possibilities and
  rule them out, and so I thought one way to approach the issue was to generate a big pile of test ciphers that
  implement any particular hypothesis for how the 340's cipher works, and then try to solve those ciphertexts. If you
  can break those and not break the 340, then the 340's cipher is probably not the same as the one that created
  those cracked ciphers.
  - 18:59 - To start this process I started with the hypothesis that the 340 was created like the 408. I created a
  ciphertext generator: it goes through a big pile of books, takes random samlpes of length 340, etc. I use an algorithm
  to come up with a key that comes closest to generating a ciphertext that matches the 340 along several dimensions.
  - 20:35 - So here are some 340-like ciphers. You can see they have a lot of the same patterns: the weird pivots, the
  box-corner patterns, the pseudo-words including the Zodiac signatures, they have real underlying plaintext, they have
  the same bigram count as the real 340.
  - 21:15 - Why do this? As background: I've seen similar efforts that mimic the symbol distribution but none of the
  other qualities of the real 340. And the problem with that is that you never know if your code-breaking technique will
  be able to handle a ciphertext that has those special qualities that the 340 has.
  - 22:10 - He shows a slide with a few different hypotheses listed.
  - 22:15 - Possible future work: Knight/Nuhn were able to automatically distinguish between fifty different types of
  ciphers. I think these results can be improved with ensemble classifiers that correct the weaknesses of other
  classifiers. I wonder how a classifier would classify the 340 after having been trained on a large test set.
  - (Switches to questions. TODO: Finish this.)
- [2016.02.28 - Ciphers that resemble Zodiac's 340-character cryptogram](http://www.zodiackillerciphers.com/?p=637)
- [2017.09.08 - Hands on Z408](http://www.zodiackillerciphers.com/?p=662)
- [2017.09.28 - Criminal codes and ciphers](http://www.zodiackillerciphers.com/?p=666)
- [2017.10.19 - YouTube - The Unsolved Zodiac 340 Cipher: Features or Phantoms?](https://www.youtube.com/watch?v=rew8uLqCS2w)
  - 0:00 - 0:30 - Intro of who David is.
  - 0:30 - 1:40 - David gives a background on who the Zodiac was and what the ciphertexts are.
  - 1:40 - A lot of people have spotted potential clues, and what I'm interested in is knowing which are good clues and
  which are bad clues.
  - 3:00 - He gives an example. If a person suspects a particular individual is the Zodiac killer, they'll look for
  their name in the ciphertext.
  - 4:15 - There's another way to check for bad clues: one is the shuffle test. You rearrange the symbols from the
  ciphertext and then test the feature. So, for example, if you do the shuffle test for names, they pop up all over
  the place.
  - 4:50 - I call bad clues "phantoms".
  - 5:00 - "Features are things that may tell you things about how the cipher is constructed or may give you hints
  to what the underlying plaintext message may be."
  - 5:08 - The same thing with names is also seen with words: random shuffles will produce a pile of short, common
  words.
  - 5:38 - But in the lower-right we seem to see the word "Zodiac", and that does not show up in shuffle tests.
  - 6:20 - He gives the analogy of the blade of grass and the golf ball.
  - 7:10 - I came up with variations of Zodiac and still got odds of 1 in 30,000. But I didn't test for the word
  being written backwards, or diagonally
  - 7:45 - Someone found a pattern where a sequence of symbols that follows a pattern, and the same shape appears
  underneath, with the same symbols. But if you do the shuffle test, this shows up basically every time.
  - 8:25 - Let's look at some real features.
  - 8:26 - He shows the 408 ciphertext and its solution.
  - 8:57 - The couple that solved the ciphertext noticed patterns in the ciphertext.
  - 9:03 - They noticed doubled symbols and figured they stood for double letters in the plaintext. Double "l" is the
  most common doubled letter that appears in English, and so they (correctly) guessed that that's what the symbols
  stood for.
  - 9:33 - There's another pattern that's statistically significant, which is the repeating bigrams.
  - 9:54 - By making the correct guesses about this small set of symbols, they were able to recover about 20% of the
  plaintext.
  - 10:08 - Let's mark all the repeating bigrams in the 408. They cover about 43.87% of the ciphertext. If you do the
  shuffle test, you never see such a high number of repeating bigrams.
  - 11:04 - We can check the 340 for repeating bigrams, and what we find is that there are not as many. They only cover
  23.53% of the ciphertext.
  - 11:25 - If you come up with test messages that are very similar to the 340's statistics, you find that on average
  you'd have more repeating bigrams.
  - 11:32 - If you do a shuffle study, you find that 1 in 9 randomized ciphers has as many or more repeating bigrams
  as the 340.
  - 11:55 - Either there's not as many repeating bigrams in the plaintext message, or some aspect of the encipherment
  is hiding them.
  - 12:10 - There's a manipulation that you can do on the 340 that will cause more repeating bigrams to appear. You do a
  skip 19, where you rearrange the ciphertext by taking every 19th letter from the original ciphertext. If you do a
  shuffle test of this, you find about 1 in every 40,000 trials has this property.
  - 13:10 - There are other manipulations that make even more repeating bigrams appear, such as doing a horizontal flip
  of the original text and then doing a period 15.
  - 13:33 - So what does that tell us? Well, it's not the solution, but there's some mystery about where the repeating
  bigrams are.
  - 13:48 - Another thing we can look for in the 408 is repeating segments that may have symbols in between. These are
  statistically significant. The reason they appear is because the same word or pair of words is showing up multiple
  times in the plaintext.
  - 14:35 - If we look at the 340, we find a few of these. (He shows the three longest ones.)
  - 14:50 - Just as with bigrams, we can manipulate the ciphertext to make more of these appear.
    - Q from NW: Why doesn't he talk about what happens when these same manipulations are done on the 408?
  - 15:02 - Another potentially-interesting feature in the 340 are what I call "pivots", where a sequence of letters
  appears both horizontally and vertically and intersect. In 1 in 20,000 shuffles you'll see some pair of patterns
  like this.
  - 15:58 - The 408 is homophonic. We can look for patterns in those symbol assignments. For example, we can look for
  groups of letters that always appear in a cycle. That suggests that the author had a key and was tracking which
  symbol he'd used last time, so that he could use a different one this time. There's at least one very long group
  of characters that shows this pattern in the 408.
  - 16:50 - You can look for these cycles by just looking for pairs of symbols that show up in a repeating cycle, one
  after the other. In the 408, 'P' and 'U' show up one after the other. In the 340 there's a *perfect* sequence,
  backwards 'L' and 'M'.
  - 17:22 - But what we find is that while such cycling shows up in the 340, they're not as statistically unlikely as
  the ones that appear in the 408.
  - 17:35 - But just as with the earlier patterns, there are manipulations that will increase the amount of cycling that
  appears.
  - 17:45 - In the case of the 340, the cycles are improved if you swap two pairs of groups of lines.
  - 18:01 - A remaining difficulty is that the "successful" manipulations I've described each only maximizes one of the
  different features, and not the others. So what we'd really like is a manipulation that increases all of them.
  - 18:37 - A member of the American Cryptogram Association named Bart Wenmeckers(sp?) did a Kasisky exam, which involves
  looking for repeating patterns in the ciphertext, which is used to look for the key length of a polyalphabetic
  cipher. He just kept shifting the ciphertext forwards and seeing how many symbols coincided with the original
  ciphertext, and he found a peak of 19 coincidences when he shifted the ciphertext 78 positions forwards. It seems
  interesting, but I don't know what it means. A peak this high at any shift value will show up in about 1 in 100
  shuffles. One interesting this to me is that the shift of 78 is exactly double the distance of the two pivots I
  mentioned earlier.
  - 20:30 - There are interesting things happening with individual symbols. In the 408 there are six lines that have no
  repeating lines, whereas in the 408 there are 9 lines with no repeats.
  - 20:53 - In the 408, shuffle studies showed that one in 100 shuffles would have six or more lines with no repeats,
  but with the 340 you need to do millions of shuffles to get as many lines with no repeats as show up in the 340.
  - 21:17 - (NW: I didn't quite understand what he was trying to say here:) Typically with a homophonic system you'd
  expect to see some amount of this phenomonenon because the person encoding the message will tend to not use the same
  symbol for a particular character soon after using it. But it seems that there may have been some process used by
  the person encoding the text that led to an even-greater amount of this phenomenon.
    - Q from NW: What are the symbols in the 408 that are *preventing* the ciphertext from having more lines without
    repeats, and is it the case that those symbols are preventing rows with no repeats because 1) the author didn't
    choose enough symbols for a commonly-occurring letter of the alphabet, or is it instead 2) the author wasn't
    cycling through the options for particular letters in such a way that would prevent the same symbol from appearing
    on the same line two or more times?
    - NW: Why would he think that there's some manipulation going on to make this effect more dramatic when we know
    that this cipher uses far more symbols than the 408, and we know that this phenomenon is a function (in part) of
    the number of symbols used for each letter (especially the most-common letters)?
  - 21:46 - Another interesting thing is that there is a set of symbols that only appear in the top six lines of the
  ciphertext and the bottom four lines of the ciphertex, with none in the middle 10 lines.
  - 22:10 - He concludes his talk. He runs ZodiacKillerCiphers.com and can be reached at
  doranchak@gmail.com and @doranchak on Twitter. There's a section on his website called "Encyclopedia of
  Observations" where he's collecting all the "phantoms" and "features" that he's come across, as well as links to
  different studies. There's also a forum at ZodiacKillerSite.com where people are collaborating on trying to decode
  the ciphertext.
  - 23:00 - Craig Bauer talks about his own quest to decode
  - 24:09 - Q for David: where are the actual Zodiac letters now? A: Not sure, I think the SFPD and Vallejo PD have them.
  - 24:37 - Point for David: Two days ago there was a fictional show that revealed who the Zodiac killer was, so he's
  still very much in the public's mind.
  - 25:00 - Q for Craig.
  - 27:12 - Q for David: In the 408, towards the end the decoding seems to break down. What's up with that?
    - A: When the text was first sent out it was sent in three pieces, and some suspect that he added those filler
    characters to make it less obvious what the order was for the different pieces. Others suspect that he's got
    another message in that last 18 characters.
  - 27:53 - Q for David: Has there been any attempt to use those in solving the 340?
    - A: Yeah, so, in the 408 people noticed that the last 18 characters seem to have been pulled down from the
    characters that appeared above them, and there has been some attempt to look for the same kind of pattern in the
    340, looking at multiple
  - 28:24 - Q for Craig
  - 29:30 - Q for David: Could it be that the 340 was not authored by the same person as the 408?
    - A: I think the investigators concluded that they were written by the same person by handwriting analysis and
    possibly some other physical evidence. The ciphertexts came with accompanying plaintext letters that were not
    written in block text.
  - 30:27 - Q for David: What are the odds that the second message was sent to be unbreakable?
    - A: Oh yeah, that's a definite possibility. Another possibility is that he messed up the encipherment; that
    happened with BTK, and there was another case like that too.
  - 31:14 - Qs for Craigs
  - 32:30 - Q for David: How many different symbols are there in the two ciphers?
    - A: 54 in the 408, 63 in teh 340. Interestingly, other ciphertexts that are of the same length as the 340, with
    ciphers containing as many unique symbols as the 340, are easily broken using traditional methods. Because the
    first one was solved, and it was publicized, and it was solved by a regular-Joe high school teacher, and there
    were articles in which the teacher explained how they solved it, the author of the cipher may have read those
    articles and deliberately changed the second cipher to avoid those methods of decoding.
      - NW: Follow up with David about this. I'd like to know the examples.
  - 34:20 - Q for David: How do you know that the existing proposed solutions for the 340 are not correct?
    - A: By comparing them to the solution for the 408. With the 408, the solution is fairly simple once you know it:
    you just use the key to decode each symbol. The solutions for the 340 tend to be a lot more convoluted, and you
    can use the same method used to arrive at their solution to come up with alternate solutions.
  - 35:23 - Q: Is there any reason for this continued research?
    - A: We still occasionally see these kinds of historical messages popping up every so often. For me it's just been
    an excuse to do more programming.
  - 37:23 - Q: Is there anything like a program that can take a random encrypted message and try different things until
  it decodes it?
    - A from David: There's nothing like that now but we seem to be moving in that direction, because you can train a
    neural network to recognize different ciphers.
- [2017.10.22 - Criminology (Podcast)](http://www.zodiackillerciphers.com/?p=670)
- [2017.12.20 - "Behind True Crime" podcast](http://www.zodiackillerciphers.com/?p=767)

# Communities / websites of particular interest

- [ZodiakKillerCiphers.com](http://www.zodiackillerciphers.com/)
- [ZodiacKillerSite - Cipher subforum](http://www.zodiackillersite.com/viewforum.php?f=81)
  - TODO: Go through the posts here.
- [ZodiacCiphers.com](http://www.zodiacciphers.com/)
- [ZodiacKiller.com](http://www.zodiackiller.com/)

# Online tools / resources

## Tools

## Compilations

- [ZodiacKillerCiphers - Software Tools](http://zodiackillerciphers.com/wiki/index.php?title=Software_Tools)

## Individual tools

### Zodiac-specific

- [ZodiacKillerCiphers - Webtoy](http://zodiackillerciphers.com/webtoy/)
- [ZodiacKillerCiphers - Cipher Explorer](http://zodiackillerciphers.com/cipher-explorer/)
- [ZodiacRevisited - Zodiac Killer Cipher Generator](http://zodiacrevisited.com/zodiac-killer-cipher-generator/)
  - [2012.06.03 - ZodiacRevisited - Cipher Generator Released](http://zodiacrevisited.com/cipher-generator-released/)
  - This lets you generate ciphertext from any input text you provide.
  - It doesn't give you control over the distribution of symbols to plaintext letters.
  - It doesn't seem to give you the mapping of symbols to plaintext letters (i.e. the actual cipher).
- [ZodiacKillerCiphers - CryptoScope](http://zodiackillerciphers.com/webtoy/stats.html)
  - [CryptoScope help](http://zodiackillerciphers.com/wiki/index.php?title=CryptoScope_Help)
  - [2011.09.30 - New CryptoScope features](http://www.oranchak.com/zodiac/webtoy/new_cryptoscope_features.html)
- [ZodiacKillerCiphers - Pattern Drawer](http://zodiackillerciphers.com/zodiac-pattern-drawer/)
  - This allows you to see the effect of various transformations to the ciphertext: reading the symbols backwards, reading
  each column top-down and then L-to-R, reading by columns but zig-zagging up and down, reading in a spiral, and combinations
  of all those.
- [ZodiacKillerSite - Peek-a-boo](http://www.zodiackillersite.com/viewtopic.php?f=81&t=3255#p51370)
  - Authors description: *When I am working on z340 I usually implement transpositioning ideas and statistics. That is fine,
  but I like "visual" results like the ones in smokie treat's excel sheets. Unfortunately my excel skills are very poor and
  so I wrote a tool which keeps track of the letters in the inscription and the transcription rectangles. It is possible to
  select letters and apply a color to them. The main idea is that the relationship between inscription and transcription is
  always considered when applying new colors. That should help to visualize what happens when experimenting with transcriptions.*
- [Martin Lindhe - A widget to investigate symbols missing from the middle rows](https://martinlindhe.github.io/zodiac-widget/letter-distribution/index.html)

### Not Zodiac-specific

- [The Free Dictionary](https://www.thefreedictionary.com/words-containing-ll)
  - This has a very useful feature where you can search for words that: 1) start with some string of characters, 2)
  end with some string of characters, or 3) contain some string of characters.

## Resources

### Zodiac-specific

- [ZodiacKillerCiphers - Zodiac Cipher Font](http://www.zodiackillerciphers.com/?p=726)
- [ZodiacKillerCiphers - ASCII-to-Symbols table](http://zodiackillerciphers.com/wiki/index.php?title=Comparison_of_cipher_alphabets)

### Not Zodiac-specific

- [University of Notre Dame - Cryptanalysis Hints](https://www3.nd.edu/~busiforc/handouts/cryptography/cryptography%20hints.html)
  - Tips for what procedure to follow:
    - Focus on pairs of repeated letters.
    - If the ciphertext contains spaces between words, then try to identify words containing just one, two or three letters.
      - (NW: This is not the case with the 340 ciphertext.)
    - Tailor your table of expected frequencies to the likely content of the message you are trying to decipher.
    - Start by guessing at what a particular sequence of characters decodes to,
    and then see if that leads to further deductions.
  - Frequency reference
    - Order Of Frequency Of Single Letters - E T A O I N S H R D L U
    - Order Of Frequency Of Digraphs - th er on an re he in ed nd ha at en es of or nt ea ti to it st io le is ou ar as de rt ve
    - Order Of Frequency Of Trigraphs - the and tha ent ion tio for nde has nce edt tis oft sth men
    - Order Of Frequency Of Most Common Doubles - ss ee tt ff ll mm oo
    - Order Of Frequency Of Initial Letters - T O A W B C D S F M R H I Y E G L N P U J K
    - Order Of Frequency Of Final Letters - E S T D N R Y F L O G H A K M P U W
    - One-Letter Words - a, I.
    - Most Frequent Two-Letter Words - of, to, in, it, is, be, as, at, so, we, he, by, or, on, do, if, me, my, up, an, go, no, us, am
    - Most Frequent Three-Letter Words - the, and, for, are, but, not, you, all, any, can, had, her, was, one, our, out, day, get, has, him, his, how, man, new, now, old, see, two, way, who, boy, did, its, let, put, say, she, too, use
    - Most Frequent Four-Letter Words - that, with, have, this, will, your, from, they, know, want, been, good, much, some, time
- [Panopy.com - Words with double letters](https://www.panopy.com/iphone/secret-ada/double-letter-words.html)
- [US Army Field Manual 34-40-2 - Basic Cryptanalysis](https://ia801604.us.archive.org/27/items/Fm3440.2BasicCryptAnalysis/fm_34-40.2%20%20-%20Basic%20CryptAnalysis.pdf)

## Research papers

### Compilations

- [ZodiacKillerCiphers - Research Papers](http://zodiackillerciphers.com/wiki/index.php?title=Research_papers)

## Individual papers

### Others

- [1993 - An algorithmic solution of sequential homophonic ciphers](http://www.oranchak.com/king-homophonic-ciphers.pdf)
  - "sequential" means you choose from the homophones for a particular plaintext letter in sequential order.
  - ...but the 340 is clearly *not* sequential in its original orientation.
- [YYYY - MIT - Edwin Olson - Robust dictinoary attack of short simple subtitution ciphers](https://april.eecs.umich.edu/pdfs/olson2007crypt.pdf)

# Does the 340 contain a message?

## Evidence that the 340 does not contain a message

- From one of Zodiac's letters:
  - "If you wonder why I was wipeing the cab down I was leaving fake clews for the police to run all over town with,
  as one might say, I gave the cops som bussy work to do to keep them happy. I enjoy needling the blue pigs."

## Evidence that the 340 does contain a message

- The message contains a crossed out "K", with a backwards "K" written above it, indicating the author had made a mistake.
  - NW: This could, of course, be the Zodiac leaving "fake clews".
- The Zodiac seemed to give a hint for his map cipher: "PS. The Mt. Diablo Code concerns Radians + # inches along the
radians".
  - If this was a false clue, it would be a level of deception that seems to go beyond anything else the Zodiac is
  known to have done.
  - Given the mistakes the Zodiac is known to have made when producing the 408 ciphertext, it seems more likely
  that the Zodiac simply made another mistake and created a ciphertext that was too short to allow a unique solution to
  be found.
  - I (NW) have personally have a friend who loves to give out riddles / puzzles, and a recurring problem I saw
  with the puzzles he gave me is that there seemed to be no way to verify that a potential solution was the correct one
  without asking him.

# Is the 340 meant to be read in a different orientation?

## Evidence for a horizontal reading order

- The symbols tend not to repeat within the same row, but there's no such hesitancy to repeat symbols in the columns.
  - David makes this point at 11:00 in his "What do we know?" talk.

## Evidence for a horizontal-flip orientation

- [ZodiacKillerCiphers - Levenshtein distance analysis](http://zodiackillerciphers.com/wiki/index.php?title=Levenshtein_distance_analysis)
  - David checked the 408 and 340 for partial symbol matches, like if you had "GHAJ" and "GBAJ", with the idea that
  the mismatched symbols may refer to the same underlying plaintext letter.
  - He checked not only the original orientation, but also when rotating the diagram 90 degrees, when flipping it
  horizontally, and when doing both transformations (with the flip first).
  - > The count is at maximum the most for the 408 when it is not transformed via rotations and flips. The count is at
  maximum the most for the 340 when it is flipped horizontally.

# Clues

- We know how the 408 ciphertext was created.
- The frequency distribution of ciphertext symbols is not flat.
- There are two symbols which appear twice in a row at least once: '+' and the horizontally-flipped 'P'.
- We have strong reason to believe that when Zodiac was creating the 340 cipher, he was aware that his previous cipher
had been broken by guessing that he'd use the word "kill" and "I".

# Interesting features of the 408

- [ZodiacKillerCiphers Wiki - Encyclopedia of observations - Z408](http://zodiackillerciphers.com/wiki/index.php?title=Encyclopedia_of_observations#Z408)
  - [Z408 and Z340](http://zodiackillerciphers.com/wiki/index.php?title=Encyclopedia_of_observations#Z408_and_Z340)
- The only repeated n-gram that uses the same character is for the letter "L".
- The most-common symbol is used for the letter 'M', and it is the only symbol
that represents 'M'.
- 'E' is represented by five different symbols
- The second-most-common symbol is used for the letter 'I', and 'I' is the second-most-common letter in the plaintext.
- The third-most-common symbol is used for the letter 'L', and 'L' is the
fourth-most-common symbol.
- The symbol for 'C' is the 9th-most-common symbol, and it is the only symbol
that represents 'C'. Ditto for the symbol for 'U', which is the 10th-most-common
symbol.

# How the 408 was originally solved

- [10 second clip of an interview with Donald Harden](http://www.zodiackiller.com/donaldharden.mp3   )
  - "we felt that the word 'kill' or 'killing' would appear in his code, and the word 'I', because he had an ego."
- [Annotated solution to the 408 cipher, based on the Harden worksheets](http://zodiackillerciphers.com/408/key.html)

# Differences between the 340 from the 408

- The 340's cipher is not the same as the 408's cipher.
  - (NW: This is obvious but worth recording explicitly.)
- The 340 was sent about two months after the 408, and the 408 had been decoded after about a week
  of being published, so it seems likely that the 340's cipher was created after the 408's cipher.
- The 340 contains significantly fewer repeated n-grams than the 408.
  - Repeated 4-grams: 2 in the 408, 0 in the 340.
  - Repeated 3-grams: 10 in the 408, 2 in the 340.
  - Repeated 2-grams: 47 in the 408, 21 in the 340.

# Interesting features of the 340

- [ZodiacKillerCiphers Wiki - Encyclopedia of observations - Z340](http://zodiackillerciphers.com/wiki/index.php?title=Encyclopedia_of_observations#Z340)
  - [Z408 and Z340](http://zodiackillerciphers.com/wiki/index.php?title=Encyclopedia_of_observations#Z408_and_Z340)

# Predictions

- It seems reasonable to predict that the 340 will not contain the Zodiak Killer's real name.
  - Why: The Zodiak Killer said the 408 would have his name and it didn't. In fact, it
  explicitly said that he would *never* give away his name because he didn't want to be stopped.

# Why the 340 seems to be using a homophonic cipher

- The 340 is using many more symbols than exist in the alphabet, which is typical of a homophonic cipher.

# What kind of encryption the 340 is almost certainly *not* using

- [A standard one-time pad](https://en.wikipedia.org/wiki/One-time_pad) q   swa
- [A standard four-square cipher](https://en.wikipedia.org/wiki/Four-square_cipher)
  - Why: A standard four-square cipher only uses 25 symbols: the 26 letters of the alphabet minus 'Q'.

# Assumptions

- The person who encoded this message was not very sophisticated.
  - Why:
    - The 408 message included several errors of a type that suggest they were unintentional.
    - Zodiac's plaintext letters to newspapers were also full of spelling errors.
- The cipher is a monoalphabetic homophonic substitution cipher.
  - Why: This is how the 408 ciphertext was created.

# Ideas

## Cribs

- Guess what word starts the text.
- Guess what what words likely appear in the text.

## Pruning

- If after choosing some of the substitutions the final deviation (after having chosen all of the of substititions)
between the actual plaintext letter frequencies and the expected letter frequencies is guaranteed to exceed a
specified amount, or if the deviation of a particular letter's frequency from what's expected exceeds some "sanity check" level,
stop all further exploration in that direction.
  - Example: You choose to substitute 'Z' for the most-common symbol ('+'). The program should now immediately recognize that
  there's no way you're going to be able to get a final letter frequency distribution that will pass a sanity check.

## Scoring function

- Have a function (markov model?) that takes in two or more characters and returns the frequency with which they
appear in that order (in some reference body of text). Run that across every adjacent pair of characters and
prune / fail a branch of exploration if it has too many characters that never show up next to each other (ljsfna).
- Starting with 1-character and going up to, say, 5 characters, run across every n characters and see if it appears
in a dictionary. If it does, start at the next sequence of characters after this sequence and see if *that*
contains a word (of any length).

## Frequency analysis

- Use the letter frequencies from the decoded 408
- Use the letter frequencies from the Zodiac's known writings

# Misc

- Have various constraints that you brute-force combinations of. For example, "The 'my name is' ciphertext was a
clue to the cipher of the 340 ciphertext". Then with those constraints brute-force check the 7 different options
for the + symbol (assuming it's representing a single letter). Then look for groups of four letters in a row that
would be impossible to get from a correct solution (e.g. four consonants or four vowels in a row; there are probably
other patterns to look for that would show those characters are not from a word or two words back-to-back. ex: "Q"
followed by any consonant). At that point you can probably eliminate that combination as likely. If you don't find
any obvious problems, then continue doing a brute-force search by looking at your existing placed characters and
being smart about checking characters next that are the most prevalent and also next to your existing characters,
so you're most likely to either form a new word or create some kind of contradiction.
- Drag the word "kill" (or some other given word) across the ciphertext and determine at which position it maximizes the number of future
appearances of decoded letters that are positioned in such a way that the same word would appear.

# Questions

- Where did the Zodiac likely get the idea to send in a cryptogram?

# Terms / Concepts

## Methods of encryption

- [Substitution cipher](https://en.wikipedia.org/wiki/Substitution_cipher) - This is a cipher where, for each letter of the alphabet in the
plaintext, you substitute a different letter or symbol for each instance of that letter in order to encode the message.  The one most people have
heard of is the Caesar cipher, where you decide on the substitutions by shifting each letter a certain number of spots to the forward in the alphabet.
- [Monoalphabetic cipher](https://en.wikipedia.org/wiki/Substitution_cipher) - This is a cipher that maps each plaintext letter
to the same group of symbols for the duration of the message. So a Caesar cipher (replacing each letter with another letter a certain number
of positions later in the alphabet) is a monoalphabetic cipher. But if the Caesar cipher was slightly more complicated, where every odd letter was
decoded with a ROT5 (rotate 5 letters) Caesar cipher, and every even letter was decoded with a ROT10 Caesar cipher, then that system of
alternating ciphers would be considered a polyalphabetic cipher.
  - The Zodiac Killer used this system for the 408 message, and it seems reasonable to believe he also used this system for his 340 message,
  since he was not very sophisticated and was more interested in toying with the public than in protecting some secret information.
- [Polyalphabetic cipher](https://en.wikipedia.org/wiki/Polyalphabetic_cipher) - This is a 'cipher made up of several ciphers',
where the person encoding the message switches from one cipher to another according to some prearranged method, or while indicating to the
reader that he has switched ciphers (and if necessary, which cipher he has switched to). Usually it seems like the method of switching between
ciphers is to just rotate among a list. So you start with cipher 1, then switch to cipher 2, then to 3, and then back to 1.
  - It doesn't seem likely that the Zodiac Killer used this method of encoding his 340 message, because his goal seems to have been to toy
  with the public and the police by giving them a puzzle, rather than to protect some information from being discovered (as is the case
  with government ciphers).
- [Homophonic substitution](https://en.wikipedia.org/wiki/Substitution_cipher#Homophonic_substitution) - This is a cipher where a plaintext letter
can decode to any of several ciphertext symbols.  Normally each ciphertext symbol is unique to a particular plaintext letter.
  - The 408 ciphertext used this method of obfuscation. It seems likely that the same method was used for the 340 message.

## Methods of Cryptanalysis

- [Known-plaintext attack / cribs](https://en.wikipedia.org/wiki/Known-plaintext_attack)
  - More information: [Cryptanalysis of the Enigma - Crib-based decryption](https://en.wikipedia.org/wiki/Cryptanalysis_of_the_Enigma#Crib-based_decryption)
- [Frequency analysis](https://en.wikipedia.org/wiki/Frequency_analysis)

# Sources

## The evaluation function

- [Stack Overflow - Scoring a string based on how English-like it is
](https://stackoverflow.com/questions/6878303/scoring-a-string-based-on-how-english-like-it-is)

# Notable researchers

- David Oranchak
  - [2007-2012 - Oranchak.com - Zodiac-related posts](http://www.oranchak.com/?cat=38)
    - [Here](http://www.oranchak.com/?p=364#comment-1296) he says that he started working on the cipher in March of 2007. He released his web toy on April 24, 2007.
  - [2012-Present - ZodiakKillerCophers](http://www.zodiackillerciphers.com/)
  - [Amazon.com - David Oranchak - The Big Book of Shinro Puzzles](https://www.amazon.com/Big-Book-Shinro-Puzzles/dp/145366050X/ref=sr_1_1?s=books&ie=UTF8&qid=1516041163&sr=1-1&refinements=p_27%3ADavid+Oranchak)
    - Mentioned in his 2017.10.19 talk.

