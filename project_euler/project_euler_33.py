import copy

def main():
    digits = get_digits()

    for x in xrange(10, 100):
        for y in xrange(10, 100):
            if x >= y:
                continue
            d1 = digits[x]
            d2 = digits[y]

            in_both = -1
            for digit in d1:
                if digit in d2:
                    d3 = copy.deepcopy(d1)
                    d4 = copy.deepcopy(d2)
                    d3.remove(digit)
                    d4.remove(digit)
                    new_num = d3[0]
                    new_denom = d4[0]
                    if new_denom > 0:
                        if float(x)/float(y) == float(new_num) / float(new_denom):
                            print x, y


def get_digits():
    digits = {}
    for x in xrange(10, 100):
        digits[x] = [(int)(x / 10), x % 10]
    return digits

main()

"""
16 64
19 95
26 65
49 98
"""
1*19*26*49 = 24206
4*95*65*98 = 2420600
