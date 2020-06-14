MAX = 28123
def main():
    nums = get_all_abundant_numbers()
    sums = {number: False for number in xrange(1, MAX)}
    for num1 in nums:
        for num2 in nums:
            sum = num1 + num2
            if sum > 28123:
                break
            else:
                sums[sum] = True

    total = 0
    for s in xrange(1, MAX):
        if sums[s] == False:
            total += s
    print total

def get_all_abundant_numbers():
    abundant = []
    for number in xrange(1, MAX):
        if find_factor_sum(number) > number:
            abundant.append(number)
    return abundant

def find_factor_sum(number):
    factor_sum = 0
    for x in xrange(2, number):
        if number % x == 0:
            factor_sum += x
    return factor_sum

if __name__ == "__main__":
    main()