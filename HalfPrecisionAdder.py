"""Creating a half precision adder"""

"""Stage1 Compare the exponents and determine the amount of shifts required to align the
mantissa to make the exponents equal. Then, right-shift the mantissa of the smaller exponent by
the required amount (alignment)"""


# Python program to convert float
# decimal to binary number
def decimal_converter(num):
    while num > 1:
        num /= 10
    return num


# Function returns octal representation
def float_bin(number):
    if number == int(number):
        if number > 0:  # Checking if the number is positive
            res = bin(number)[2:]
            #            print(type(res))
            res = "pos" + ',' + str(res)
            return res
        else:
            number = abs(number)  # Taking the abs value of the number to consider negative numbers also
            res = bin(number)[2:]
            res = "neg" + ',' + str(res)
            return res

    else:
        if number > 0:
            sign = 'pos'
        else:
            sign = 'neg'

        number = 1.0 * number  # converting to float
        # print(number)
        # split() separates whole number and decimal
        # part and stores it in two separate variables
        whole, dec = str(number).split(".")

        # Convert both whole number and decimal
        # part from string type to integer type
        whole = int(whole)
        dec = int(dec)

        # Convert the whole number part to it's
        # respective binary form and remove the
        # "0b" from it.
        res = bin(whole).lstrip("0b") + "."

        # Iterate the number of times, we want
        # the number of decimal places to be
        for x in range(12):  # use of 12 to normalise the values
            # Multiply the decimal value by 2
            # and separate the whole number part
            # and decimal part
            whole, dec = str((decimal_converter(dec)) * 2).split(".")

            # Convert the decimal part
            # to integer again
            dec = int(dec)

            # Keep adding the integer parts
            # receive to the result variable
            res += whole
        #        print(type(res))

        if sign == 'pos':
            res = sign + ',' + res
            return res
        else:
            res = res[3:]
            res = sign + ',' + res
            return res

    # Function converts the value passed as
    # parameter to it's decimal representation

    # Driver Code

    # Take the user input for
    # the floating point number
    # n = input("Enter your floating point value : \n")

    # Take user input for the number of
    # decimal places user want result as
    # p = int(input("Enter the number of decimal places of the result : \n"))

    # print(float_bin(n, places=p))


def count_exponential(signed_number):
    sign, number = signed_number.split(',')

    """Converting binary number into standard exponential number"""
    # int_number = number.split('.')
    count = 0
    for i in number:

        if i == '0' or i == '1' and i != '.':
            count += 1
        else:
            return count
    return count


def convert_standard(signed_number, count):
    sign, number = signed_number.split(',')
    num_output = []
    number_exp_output = number.split('.')
    for i in range(len(number_exp_output)):
        num_output.append(number_exp_output[i])

    joined_binary = ''.join(num_output)
    # print(joined_binary)
    adjust_binary = sign + ',' + joined_binary[0] + '.' + joined_binary[1:] + 'exp' + str(count - 1)
    # print(adjust_binary)
    return adjust_binary


