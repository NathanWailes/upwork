# Python 3.5.2
import argparse

from math import sqrt


def solution(path_to_input_file):
    with open(path_to_input_file) as infile:
        lines_of_input = infile.readlines()

    number_of_locations = int(lines_of_input[0])
    current_location_to_next_location = {}

    for index, line in enumerate(lines_of_input[1:]):
        current_location_to_next_location[str(index)] = line.strip()

    seen_locations = set()

    number_of_cycles = 0

    for starting_location in current_location_to_next_location.keys():
        if starting_location in seen_locations:
            continue
        else:
            locations_seen_on_this_trip = set()
            locations_seen_on_this_trip.add(starting_location)

            next_location = current_location_to_next_location[starting_location]

            while next_location != "-1" and next_location not in seen_locations:
                locations_seen_on_this_trip.add(next_location)
                next_location = current_location_to_next_location[next_location]
                if next_location in locations_seen_on_this_trip:  # This should only happen when there's a cycle.
                    number_of_cycles += 1
                    break

            seen_locations = seen_locations.union(locations_seen_on_this_trip)

    print(number_of_cycles)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find number of cycles in list of nodes')

    parser.add_argument('path_to_input_file', type=str)
    args = parser.parse_args()

    path_to_input_file = args.path_to_input_file

    # path_to_input_file = "./sample_input.txt"
    # path_to_input_file = "./sample_input_3_cycles.txt"
    # path_to_input_file = "./sample_input_1_cycle_with_locations_pointing_to_it.txt"
    # path_to_input_file = "./sample_input_no_cycles.txt"

    solution(path_to_input_file)
