import re

def find_numbers(number_file):
    number_list = []

    with open(number_file, 'r') as f:
        for line in f:
            if line is not '':
                # regex to find numbers in line
                num_format = re.compile(r'''(
                    (\+[1])?                # +1xxxxxxxx numbers
                    (\()?                   # open parenthesis
                    (\d{3})                 # area code
                    (\))?                   # close parenthesis
                    (\s|-|\.)?              # separator
                    (\d{3})                 # first 3 digits
                    (\s|-|\.)?              # separator
                    (\d{4})                 # last 4 digits
                    )''', re.VERBOSE)
                # matches line with num_format; will be None if no match is found
                number = num_format.match(line)
                
                if number is not None:
                    # assign all the necessary groups from the regex to variables in order to reformat into correct number for api
                    number, addition_plus, start_parenthesis, area_code, end_parenthesis, separator1, nxx, separator2, last_four = number.groups()
                    # checks if the '+1' is already on the number and adds it if not
                    if addition_plus:
                        number_list.append("{0}{1}{2}{3}".format(addition_plus, area_code, nxx, last_four))
                    else:
                        number_list.append("+1{0}{1}{2}".format(area_code, nxx, last_four))

    print(number_list)
    print("number_list.length={0}".format(len(number_list)))

find_numbers('[number list file]')