def ieee_754_standard(num):
    sign, real_value = num.split(',')
    real, mantissa_and_exponent = real_value.split('.')
    mantissa, exponent = mantissa_and_exponent.split('exp')
    # print(sign)
    # print(real)
    # print(mantissa)
    # print(exponent)
    strd_form = []
    if sign == 'pos':
        strd_form.append(0)
    elif sign == 'neg':
        strd_form.append(1)

    """Converting mantissa to real mantissa"""
    real_exponent = int(exponent) + 15
    exponent_binary_converted = float_bin(real_exponent)
    sign_m, exponent_binary_converted = exponent_binary_converted.split(',')
    # print(type(mantissa_binary_converted))
    len_mantissa = len(exponent_binary_converted)
    # print(exponent)
    # print(bin(int(exponent)))
    # zeros_to_be_appended = 5-(len(bin(int(exponent)))-2)
    # print(zeros_to_be_appended)
    exponent_adjusted = 15 + int(exponent)
    exponent_adjusted = bin(exponent_adjusted)[2:]
    # print(sign)
    # print(exponent_adjusted)
    # print(mantissa)

    """Adjusting the mantissa"""
    length_mantissa = len(mantissa)
    list_mantissa = []
    j = 0
    for i in range(length_mantissa):
        list_mantissa.insert(i, mantissa[j])
        j += 1
    b = '0'
    for i in range(length_mantissa, 12):
        list_mantissa.insert(i, b)

    # print(list_mantissa)
    mantissa = ''.join(str(i) for i in list_mantissa)
    """Creating a list and try to append the number in the IEEE floating point format"""
    ieee_strd_form = []
    if sign == 'pos':
        ieee_strd_form.insert(0, 0)
    elif sign == 'neg':
        ieee_strd_form.insert(0, 1)
    else:
        pass

    """Initialising default zero value in ieee_strd_form[1:6]"""
    for i in range(1, 6):
        ieee_strd_form.insert(i, 0)

    """Adjusting the exponent part to 5 decimal places"""
    # print(len(exponent_adjusted))
    # exponent_adjusted = '1111'
    if len(exponent_adjusted) != 5:
        temp1 = []
        no_zeroes_to_be_inserted = 5 - len(exponent_adjusted)
        for i in range(no_zeroes_to_be_inserted):
            temp1.insert(i, 0)

        j = 0
        for i in range(no_zeroes_to_be_inserted, 5):
            temp1.insert(i, int(exponent_adjusted[j]))
            j = j + 1
    else:
        temp1 = []
        j = 0
        for i in range(len(exponent_adjusted)):
            temp1.insert(i, int(exponent_adjusted[j]))
            j = j + 1

    j = 0
    for i in range(1, 6):
        ieee_strd_form.insert(i, temp1[j])
        j = j + 1

    ieee_strd_form = ieee_strd_form[:6]
    # temp1 = adjusted_exponent
    """Code for normalizing the mantissa part"""
    # print(mantissa)
    # print(mantissa[9])
    # print(mantissa[10])
    mantissa = mantissa[:11]
    if mantissa == '1111111111':
        mantissa = '0000000000'
    elif mantissa[10] == '1':
        b = '1'
        mantissa = bin(int(mantissa[:10], 2) + int(b, 2))[2:]
        # print(mantissa)
    else:
        mantissa = mantissa[:10]

    sign_exponent = ''.join(str(i) for i in ieee_strd_form)
    # print(sign_exponent)
    # print(mantissa)
    sign_exponent_mantissa = sign_exponent + mantissa

    # print(sign_exponent_mantissa)
    # print(sign)
    # print(exponent_adjusted)
    # print(exponent)

    sign_exponent_mantissa = sign + ',' + exponent_adjusted + ',' + mantissa + ',' + exponent
    return sign_exponent_mantissa


def adjust_mantissa(smaller, larger):
    sign_c, bin_exponent_c, mantissa_c, exp_c = smaller.split(',')
    sign_d, bin_exponent_d, mantissa_d, exp_d = larger.split(',')
    diff = abs(int(exp_d) - int(exp_c))
    zero_list = []
    zero_list_value = diff - 1
    for i in range(0, zero_list_value):
        zero_list.insert(i, '0')
    s = ''.join(zero_list)
    # y = [diff:10]
    s = s + '1' + mantissa_c[0:10 - diff]
    # print(s)

    # print(sign_c)
    # print(bin_exponent_c)
    # print(mantissa_c)
    # print(exp_c)
    # print(sign_d)
    # print(bin_exponent_d)
    # print(mantissa_d)
    # print(exp_d)
    # #mantissa_c = '1111111111'   #Testing the left shift operator
    # diff = int(exp_d) - int(exp_c)
    # print(diff)
    # mantissa_left_cut = mantissa_c[0:(10 - diff)]
    # """Defining the arrangement for the left part of the mantissa"""
    # adjust_list = []
    # a = '0'
    # for i in range(0, diff-1):
    #     adjust_list.insert(i, a)
    # b = '1'
    # adjust_list.insert(i+1, b)
    #
    # #print(adjust_list)
    # mantissa_right_cut = ''.join(adjust_list)
    # #print(mantissa_right_cut)
    # adjusted_mantissa = mantissa_right_cut + mantissa_left_cut
    # #print(adjusted_mantissa)
    smaller = sign_c + ',' + bin_exponent_d + ',' + s + ',' + exp_d
    return smaller


