"""
Use dictionary to track unique pairs
find prime factorization of the base
Update the base so it is as small as possible, by extracting common exponents of the prime factors
Adjust the exponent accordingly by adding the extracted exponent amount
if dictionary[base][exponent] == True
Then this term is not distinct.
else:
It is distinct, mark the position in the dictionary
"""

def prime_factorization(num):

    factors = {}
    factor = 2

    while factor <= num:
        if num % factor == 0:
            if factor in factors:
                factors[factor] += 1
            else:
                factors[factor] = 1
            num = num / factor
        else:
            factor += 1

    return factors

def run():
    unique_count = 0
    unique = {}

    for base in range(2, 101):

        factors = prime_factorization(base)  # {2: 4, 3: 2}
        factor_count = [count for count in factors.values()]
        
        adjustment = 1
        base_reduced = base

        for divisor in range(max(factor_count), 1, -1):
            no_common_divisor = [True for count in factor_count if count % divisor != 0]

            if no_common_divisor == []:  # Has a common divisor
                adjustment *= divisor
                factor_count = [count / divisor for count in factor_count]
                for factor in factors:
                    base_reduced = base_reduced / (pow(factor, (divisor - 1)))

        if base_reduced not in unique:
            unique[base_reduced] = {}

        for exponent in range(2, 101):
            exponent_adjusted = exponent * adjustment

            if unique[base_reduced].get(exponent_adjusted) != True:
                unique[base_reduced][exponent_adjusted] = True
                unique_count += 1
                #print(base, exponent)

    return unique_count

if __name__ == "__main__":
    result = run()
    print(result)

    # 9183
