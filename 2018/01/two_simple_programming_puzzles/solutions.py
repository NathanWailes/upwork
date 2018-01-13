

def get_max_nonpositive_integer_in_list(list_of_integers):
    nonpositive_integers = [integer for integer in list_of_integers if integer < 1]  # Get rid of all the integers greater than 0

    sorted_nonpositive_integers = sorted(nonpositive_integers)  # Sort the non-positive integers from least to greatest (ex: [-3, -2, -1, 0])

    max_nonpositive_integer = sorted_nonpositive_integers[-1]  # Grab the last element (the one closest in value to 0).

    return max_nonpositive_integer


def fizzbuzz(number_to_print_up_to):
    output = ""
    for i in range(1, number_to_print_up_to + 1):
        new_output = ""
        if i % 3 == 0 or i % 5 == 0 or i % 7 == 0:
            if i % 3 == 0:
                new_output += "Fizz"
            if i % 5 == 0:
                new_output += "Buzz"
            if i % 7 == 0:
                new_output += "Woof"
        else:
            new_output += str(i)

        output += new_output

        if i < number_to_print_up_to:
            output += " "  # Add a space to separate this output from the output for the next number.

    print(output)


if __name__ == '__main__':
    list_of_integers = [-3, -2, -1, 0, 1]
    print(get_max_nonpositive_integer_in_list(list_of_integers))
    fizzbuzz(24)
