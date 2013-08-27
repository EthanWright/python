"""
Expanding exercise upon language_parser1.py:

We have decided to extend the protocol to accept an arbitrary number of valid
messages. If a message begins with a number, precisely that number of valid
messages must follow. e.g.
3aaa VALID
2aaa INVALID
2ZaMbb VALID
K2aaa VALID
10aaaaaaaaaa VALID

The program is run on the command line as:
python language_parser2.py "<words>"
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
        elif letter in str(range(9)):
            num = 0
            while word[0] in str(range(9)):
                num *= 10
                num += int(word[0])
                word = word[1:]
            for x in xrange(num):
                word = parse(word)
            return word
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

def is_word_multi(word):
    word = parse(word)
    if word == '':
        return 'Valid'
    else:
        return 'Invalid'

if __name__ == '__main__':
    if len(sys.argv) == 2:
        words = sys.argv[1]
    else:
        words = '3aaa 2aaa 2ZaMbb K2aaa 10aaaaaaaaaa'
    word_list = words.split(' ')

    for word in word_list:
        print word,
        print is_word_multi(word)
