number_of_baskets_sold = 0


def get_the_pulse_value_to_send_to_the_dc_motor():
    pulse_values_ordered_according_to_each_row_of_baskets = [0, 10, 20, 30]
    index_to_use = get_the_current_row_of_baskets_to_expose()
    return pulse_values_ordered_according_to_each_row_of_baskets[index_to_use]


def get_the_current_row_of_baskets_to_expose():
    return get_the_number_of_rows_of_baskets_sold()


def get_the_number_of_rows_of_baskets_sold():
    global number_of_baskets_sold
    return number_of_baskets_sold / 6


if __name__ == '__main__':
    global number_of_baskets_sold
    number_of_baskets_sold = 7
    print(get_the_pulse_value_to_send_to_the_dc_motor())