def normal_addition_1(smaller_mantissa, larger_mantissa, larger_exp):
    # smaller_mantissa = '0000100000'
    # larger_mantissa = '0000001000'
    result = bin(int(smaller_mantissa, 2) + int(larger_mantissa, 2))[2:]
    if len(result) < 10:  # print(result)
        diff = 10 - len(result)
        empty_list = []
        n = '0'
        for c in range(diff):
            empty_list.insert(c, n)
        m = ''.join(empty_list)
        result_mantissa = m + result
        #########Normalising
        x = 0
        for x in range(10):
            if result_mantissa[x] == '1':
                break
        first_one_position = x
        # print(first_one_position)
        remaining_mantissa = result_mantissa[first_one_position + 1:10]
        # print(remaining_mantissa)
        remaining_mantissa_length = len(remaining_mantissa)
        # print(remaining_mantissa_length)
        diff = 10 - remaining_mantissa_length

        temp_list_1 = []
        a = '0'
        for i in range(diff):
            temp_list_1.insert(i, a)

        s = ''.join(temp_list_1)
        result_normalised_mantissa = remaining_mantissa + s

        value_to_be_subtracted_from_exp = first_one_position + 1
        new_exponent = int(larger_exp) - value_to_be_subtracted_from_exp
        # new_exponent = 0
        # print(new_exponent)
        adjusted_new_exponent = bin(15 + new_exponent)[2:]
        # print(adjusted_new_exponent)
        adjusted_new_exponent_length = len(adjusted_new_exponent)
        # print(remaining_mantissa_length)
        diff = 5 - adjusted_new_exponent_length

        temp_list_2 = []
        a = '0'
        for i in range(diff):
            temp_list_2.insert(i, a)

        s = ''.join(temp_list_2)
        adjusted_new_exponent = s + adjusted_new_exponent
        # print(adjusted_new_exponent)
        result_sign = '0'
        # print(result_sign)
        # print(adjusted_new_exponent)
        # print(result_normalised_mantissa)
        result = result_sign + adjusted_new_exponent + result_normalised_mantissa

        # result_exponent = 15 + int(larger_exp)
        # # print(result_exponent)
        # result_exponent = bin(int(result_exponent))[2:]
        # # print(result_exponent)
        # result_exponent_length = len(result_exponent)
        # # print(result_exponent_length)
        # diff = 5 - result_exponent_length
        # temp_list = []
        # a = '0'
        # for i in range(diff):
        #     temp_list.insert(i, a)
        #
        # s = ''.join(temp_list)
        # result_exponent = s + result_exponent

        # print(result_sign)
        # print(result_exponent)
        # print(result_mantissa)
        # result = result_exponent + result_mantissa
        return result
    ##########
    elif len(result) == 11:
        # if result[0] == '1':
        result_mantissa = result[1:]
        result_sign = '0'
        # larger_exp = 0
        result_exponent = 15 + int(larger_exp)
        # print(result_exponent)
        result_exponent = bin(int(result_exponent))[2:]
        # print(result_exponent)
        result_exponent_length = len(result_exponent)
        # print(result_exponent_length)
        diff = 5 - result_exponent_length
        temp_list = []
        a = '0'
        for i in range(diff):
            temp_list.insert(i, a)

        s = ''.join(temp_list)
        result_exponent = s + result_exponent

        # print(result_sign)
        # print(result_exponent)
        # print(result_mantissa)
        result = result_exponent + result_mantissa
        return result

    else:
        result_mantissa = result
        # print(result_mantissa)
        result_mantissa_length = len(result_mantissa)
        diff = 10 - result_mantissa_length
        temp_list = []
        a = '0'
        for i in range(diff):
            temp_list.insert(i, a)

        s = ''.join(temp_list)
        result_mantissa = result_mantissa + s
        # print(result_mantissa)

        x = 0
        for x in range(10):
            if result_mantissa[x] == '1':
                break
        first_one_position = x
        # print(first_one_position)
        remaining_mantissa = result_mantissa[first_one_position + 1:10]
        # print(remaining_mantissa)
        remaining_mantissa_length = len(remaining_mantissa)
        # print(remaining_mantissa_length)
        diff = 10 - remaining_mantissa_length

        temp_list_1 = []
        a = '0'
        for i in range(diff):
            temp_list_1.insert(i, a)

        s = ''.join(temp_list_1)
        result_normalised_mantissa = remaining_mantissa + s

        value_to_be_subtracted_from_exp = first_one_position + 1
        new_exponent = int(larger_exp) - value_to_be_subtracted_from_exp
        # new_exponent = 0
        # print(new_exponent)
        adjusted_new_exponent = bin(15 + new_exponent)[2:]
        # print(adjusted_new_exponent)
        adjusted_new_exponent_length = len(adjusted_new_exponent)
        # print(remaining_mantissa_length)
        diff = 5 - adjusted_new_exponent_length

        temp_list_2 = []
        a = '0'
        for i in range(diff):
            temp_list_2.insert(i, a)

        s = ''.join(temp_list_2)
        adjusted_new_exponent = s + adjusted_new_exponent
        # print(adjusted_new_exponent)
        result_sign = '0'
        # print(result_sign)
        # print(adjusted_new_exponent)
        # print(result_normalised_mantissa)
        result = result_sign + adjusted_new_exponent + result_normalised_mantissa
        # print(result)
        return result


