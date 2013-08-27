"""
Exercise:
We've built a new communication protocol that sends messages with a restricted
syntax. We need to write a function which determines whether a given message is
syntactically valid or not. Here are the rules:

There are 15 valid characters in the protocol: the lower-case characters 'a'
through 'j' and the uppercase characters 'Z', 'M', 'K', 'P', and 'Q'.
Every lower-case character in isolation is a valid message, e.g., 'a' is a
valid message.
If σ is a valid message then so is Zσ.
If σ and τ are valid messages then so are Mστ, Kστ, Pστ, and Qστ.

The input consists of a series of potential messages separated by whitespace
and containing only the 15 characters above.

The output consists of one line per potential messages, followed by VALID if
the message is valid and INVALID if it is invalid.

Example output:
Qa INVALID
Zj VALID
MZca VALID
Khfa INVALID
------------------
I first created a preliminary testing method that simplified the expressions by
repeated substitution. This method works, but is limited, especially if a parse
tree were to be generated. So I cam up with a more elegant method that parses
from left to right, removing parsed letters from the word, and then parsing the
rest of the expression accordingly. Whatever part of the word is left over
after parsing is returned. A valid word will return an empty string.

The program is run on the command line as:
python language_parser.py "<words>"
The words should be space separated. If no words are given, then the defaults
from the test examples will be used.

Ethan Wright
8/20/2013
"""

import sys

"""
Expressions:
s = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
Z = Zs
X = ('M', 'K', 'P', 'Q') followed by (s, Zs, X)(s, Zs, X)

s, Z, X are all valid
"""

def parse(word):
    for letter in word:
        if letter == '':
            return ''
        if is_s(letter):
            return word[1:]
        elif letter == 'Z':
            return parse(word[1:])
        elif is_upper(letter):
            remains = parse(word[1:])
            return parse(remains)
        else:
            return 'Invalid'

def is_s(piece):
    if piece in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'):
        return True
    else:
        return False

def is_upper(piece):
    if piece in ('M', 'K', 'P', 'Q'):
        return True
    else:
        return False

def is_word(word):
    results = parse(word)
    if results == '':
        return 'Valid'
    else:
        return 'Invalid'

if __name__ == '__main__':
    if len(sys.argv) == 2:
        words = sys.argv[1]
    else:
        words = 'MZca Qa Zj MZca Khfa'
    word_list = words.split(' ')

    for word in word_list:
        print word,
        print is_word(word)
