"""
Expanding exercise upon language_parser2.py:

In the case of invalid messages, output more descriptive errors.
For valid messages, output a parse tree.

This program is an altered version of language_parser2.py, edited to accept the
language described by the first bonus problem. It is also edited to print out
more descriptive errors, and to print out a parse tree.

The program is run on the command line as:
python language_parser3.py "<words>"
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
X = ('M', 'K', 'P', 'Q') followed by (s, Z, X)(s, Z, X)

s, Z, X are all valid
"""

tree = []

def parse(word, level):
    for letter in word:
        if letter == '':
            return ''
        if is_s(letter):
            tree.append((level, letter))
            return word[1:]
        elif letter == 'Z':
            tree.append((level, letter))
            return parse(word[1:], level+1)
        elif is_upper(letter):
            tree.append((level, letter))
            remains = parse(word[1:], level+1)
            return parse(remains, level+1)
        elif letter in str(range(9)):
            num = 0
            while word[0] in str(range(9)):
                num *= 10
                num += int(word[0])
                word = word[1:]
            tree.append((level, num))
            for x in xrange(num):
                word = parse(word, level+1)
            return word
        else:
            return 'Invalid %s' % word

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
    word = parse(word, 0)
    if word == '':
        return 'Valid'
    else:
        if word.startswith('Invalid'):
            print "\nInvalid characters detected: %s" % word[8:]
        else:
            print "\nSuperflous characters not parsed: %s" % word
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
        print "Parse sequence: ",
        print tree
