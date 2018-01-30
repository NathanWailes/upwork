import csv


def main(path_to_file_containing_translations):
    with open(path_to_file_containing_translations, encoding="utf8", newline="") as infile:
        lines_of_input = infile.readlines()

    lines_of_output = []
    new_line_of_output = ""

    for index, line in enumerate(lines_of_input):
        # Get rid of the newline.
        line = line.strip()

        # The first character of the first line should contain a number, e.g. "1" in "1-1".
        if index == 0:
            assert(int(line[0]))

        if index % 4 == 0:
            if index > 0:
                # Save the existing (completed) line of output before we overwrite it with the next line.
                new_line_of_output += "\n"
                lines_of_output.append(new_line_of_output)
            new_line_of_output = line + "\t"
        else:
            new_line_of_output += line + "\t"

    with open("output.tsv", "w", encoding="utf8", newline="") as outfile:
        outfile.writelines(lines_of_output)


if __name__ == "__main__":
    path_to_file_containing_translations = "input.txt"
    main(path_to_file_containing_translations)
