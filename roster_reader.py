import os
import csv
from itertools import groupby
from operator import itemgetter

path = "/Users/brandon/downloads"

writers = {}

with open(os.path.join(path, "student_rosters_Q3A.csv"), "rbU") as rosters:

    reader = csv.DictReader(rosters)
    headers = reader.fieldnames
    for row in reader:
        course = row['(Learning Center Registrations1) Class Name']
        if course not in writers:
            outfile = open(os.path.join(path, course + ".csv"), "wb")
            writers[course] = csv.DictWriter(outfile, reader.fieldnames)
            writers[course].writeheader()
        writers[course].writerow(row)