def twos_complement(str):
    # print(str)
    if str == '0000000000':
        return str
    else:

        n = len(str)

        # Traverse the string to get first
        # '1' from the last of string
        i = n - 1
        while (i >= 0):
            if (str[i] == '1'):
                break

            i -= 1

        # If there exists no '1' concatenate 1
        # at the starting of string
        if (i == -1):
            return '1' + str

        # Continue traversal after the
        # position of first '1'
        k = i - 1
        while (k >= 0):

            # Just flip the values
            if (str[k] == '1'):
                str = list(str)
                str[k] = '0'
                str = ''.join(str)
            else:
                str = list(str)
                str[k] = '1'
                str = ''.join(str)

            k -= 1

        # return the modified string
        return str


def normal_addition_2(smaller_mantissa, twos_complement_mantissa, larger_exp):
    # print(smaller_mantissa)
    # print(twos_complement_mantissa)
    # print(larger_exp)
    result = bin(int(smaller_mantissa, 2) + int(twos_complement_mantissa, 2))[2:]
    # print(result)
    result_mantissa = ''
    if len(result) == 11:
        if result[0] == '1':
            result_mantissa = result[1:]
            result_sign = '0'
            result_exp = bin(15 + int(larger_exp))[2:]

            final_answer = result_sign + result_exp + result_mantissa
            return final_answer
    else:
        result_mantissa = result  # part for taking the two's complement
        result_sign = 'neg'

        result_exp = larger_exp
        """Normalising the mantissa part """
        result_mantissa_len = len(result_mantissa)
        print(result_mantissa_len)
        s = 0
        for s in range(result_mantissa_len):
            if result_mantissa[s] == '1':
                break
        first_one_position = s

        remaining_mantissa = result_mantissa[first_one_position + 1:10]
        # print(remaining_mantissa)
        remaining_mantissa_length = len(remaining_mantissa)
        # print(remaining_mantissa_length)
        diff = result_mantissa_len - remaining_mantissa_length

        temp_list_1 = []
        a = '0'
        for j in range(diff):
            temp_list_1.insert(j, a)

        s = ''.join(temp_list_1)
        result_normalised_mantissa = remaining_mantissa + s

        value_to_be_subtracted_from_exp = first_one_position + 1
        new_exponent = int(larger_exp) - value_to_be_subtracted_from_exp
        # new_exponent = 0
        # print(new_exponent)
        adjusted_new_exponent = bin(15 + new_exponent)[2:]
        # print(adjusted_new_exponent)
        adjusted_new_exponent_length = len(adjusted_new_exponent)
        # print(remaining_mantissa_length)
        diff = 5 - adjusted_new_exponent_length

        temp_list_2 = []
        a = '0'
        for k in range(diff):
            temp_list_2.insert(k, a)

        s = ''.join(temp_list_2)
        adjusted_new_exponent = s + adjusted_new_exponent
        # print(adjusted_new_exponent)
        # print(result_sign)
        result_sign = '1'
        # print(result_sign)
        # print(adjusted_new_exponent)
        # print(result_normalised_mantissa)
        result = adjusted_new_exponent + result_normalised_mantissa
        # print(result)
        return result


