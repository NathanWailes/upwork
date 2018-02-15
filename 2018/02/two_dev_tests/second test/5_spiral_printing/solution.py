# Python 3.5.2
import argparse


def solution(path_to_input_file):
    with open(path_to_input_file) as infile:
        lines_of_input = infile.readlines()

    input_array = []
    for line in lines_of_input:
        input_array.append(line.strip().split(" "))

    height = len(input_array)
    width = len(input_array[0])

    max_row_seen = height + 1
    min_row_seen = -1
    max_column_seen = width + 1
    min_column_seen = -1

    current_x_pos = 0
    current_y_pos = 0  # 0, 0 is top-left corner.

    direction_we_are_moving_in = 1  # 1 is L-->R, 2 is U-->D, 3 is R-->L, 4 is D-->U

    output_list = []

    while True:
        if current_y_pos <= min_row_seen or current_y_pos >= max_row_seen or current_y_pos >= height or\
                current_x_pos <= min_column_seen or current_x_pos >= max_column_seen or current_x_pos >= width:
            print(" ".join(output_list))
            break
        if current_y_pos == 1 and current_x_pos == 2:
            asdf = 1
        output_list.append(input_array[current_y_pos][current_x_pos])
        if direction_we_are_moving_in == 1:  # Left --> Right
            next_xpos = current_x_pos + 1
            if next_xpos < width and next_xpos < max_column_seen:
                current_x_pos = next_xpos
            else:
                direction_we_are_moving_in = 2
                min_row_seen = current_y_pos
                current_y_pos += 1
        elif direction_we_are_moving_in == 2:  # Up --> Down
            next_ypos = current_y_pos + 1
            if next_ypos < height and next_ypos < max_row_seen:
                current_y_pos = next_ypos
            else:
                direction_we_are_moving_in = 3
                max_column_seen = current_x_pos
                current_x_pos -= 1
        elif direction_we_are_moving_in == 3:  # Right --> Left
            next_xpos = current_x_pos - 1
            if next_xpos >= 0 and next_xpos > min_column_seen:
                current_x_pos = next_xpos
            else:
                direction_we_are_moving_in = 4
                max_row_seen = current_y_pos
                current_y_pos -= 1
        elif direction_we_are_moving_in == 4:  # Down --> Up
            next_ypos = current_y_pos - 1
            if next_ypos >= 0 and next_ypos > min_row_seen:
                current_y_pos = next_ypos
            else:
                direction_we_are_moving_in = 1
                min_column_seen = current_x_pos
                current_x_pos += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print a 2-D array (n x m) in spiral order (clockwise)')

    parser.add_argument('path_to_input_file', type=str)
    args = parser.parse_args()

    path_to_input_file = args.path_to_input_file

    # path_to_input_file = "./sample_input_1x1.txt"
    # path_to_input_file = "./sample_input_2x2.txt"
    # path_to_input_file = "./sample_input_3x3.txt"
    # path_to_input_file = "./sample_input_4x4.txt"
    # path_to_input_file = "./sample_input_1x5.txt"
    # path_to_input_file = "./sample_input_5x1.txt"
    solution(path_to_input_file)
