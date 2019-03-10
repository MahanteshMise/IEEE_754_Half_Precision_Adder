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
    #print(adjust_binary)
    return adjust_binary


def ieee_754_standard(num):
    sign, real_value = num.split(',')
    real, mantissa_and_exponent = real_value.split('.')
    mantissa, exponent = mantissa_and_exponent.split('exp')
    # print(sign)
    # print(real)
    # print(mantissa)
    #print(exponent)
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
    #print(sign)
    #print(exponent_adjusted)
    #print(mantissa)

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
    #exponent_adjusted = '1111'
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
    #temp1 = adjusted_exponent
    """Code for normalizing the mantissa part"""
    #print(mantissa)
    #print(mantissa[9])
    #print(mantissa[10])
    mantissa = mantissa[:11]
    if mantissa == '1111111111':
        mantissa = '0000000000'
    elif mantissa[10] == '1':
        b = '1'
        mantissa = bin(int(mantissa[:10], 2) + int(b, 2))[2:]
        #print(mantissa)
    else:
        mantissa = mantissa[:10]

    sign_exponent = ''.join(str(i) for i in ieee_strd_form)
    #print(sign_exponent)
    #print(mantissa)
    sign_exponent_mantissa = sign_exponent + mantissa

    #print(sign_exponent_mantissa)
    #print(sign)
    #print(exponent_adjusted)
    #print(exponent)

    sign_exponent_mantissa = sign + ',' + exponent_adjusted + ','+mantissa + ','+exponent
    return sign_exponent_mantissa

def adjust_mantissa(smaller, larger):
    sign_c, bin_exponent_c, mantissa_c, exp_c = smaller.split(',')
    sign_d, bin_exponent_d, mantissa_d, exp_d = larger.split(',')
    # print(sign_c)
    # print(bin_exponent_c)
    # print(mantissa_c)
    #print(exp_c)
    # print(sign_d)
    # print(bin_exponent_d)
    # print(mantissa_d)
    #print(exp_d)
    #mantissa_c = '1111111111'   #Testing the left shift operator
    diff = int(exp_d) - int(exp_c)
    #print(diff)
    mantissa_left_cut = mantissa_c[0:(10 - diff)]
    """Defining the arrangement for the left part of the mantissa"""
    adjust_list = []
    a = '0'
    for i in range(0, diff-1):
        adjust_list.insert(i, a)
    b = '1'
    adjust_list.insert(i+1, b)

    #print(adjust_list)
    mantissa_right_cut = ''.join(adjust_list)
    #print(mantissa_right_cut)
    adjusted_mantissa = mantissa_right_cut + mantissa_left_cut
    #print(adjusted_mantissa)
    smaller = sign_c + ',' + bin_exponent_c + ',' + adjusted_mantissa + ',' + exp_c
    return smaller

def normal_addition(smaller_mantissa, larger_mantissa):
    smaller_mantissa = '1000000000'
    larger_mantissa = '0001000000'
    result = bin(int(smaller_mantissa, 2) + int(larger_mantissa, 2))[2:]
    #print(result)
    if result[0] == '1':
        result_mantissa = result[1:]
        #print(result_mantissa)
    else:
        result_mantissa = result
        #print(result_mantissa)

    return result_mantissa












def stage1(a, b):
    a_bin = float_bin(a)
    b_bin = float_bin(b)
    #print(a_bin)
    #print(b_bin)
    #print(count_exponential(a_bin))  # used to check the whether exponential are working or not
    #print(count_exponential(b_bin))
    convert_standard(a_bin, count_exponential(a_bin))
    convert_standard(b_bin, count_exponential(b_bin))
    a_bin_converted = ieee_754_standard(convert_standard(a_bin, count_exponential(a_bin)))
    b_bin_converted = ieee_754_standard(convert_standard(b_bin, count_exponential(b_bin)))
    #print(a_bin_converted)
    #print(b_bin_converted)
    """Comparing and shifting of mantissa"""
    sign_a, binary_exponent_a, mantissa_a, exponent_a = a_bin_converted.split(',')
    #print(sign_a)
    #print(binary_exponent_a)
    #print(mantissa_a)
    #print(exponent_a)
    sign_b, binary_exponent_b, mantissa_b, exponent_b = b_bin_converted.split(',')
    #print(sign_b)
    #print(binary_exponent_b)
    #print(mantissa_b)
    #print(exponent_b)
    """Comparing of the exponent"""  #condition should also be written if two exponents are equal.
    if exponent_b < exponent_a:
        smaller = b_bin_converted
        larger = a_bin_converted
        #print(smaller)
    else:
        smaller = a_bin_converted
        #print(smaller)
        larger = b_bin_converted

    adjusted_smaller_mantissa = adjust_mantissa(smaller, larger)
    #print(adjusted_smaller_mantissa)
    smaller = adjusted_smaller_mantissa
    print(smaller)
    print(larger)
    smaller_sign, smaller_bin_exp,smaller_mantissa,smaller_exp = smaller.split(',')
    larger_sign,larger_bin_exp,larger_mantissa,larger_exp = larger.split(',')
    #print(larger_mantissa)
    #print(smaller_mantissa)
    # if smaller_sign == 'neg':
    #     mantissa_to_be_complemented = smaller_mantissa
    # else:
    #     mantissa_to_be_complemented = larger_mantissa
    #
    # print(mantissa_to_be_complemented)
    """Complementing number cases"""
    smaller_sign = 'pos'
    larger_sign = 'pos'
    if smaller_sign == 'pos' and larger_sign == 'pos':
        result_mantissa = normal_addition(smaller_mantissa, larger_mantissa)
        final_answer = '0'+larger_bin_exp+result_mantissa
        print(final_answer)
    elif smaller_sign == 'pos' and larger_sign == 'neg':
        pass
    elif smaller_sign == 'neg' and larger_sign == 'pos':
        pass
    elif smaller_sign == 'neg' and larger_sign == 'neg':
        pass
    else:
        pass




stage1(-193.45, 11)
# stage1(-193.45, -11)
