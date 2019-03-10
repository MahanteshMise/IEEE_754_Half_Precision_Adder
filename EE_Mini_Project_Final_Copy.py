""" 1)This is a python program to create Half Precision IEEE 754 Floating point adder.
    2)All the four stages have been implemented and commented in the code also and each conversion
      and variables named accordingly.
    3) The code is limited to 3 floating point precision inputs only
    4)Enter the two rounded inputs with appropriate signs in the stage1 section of the code.
    5)Then run the code and note down the results in the output console.
    6)The first output line includes the representation of the num1 in the form sign,ieee_exponent,
    ieee_mantissa and regular exponent value in integer format.
    7)The second output line includes the representation of the num2 in the form sign,ieee_exponent,
    ieee_mantissa and regular exponent value in integer format.
    8)The third output line the smaller exponent number adjusted in the form sign,ieee_exponent,
    ieee_mantissa and regular exponent value in integer format
    9)The fourth output line indicates the larger exponent number in the form in the form sign,ieee_exponent,
    ieee_mantissa and regular exponent value in integer format
    10)The fifth and the sixth lines include if we are taking two's complement or not and if taking it
    includes the result of the addition in the standard IEEE 754 format without normalizing.
    11)The last line indicates the final answer after addition and Normalization in the standard
       IEEE 754 Half Precision Format

                                                    Author :Mahantesh Shashikant Mise
                                                    IDE used for creating :PyCharm
       ----------------------------------************-------------------------------------"""


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

        number = 1.00 * number  # converting to float

        whole, dec = str(number).split(".")

        whole = int(whole)
        dec = int(dec)

        res = bin(whole).lstrip("0b") + "."

        for x in range(3):  # use of 12 to normalise the values

            whole, dec = str((decimal_converter(dec)) * 2).split(".")

            dec = int(dec)

            res += whole

        if sign == 'pos':
            res = sign + ',' + res
            return res
        else:
            res = res[3:]
            res = sign + ',' + res
            return res


def count_exponential(signed_number):
    sign, number = signed_number.split(',')

    """Converting binary number into standard exponential number"""

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
    adjust_binary = sign + ',' + joined_binary[0] + '.' + joined_binary[1:] + 'exp' + str(count - 1)

    return adjust_binary


def ieee_754_standard(num):
    sign, real_value = num.split(',')
    real, mantissa_and_exponent = real_value.split('.')
    mantissa, exponent = mantissa_and_exponent.split('exp')

    strd_form = []
    if sign == 'pos':
        strd_form.append(0)
    elif sign == 'neg':
        strd_form.append(1)

    """Converting mantissa to real mantissa"""
    real_exponent = int(exponent) + 15
    exponent_binary_converted = float_bin(real_exponent)
    sign_m, exponent_binary_converted = exponent_binary_converted.split(',')

    exponent_adjusted = 15 + int(exponent)
    exponent_adjusted = bin(exponent_adjusted)[2:]

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

    """Code for normalizing the mantissa part"""

    mantissa = mantissa[:11]
    if mantissa == '1111111111':
        mantissa = '0000000000'
    elif mantissa[10] == '1':
        b = '1'
        mantissa = bin(int(mantissa[:10], 2) + int(b, 2))[2:]

    else:
        mantissa = mantissa[:10]

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

    s = s + '1' + mantissa_c[0:10 - diff]

    smaller = sign_c + ',' + bin_exponent_d + ',' + s + ',' + exp_d
    return smaller


