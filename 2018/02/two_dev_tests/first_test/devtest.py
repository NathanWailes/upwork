from datetime import timedelta, datetime
import calendar


class Solutions(object):

    def greater_than_avg(self, numbers):
        average = sum(numbers) / len(numbers)
        return [number for number in numbers if number > average]

    def sort_fruit(self, fruit):
        return sorted(fruit, key=lambda x: x['count'])

    def reverse_dict(self, d):
        return {value: key for key, value in d.items()}

    def week_start_end(self, dt):
        # The datetimes below have the same hour / minute / second as the input (dt).
        first_day_of_the_week = dt - timedelta(days=dt.weekday())
        last_day_of_the_week = first_day_of_the_week + timedelta(days=6)

        # These datetimes have the correct hour / minute / second.
        start_of_the_week = datetime(first_day_of_the_week.year, first_day_of_the_week.month, first_day_of_the_week.day)
        end_of_the_week = datetime(last_day_of_the_week.year, last_day_of_the_week.month, last_day_of_the_week.day, 23,
                                   59, 59, 999999)
        return (start_of_the_week, end_of_the_week)

    def month_last_day(self, dt):
        month_range = calendar.monthrange(dt.year, dt.month)
        return month_range[1]

    def string_parse(self, text):
        list_of_tuples = []

        text_in_first_column_cell = ""
        text_in_second_column_cell = ""
        for index, line in enumerate(text.split('\n')):
            if index < 5 or index >= len(text.split('\n')) - 1 or not line:
                continue
            if line != "+------------------------------------+-----------------------------------+":
                line = line[1:-1]  # Get rid of the first and last pipe characters
                first_column_line_text, second_column_line_text = line.split("|")
                if not text_in_first_column_cell and not text_in_second_column_cell:
                    text_in_first_column_cell = first_column_line_text.strip()
                    text_in_second_column_cell = second_column_line_text.strip()
                else:
                    text_in_first_column_cell = text_in_first_column_cell + " " + first_column_line_text.strip()
                    text_in_second_column_cell = text_in_second_column_cell + " " + second_column_line_text.strip()
            else:
                list_of_tuples.append(
                    (text_in_first_column_cell.strip().decode('utf-8'), text_in_second_column_cell.strip().decode('utf-8')))
                text_in_first_column_cell = ""
                text_in_second_column_cell = ""
        return list_of_tuples

    def palindrome_test_function(self):
        def is_palindrome(string_to_check):
            string_to_check = ''.join(character.lower() for character in string_to_check if character.isalnum())

            if (string_to_check == string_to_check[::-1]):
                return True
            return False

        return is_palindrome

    def get_dynamic_classes(self, names):
        class BaseClass(object):
            def __init__(self):
                pass

            def is_the_one(self):
                return self.__class__.__name__ == "Neo"

        def get_new_class(name, BaseClass=BaseClass):
            def __init__(self):
                BaseClass.__init__(self)

            new_class = type(name, (BaseClass,), {})
            return new_class

        return [get_new_class(name) for name in names]
