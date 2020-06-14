
def calculate_digital_sums():
    greatest_sum = 0
    for num in range(1, 100):
        sum = calculate_digital_sum(num)
        #import pdb;pdb.set_trace()
        if sum > greatest_sum:
            greatest_sum = sum

    print("The greatest sum overall is {}".format(greatest_sum))
    return greatest_sum

def to_array(num):
    num_arr = []
    while num:
        digit = num % 10
        num_arr.insert(0, digit)
        num = (num - digit) / 10

    return num_arr

def calculate_digital_sum(num):
    # Turn it into an array
    mult_arr = to_array(num)
    greatest_sum = 0

    for x in range(0, 100):
        #print(mult_arr)
        num_sum = sum(mult_arr)
        if num_sum > greatest_sum:
            greatest_sum = num_sum

        carry = 0
        new_mult_arr = []
        for digit in reversed(mult_arr):
            multiplied = digit * num + carry
            new_value = multiplied % 10

            carry = (multiplied - new_value) / 10
            new_mult_arr.insert(0, new_value)

        # If we have a carry left over, add it to the from of the num_arr
        carry_arr = to_array(carry)
        mult_arr = carry_arr + new_mult_arr

    print("The greatest sum for {} is {}".format(num, greatest_sum))

    return greatest_sum


if __name__ == "__main__":
    calculate_digital_sums()