def normal_addition_1(smaller_mantissa, larger_mantissa, larger_exp, smaller_sign, larger_sign):

    result = bin(int(smaller_mantissa, 2) + int(larger_mantissa, 2))[2:]
    if smaller_sign == 'pos' and larger_sign == 'pos':
        if len(result) == 11:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result[1:]
        else:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result
        print('The output after adding the two numbers is {}'.format(output))
    elif smaller_sign == 'pos' and larger_sign == 'pos':
        if len(result) == 11:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result[1:]
        else:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result
        print('The output after adding the two numbers is {}'.format(output))
    elif smaller_sign == 'pos' and larger_sign == 'neg':
        if len(result) == 11:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result[1:]
        else:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result
        print('The output after adding the two numbers is {}'.format(output))
    else:
        if len(result) == 11:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result[1:]
        else:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result
        print('The output after adding the two numbers is {}'.format(output))

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

        remaining_mantissa = result_mantissa[first_one_position + 1:10]

        remaining_mantissa_length = len(remaining_mantissa)

        diff = 10 - remaining_mantissa_length

        temp_list_1 = []
        a = '0'
        for i in range(diff):
            temp_list_1.insert(i, a)

        s = ''.join(temp_list_1)
        result_normalised_mantissa = remaining_mantissa + s

        value_to_be_subtracted_from_exp = first_one_position + 1
        new_exponent = int(larger_exp) - value_to_be_subtracted_from_exp

        adjusted_new_exponent = bin(15 + new_exponent)[2:]

        adjusted_new_exponent_length = len(adjusted_new_exponent)

        diff = 5 - adjusted_new_exponent_length

        temp_list_2 = []
        a = '0'
        for i in range(diff):
            temp_list_2.insert(i, a)

        s = ''.join(temp_list_2)
        adjusted_new_exponent = s + adjusted_new_exponent

        result = adjusted_new_exponent + result_normalised_mantissa
        return result

    elif len(result) == 11:

        result_mantissa = result[1:]

        result_exponent = 15 + int(larger_exp)

        result_exponent = bin(result_exponent)[2:]

        result_exponent_length = len(result_exponent)

        diff = 5 - result_exponent_length
        temp_list = []
        a = '0'
        for i in range(diff):
            temp_list.insert(i, a)

        s = ''.join(temp_list)
        result_exponent = s + result_exponent

        result = result_exponent + result_mantissa
        return result

    else:
        result_mantissa = result

        result_mantissa_length = len(result_mantissa)
        diff = 10 - result_mantissa_length
        temp_list = []
        a = '0'
        for i in range(diff):
            temp_list.insert(i, a)

        s = ''.join(temp_list)
        result_mantissa = result_mantissa + s

        x = 0
        for x in range(10):
            if result_mantissa[x] == '1':
                break
        first_one_position = x

        remaining_mantissa = result_mantissa[first_one_position + 1:10]

        remaining_mantissa_length = len(remaining_mantissa)

        diff = 10 - remaining_mantissa_length

        temp_list_1 = []
        a = '0'
        for i in range(diff):
            temp_list_1.insert(i, a)

        s = ''.join(temp_list_1)
        result_normalised_mantissa = remaining_mantissa + s

        value_to_be_subtracted_from_exp = first_one_position + 1
        new_exponent = int(larger_exp) - value_to_be_subtracted_from_exp

        adjusted_new_exponent = bin(15 + new_exponent)[2:]

        adjusted_new_exponent_length = len(adjusted_new_exponent)

        diff = 5 - adjusted_new_exponent_length

        temp_list_2 = []
        a = '0'
        for i in range(diff):
            temp_list_2.insert(i, a)

        s = ''.join(temp_list_2)
        adjusted_new_exponent = s + adjusted_new_exponent

        result = adjusted_new_exponent + result_normalised_mantissa

        return result


def twos_complement(str):
    if str == '0000000000':
        return str
    else:

        n = len(str)

        # Traverse the string to get first
        # '1' from the last of string
        i = n - 1
        while i >= 0:
            if str[i] == '1':
                break

            i -= 1

        if i == -1:
            return '1' + str

        k = i - 1
        while k >= 0:

            # Just flip the values
            if str[k] == '1':
                str = list(str)
                str[k] = '0'
                str = ''.join(str)
            else:
                str = list(str)
                str[k] = '1'
                str = ''.join(str)

            k -= 1

        return str


