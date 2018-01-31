
alphabet_lowercase = "abcdefghijklmnopqrstuvwxyz"
alphabet_capitalized = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

start_of_syllable_consonant_blends = ["bl", "br", "ch", "cl", "cr", "dr", "fl", "fr", "gh", "gl", "gr", "kn", "kw",
                                      "ph", "pl", "pr", "qu", "sc", "sh", "sk", "sl", "sm", "sn", "sp", "st", "sw",
                                      "th", "tr", "tw", "wh", "wr", "sch", "scr", "shr", "spl", "spr", "squ", "str",
                                      "th"]

vowel_digraphs = ["ai", "au", "ay", "ea", "ee", "ei", "eo", "eu", "ey", "ia", "ie", "io", "oa", "oe"]

vowel_trigraphs = ["igh"]

vowel_quadgraphs =["eaue", "eigh"]

# The encoded ciphertexts are from http://zodiackillerciphers.com/wiki/index.php?title=Webtoy%27s_transcription_scheme

z340 = ["HER>pl^VPk|1LTG2d",
        "Np+B(#O%DWY.<*Kf)",
        "By:cM+UZGW()L#zHJ",
        "Spp7^l8*V3pO++RK2",
        "_9M+ztjd|5FP+&4k/",
        "p8R^FlO-*dCkF>2D(",
        "#5+Kq%;2UcXGV.zL|",
        "(G2Jfj#O+_NYz+@L9",
        "d<M+b+ZR2FBcyA64K",
        "-zlUV+^J+Op7<FBy-",
        "U+R/5tE|DYBpbTMKO",
        "2<clRJ|*5T4M.+&BF",
        "z69Sy#+N|5FBc(;8R",
        "lGFN^f524b.cV4t++",
        "yBX1*:49CE>VUZ5-+",
        "|c.3zBK(Op^.fMqG2",
        "RcT+L16C<+FlWB|)L",
        "++)WCzWcPOSHT/()p",
        "|FkdW<7tB_YOB*-Cc",
        ">MDHNpkSzZO8A|K;+"]

z340_symbols = set(list("".join(z340)))

z340_first_quadrant = [row[:10] for row in z340[:11]]
z340_second_quadrant = [row[8:] for row in z340[:11]]
z340_third_quadrant = [row[:10] for row in z340[11:]]
z340_fourth_quadrant = [row[8:] for row in z340[11:]]

z408 = ["9%P/Z/UB%kOR=pX=B",
        "WV+eGYF69HP@K!qYe",
        "MJY^UIk7qTtNQYD5)",
        "S(/9#BPORAU%fRlqE",
        "k^LMZJdr\\pFHVWe8Y",
        "@+qGD9KI)6qX85zS(",
        "RNtIYElO8qGBTQS#B",
        "Ld/P#B@XqEHMU^RRk",
        "cZKqpI)Wq!85LMr9#",
        "BPDR+j=6\\N(eEUHkF",
        "ZcpOVWI5+tL)l^R6H",
        "I9DR_TYr\\de/@XJQA",
        "P5M8RUt%L)NVEKH=G",
        "rI!Jk598LMlNA)Z(P",
        "zUpkA9#BVW\\+VTtOP",
        "^=SrlfUe67DzG%%IM",
        "Nk)ScE/9%%ZfAP#BV",
        "peXqWq_F#8c+@9A9B",
        "%OT5RUc+_dYq_^SqW",
        "VZeGYKE_TYA9%#Lt_",
        "H!FBX9zXADd\\7L!=q",
        "_ed##6e5PORXQF%Gc",
        "Z@JTtq_8JI+rBPQW6",
        "VEXr9WI6qEHM)=UIk"]

z408_symbols = set(list("".join(z408)))

def get_ciphertext(path_to_file_with_ciphertext):
    """ Returns a list of lists

    :param path_to_file_with_ciphertext:
    :return:
    """
    with open(path_to_file_with_ciphertext) as inputfile:
        rows_of_ciphertext_characters = [[character for character in row.strip()] for row in inputfile.readlines()]
    return rows_of_ciphertext_characters
