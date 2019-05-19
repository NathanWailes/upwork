def main():
    continuum_length = 300
    # [beginning, length, value]
    annotations = [
        [
            (150, 30, 0),
            (180, 60, 1),
            (240, 60, 0),
            (300, 50, 1),
            (350, 100, 0),
        ],
        [
            (150, 30, 0),
            (180, 60, 1),
            (240, 60, 0),
            (300, 50, 1),
            (350, 100, 0),
        ]
    ]
    number_of_identified_units = get_number_of_identified_units(annotations)
    print("Number of identified units: %d" % number_of_identified_units)
    print(get_expected_disagreement(continuum_length, annotations, number_of_identified_units))


def get_number_of_identified_units(annotations):
    number_of_identified_units = 0
    for annotator_index in range(len(annotations)):
        for (beginning, length, value) in annotations[annotator_index]:
            if value == 1:
                number_of_identified_units += 1
    return number_of_identified_units


def get_expected_disagreement(continuum_length, annotations, number_of_identified_units):
    numerator = get_numerator(continuum_length, annotations, number_of_identified_units)
    denominator = get_denominator(continuum_length, annotations)
    return numerator / denominator


def get_numerator(continuum_length, annotations, number_of_identified_units):
    first_term = 2 / continuum_length
    number_of_annotators = len(annotations)

    outer_double_summation = 0
    for annotator_index in range(number_of_annotators):
        for (beginning, length, value) in annotations[annotator_index]:
            if value:
                outer_double_summation += value * get_value_in_angled_brackets(annotations, number_of_identified_units, length)
    return first_term * outer_double_summation


def get_value_in_angled_brackets(annotations, number_of_identified_units, outer_annotation_length):
    first_term = (number_of_identified_units - 1) / 3
    second_term = 2 * pow(outer_annotation_length, 3) - 3 * pow(outer_annotation_length, 2) + outer_annotation_length
    first_product = first_term * second_term

    inner_double_summation = 0
    for annotator_index in range(len(annotations)):
        for (inner_annotation_beginning, inner_annotation_length, inner_annotation_value) in annotations[annotator_index]:
            if inner_annotation_length >= outer_annotation_length:
                inner_double_summation += (1 - inner_annotation_value) \
                                           * (inner_annotation_length - outer_annotation_length + 1)

    second_product = pow(outer_annotation_length, 2) * inner_double_summation
    return first_product + second_product


def get_denominator(continuum_length, annotations):
    number_of_annotators = len(annotations)

    first_term = number_of_annotators * continuum_length
    second_term = first_term - 1

    third_term = 0
    for annotator_index in range(number_of_annotators):
        for (beginning, length, value) in annotations[annotator_index]:
            third_term += value * length * (length - 1)

    return (first_term * second_term) - third_term


if __name__ == '__main__':
    main()
