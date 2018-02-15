# Python 3.5.2
import argparse

from math import sqrt


def solution(path_to_input_file):
    with open(path_to_input_file) as infile:
        lines_of_input = infile.readlines()

    assert(len(lines_of_input) == 2)

    data = []
    for line in lines_of_input:
        numbers = [float(number_as_string) for number_as_string in line.split(" ")]
        xpos = numbers[0]
        ypos = numbers[1]
        radius = numbers[2]
        data.append({'xpos': xpos, 'ypos': ypos, 'radius': radius})

    x0 = data[0]['xpos']
    x1 = data[1]['xpos']

    y0 = data[0]['ypos']
    y1 = data[1]['ypos']

    r0 = data[0]['radius']
    r1 = data[1]['radius']

    # Math below from https://stackoverflow.com/a/42803692/4115031

    d = sqrt(pow((x1 - x0), 2) + pow((y1 - y0), 2))
    a = (pow(r0, 2) - pow(r1, 2) + pow(d, 2)) / (2 * d)
    h = sqrt(pow(r0, 2) - pow(a, 2))
    x2 = x0 + a * (x1 - x0) / d
    y2 = y0 + a * (y1 - y0) / d

    x3 = x2 + h * (y1 - y0) / d
    x4 = x2 - h * (y1 - y0) / d

    y3 = y2 - h * (x1 - x0) / d
    y4 = y2 + h * (x1 - x0) / d

    print(x3, y3)

    if x3 != x4:  # If the two circles are tangent, the two solutions will be identical (and thus x3 will equal x4).
        print(x4, y4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find all intersections of two defined circles')

    parser.add_argument('path_to_input_file', type=str)
    args = parser.parse_args()

    path_to_input_file = args.path_to_input_file

    # path_to_input_file = "./sample_input.txt"

    solution(path_to_input_file)