def normal_addition_2(smaller_mantissa, twos_complement_mantissa, larger_exp, smaller_sign, larger_sign):
    result = bin(int(smaller_mantissa, 2) + int(twos_complement_mantissa, 2))[2:]
    if smaller_sign == 'pos' and larger_sign == 'pos':
        if len(result) == 11:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result[1:]
        else:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result

        print('The output after adding the two numbers is {}'.format(output))

    elif smaller_sign == 'pos' and larger_sign == 'pos':
        if len(result) == 11:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result[1:]
        else:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result
        print('The output after adding the two numbers is {}'.format(output))
    elif smaller_sign == 'pos' and larger_sign == 'neg':
        if len(result) == 11:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result[1:]
        else:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result
        print('The output after adding the two numbers is {}'.format(output))
    else:
        if len(result) == 11:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result[1:]
        else:
            output = '0' + ',' + bin(15 + int(larger_exp))[2:] + ',' + result
        print('The output after adding the two numbers is {}'.format(output))

    if len(result) == 11:

        result_mantissa = result[1:]

        """Normalising the mantissa part """
        result_mantissa_len = len(result_mantissa)

        s = 0
        for s in range(result_mantissa_len):
            if result_mantissa[s] == '1':
                break
        first_one_position = s

        remaining_mantissa = result_mantissa[first_one_position + 1:10]

        remaining_mantissa_length = len(remaining_mantissa)

        diff = result_mantissa_len - remaining_mantissa_length

        temp_list_1 = []
        a = '0'
        for j in range(diff):
            temp_list_1.insert(j, a)

        s = ''.join(temp_list_1)
        result_normalised_mantissa = remaining_mantissa + s

        value_to_be_subtracted_from_exp = first_one_position + 1
        new_exponent = int(larger_exp) - value_to_be_subtracted_from_exp

        adjusted_new_exponent = bin(15 + new_exponent)[2:]

        adjusted_new_exponent_length = len(adjusted_new_exponent)

        diff = 5 - adjusted_new_exponent_length

        temp_list_2 = []
        a = '0'
        for k in range(diff):
            temp_list_2.insert(k, a)

        s = ''.join(temp_list_2)
        adjusted_new_exponent = s + adjusted_new_exponent

        result = adjusted_new_exponent + result_normalised_mantissa

        return result

    else:
        result_mantissa = result  # part for taking the two's complement

        """Normalising the mantissa part """
        result_mantissa_len = len(result_mantissa)

        s = 0
        for s in range(result_mantissa_len):
            if result_mantissa[s] == '1':
                break
        first_one_position = s

        remaining_mantissa = result_mantissa[first_one_position + 1:10]

        remaining_mantissa_length = len(remaining_mantissa)

        diff = result_mantissa_len - remaining_mantissa_length

        temp_list_1 = []
        a = '0'
        for j in range(diff):
            temp_list_1.insert(j, a)

        s = ''.join(temp_list_1)
        result_normalised_mantissa = remaining_mantissa + s

        value_to_be_subtracted_from_exp = first_one_position + 1
        new_exponent = int(larger_exp) - value_to_be_subtracted_from_exp

        adjusted_new_exponent = bin(15 + new_exponent)[2:]

        adjusted_new_exponent_length = len(adjusted_new_exponent)

        diff = 5 - adjusted_new_exponent_length

        temp_list_2 = []
        a = '0'
        for k in range(diff):
            temp_list_2.insert(k, a)

        s = ''.join(temp_list_2)
        adjusted_new_exponent = s + adjusted_new_exponent

        result = adjusted_new_exponent + result_normalised_mantissa

        return result


def normal_subtraction_1(smaller_mantissa, larger_mantissa, larger_exp, smaller_sign, larger_sign):
    if smaller_sign == 'neg':

        smaller_mantissa_twos_complement = twos_complement(smaller_mantissa)

        print("Taking two's complement and adding,we have:")
        return normal_addition_2(larger_mantissa, smaller_mantissa_twos_complement, larger_exp, smaller_sign,
                                 larger_sign)
    else:

        larger_mantissa_twos_complement = twos_complement(larger_mantissa)

        print("Taking two's complement and adding,we have:")
        return normal_addition_2(smaller_mantissa, larger_mantissa_twos_complement, larger_exp, smaller_sign,
                                 larger_sign)


