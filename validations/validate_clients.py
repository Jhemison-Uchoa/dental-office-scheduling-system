from pydantic import constr

# accepts only letters and allows full names separated by a single space
NameStr = constr(min_length= 3, max_length= 50, pattern= r'^[A-Za-zá-úÁ-Ú]+( [A-Za-zá-úÁ-Ú]+)*$',
                strip_whitespace= True)


# accepts only numbers
CpfStr = constr(min_length= 11, max_length= 11, pattern= r'^[0-9]+$')
def validate_cpf(cpf: str) -> bool:

    """
    validates a brazilian cpf number using its check digit algorithm.
    raises valueError if the cpf is invalid.
    """

    # checks if the cpf has 11 repeated digits.
    if cpf == cpf[0] * 11:
        raise ValueError('invalid cpf')

    # calcule the first number cpf check digit
    weight = 10
    total_sum = 0

    for digit in cpf[:9]:
        total_sum += weight * int(digit)
        weight -= 1
    
    total_sum *= 10
    total_sum %= 11
    result = 0 if total_sum > 9 else total_sum

    
    # calcule the second number cpf check digit
    weight_digit_2 = 11
    total_sum_digit_2 = 0

    for digit in cpf[:10]:
        total_sum_digit_2 += weight * int(digit)
        weight_digit_2 -= 1

    total_sum_digit_2 *= 10
    total_sum_digit_2 %= 11
    result_digit_2 = 0 if total_sum_digit_2 > 9 else total_sum_digit_2

    if not int(cpf[9]) == result or not int(cpf[10]) == result_digit_2:
        raise ValueError('invalid cpf')
    
    return True

# accepts only numbers
PhoneNumberStr = constr(min_length = 10, max_length= 10, pattern= r'^[0-9]+$')
def validate_phone_number(phone_number: str) -> bool:

    # checks if the phone number has 10 repeated digits.
    if phone_number == phone_number[0] * 10:
        raise ValueError('invalid phone_number')
    
    return True