def normal_subtraction_1(smaller_mantissa, larger_mantissa, larger_exp, smaller_sign, larger_sign):
    # if len(smaller_mantissa) == 10:
    #     #print(smaller_mantissa)
    #     smaller_mantissa = '0' + smaller_mantissa
    #     print(smaller_mantissa)
    # if len(larger_mantissa) == 10:
    #     #print(larger_mantissa)
    #     larger_mantissa = '0' + larger_mantissa
    #     print(larger_mantissa)
    # Checking the condition for overflow addition bits in two's complement addition.
    if smaller_sign == 'neg':
        # if smaller_mantissa[0] == '1':
        # smaller_mantissa = '0' + smaller_mantissa
        # print(smaller_mantissa)

        smaller_mantissa_twos_complement = twos_complement(smaller_mantissa)
        # print(smaller_mantissa_twos_complement)
        return normal_addition_2(larger_mantissa, smaller_mantissa_twos_complement, larger_exp)
    else:
        # if larger_mantissa[0] == '1':
        #   larger_mantissa = '0' + larger_mantissa
        # print(larger_mantissa)

        larger_mantissa_twos_complement = twos_complement(larger_mantissa)
        # print(larger_mantissa_twos_complement)
        return normal_addition_2(smaller_mantissa, larger_mantissa_twos_complement, larger_exp)