def stage1(a, b):
    x = float(a)
    y = float(b)

    if a == 0 and b == 0:
        print("The output answer is :000000000000000")
        return

    a_bin = float_bin(a)
    b_bin = float_bin(b)

    if a_bin == 0:
        a_bin_converted = 'pos,00000,0000000000,0'
    else:
        a_bin_converted = ieee_754_standard(convert_standard(a_bin, count_exponential(a_bin)))
    print('The number {} converted in ieee standard format after rounding the 11th bit of mantissa is {}'.format(a,
                                                                                                                 a_bin_converted))
    if b_bin == 0:
        b_bin_converted = 'pos,00000,0000000000,0'
    else:
        b_bin_converted = ieee_754_standard(convert_standard(b_bin, count_exponential(b_bin)))

    print('The number {} converted in ieee standard format after rounding the 11th bit of mantissais {}'.format(b,
                                                                                                                b_bin_converted))

    """Comparing and shifting of mantissa"""
    sign_a, binary_exponent_a, mantissa_a, exponent_a = a_bin_converted.split(',')

    sign_b, binary_exponent_b, mantissa_b, exponent_b = b_bin_converted.split(',')

    """Comparing of the exponent"""  # condition should also be written if two exponents are equal.
    if exponent_b < exponent_a:
        smaller = b_bin_converted
        larger = a_bin_converted
        adjusted_smaller_mantissa = adjust_mantissa(smaller, larger)

        smaller = adjusted_smaller_mantissa

    elif exponent_a < exponent_b:
        smaller = a_bin_converted

        larger = b_bin_converted
        adjusted_smaller_mantissa = adjust_mantissa(smaller, larger)

        smaller = adjusted_smaller_mantissa
    else:
        smaller = a_bin_converted
        larger = b_bin_converted

    print('The smaller exponent number after adjustment is {}'.format(smaller))
    print('The larger exponent number after adjustment is {}'.format(larger))

    smaller_sign, smaller_bin_exp, smaller_mantissa, smaller_exp = smaller.split(',')
    larger_sign, larger_bin_exp, larger_mantissa, larger_exp = larger.split(',')

    """Complementing number cases"""

    if smaller_sign == 'pos' and larger_sign == 'pos':

        result = '0' + normal_addition_1(smaller_mantissa, larger_mantissa, larger_exp, smaller_sign, larger_sign)

        result = result[0] + ',' + result[1:6] + ',' + result[6:]
        print('The final answer after addition and normalising is :{}'.format(result))
    elif smaller_sign == 'pos' and larger_sign == 'neg':
        result = normal_subtraction_1(smaller_mantissa, larger_mantissa, larger_exp, smaller_sign, larger_sign)
        if x + y < 0:
            sign = '1'
        else:
            sign = '0'
        result = sign + result
        result = result[0] + ',' + result[1:6] + ',' + result[6:]

        print('The final answer after addition and normalising is :{}'.format(result))
    elif smaller_sign == 'neg' and larger_sign == 'pos':
        result = normal_subtraction_1(smaller_mantissa, larger_mantissa, larger_exp, smaller_sign, larger_sign)
        if x + y < 0:
            sign = '1'
        else:
            sign = '0'
        result = sign + result
        result = result[0] + ',' + result[1:6] + ',' + result[6:]

        print('The final answer after addition and normalising is :{}'.format(result))
    elif smaller_sign == 'neg' and larger_sign == 'neg':

        result = '1' + normal_addition_1(smaller_mantissa, larger_mantissa, larger_exp, smaller_sign, larger_sign)

        result = result[0] + ',' + result[1:6] + ',' + result[6:]
        print('The final answer after addition and normalising is :{}'.format(result))
    else:
        pass


stage1(110.875, 99.185)
