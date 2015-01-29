'''
My problem:
    I was spending 3-4 hours clickig through our information system export
    inidivudal course rosters that I needed to mailmerge with our reports. Even
    after finding out how to export all course rosters into one spreadsheet, I
    still needed to parse through the CSV file because it was HUGE! 

My solution:
    I wrote this script to iterate through the CSV file and everytime the
    Course Title changed in the spreadsheet, write that data to a new
    spreadsheet with it's title set to the Course Title in the large file's
    column. After asking for help on Stackoverflow:
    
    https://stackoverflow.com/questions/28181647/how-do-i-make-the-filename-of-the-output-csv-file-equal-to-the-the-content-of-a/28182236#28182236

    I was able to write up this script that accomplished the task. Saving me
    tons of time. Maybe it someone else has a huge file they need separated,
    they will find this useful as a guide.

Next steps:
    Next, I want to take those new files, and mailmerge them into corresponding
    Word Documents based on title.
'''
import os
import csv
from itertools import groupby
from operator import itemgetter

path = "/Users/brandon/downloads"

# open empty list to store course fields in
writers = {}

# open the CSV file and attach it to the rosters variable
with open(os.path.join(path, "student_rosters.csv"), "rbU") as rosters:

    #set reader equal to the Dictionart content of the rosters (i.e. the CSV file)
    reader = csv.DictReader(rosters)
        # read through the rows of the file and set course variable equal to
        # the course title
        for row in reader:
            course = row['(Learning Center Registrations1) Class Name']
            # adds the course content to the writers list if it isn't there yet
            if course not in writers:
                # if the course isn't added yet, this creates a new CSV file that
                # takes the course's title as it's name
                outfile = open(os.path.join(path, course + ".csv"), "wb")
                # the 'course' key is set equal to the output of the outfile
                writers[course] = csv.DictWriter(outfile, reader.fieldnames)
            # each row of the outfile is written to course, which is then added
            # to the corresponding file that was created
            writers[course].writerow(row)