def stage1(a, b):
    if a == 0 and b == 0:
        print('000000000000000')
        return

    a_bin = float_bin(a)
    b_bin = float_bin(b)
    # print(a_bin)
    # print(b_bin)
    # print(count_exponential(a_bin))  # used to check the whether exponential are working or not
    # print(count_exponential(b_bin))
    # convert_standard(a_bin, count_exponential(a_bin))
    # convert_standard(b_bin, count_exponential(b_bin))
    if a_bin == 0:
        a_bin_converted = 'pos,00000,0000000000,0'
    else:
        a_bin_converted = ieee_754_standard(convert_standard(a_bin, count_exponential(a_bin)))
    print('The number {} converted in ieee standard format is {}'.format(a, a_bin_converted))

    if b_bin == 0:
        b_bin_converted = 'pos,00000,0000000000,0'
    else:
        b_bin_converted = ieee_754_standard(convert_standard(b_bin, count_exponential(b_bin)))
    # print(a_bin_converted)
    print('The number {} converted in ieee standard format is {}'.format(a, a_bin_converted))
    # print(b_bin_converted)
    """Comparing and shifting of mantissa"""
    sign_a, binary_exponent_a, mantissa_a, exponent_a = a_bin_converted.split(',')
    # print(sign_a)
    # print(binary_exponent_a)
    # print(mantissa_a)
    # print(exponent_a)
    sign_b, binary_exponent_b, mantissa_b, exponent_b = b_bin_converted.split(',')
    # print(sign_b)
    # print(binary_exponent_b)
    # print(mantissa_b)
    # print(exponent_b)
    """Comparing of the exponent"""  # condition should also be written if two exponents are equal.
    if exponent_b < exponent_a:
        smaller = b_bin_converted
        larger = a_bin_converted
        adjusted_smaller_mantissa = adjust_mantissa(smaller, larger)
        # print(adjusted_smaller_mantissa)
        smaller = adjusted_smaller_mantissa
        # print(smaller)
    elif exponent_a < exponent_b:
        smaller = a_bin_converted
        # print(smaller)
        larger = b_bin_converted
        adjusted_smaller_mantissa = adjust_mantissa(smaller, larger)
        # print(adjusted_smaller_mantissa)
        smaller = adjusted_smaller_mantissa
    else:
        smaller = a_bin_converted
        larger = b_bin_converted

    # adjusted_smaller_mantissa = adjust_mantissa(smaller, larger)
    # # print(adjusted_smaller_mantissa)
    # smaller = adjusted_smaller_mantissa
    #print(smaller)
    #print(larger)
    print('The two number after adjusting the mantissa are {}   {}'.format(smaller,larger))
    smaller_sign, smaller_bin_exp, smaller_mantissa, smaller_exp = smaller.split(',')
    larger_sign, larger_bin_exp, larger_mantissa, larger_exp = larger.split(',')
    # print(larger_mantissa)
    # print(smaller_mantissa)
    # if smaller_sign == 'neg':
    #     mantissa_to_be_complemented = smaller_mantissa
    # else:
    #     mantissa_to_be_complemented = larger_mantissa
    #
    # print(mantissa_to_be_complemented)
    """Complementing number cases"""
    # smaller_sign = 'pos'
    # larger_sign = 'neg'
    if smaller_sign == 'pos' and larger_sign == 'pos':
        # print(larger_exp)
        result = '0' + normal_addition_1(smaller_mantissa, larger_mantissa, larger_exp)
        # final_answer = '0'+larger_bin_exp+result_mantissa
        print('The final answer after addition is \n {}'.format(result))
    elif smaller_sign == 'pos' and larger_sign == 'neg':
        result = normal_subtraction_1(smaller_mantissa, larger_mantissa, larger_exp, smaller_sign, larger_sign)
        result = '1' + result
        #print(result)
        print('The final answer after addition is \n {}'.format(result))
    elif smaller_sign == 'neg' and larger_sign == 'pos':
        result = normal_subtraction_1(smaller_mantissa, larger_mantissa, larger_exp, smaller_sign, larger_sign)
        result = '0' + result
        #print(result)
        print('The final answer after addition is \n {}'.format(result))
    elif smaller_sign == 'neg' and larger_sign == 'neg':

        result = '1' + normal_addition_1(smaller_mantissa, larger_mantissa, larger_exp)[1:]
        print('The final answer after addition is \n {}'.format(result))
    else:
        pass


a = float(input("Enter the first number to be added rounded to two decimal"))
b = float(input("Enter the second number to be added"))
#num1 = float("%0.2f" % (a))
a = round(a, 2)
b = round(b, 2)
# a = float("{0:.2f}".format(a))
#b = float("{0:.2f}".format(b))
#a = float("%0.2f" %a)
#a = '%.20f' % a
print(a)
#b = '%.20f' % b
#b = float("%0.2f" %b)
#num2 = float("%0.2f" % (num))
print(b)
stage1(a, b)


