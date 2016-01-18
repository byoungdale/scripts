import requests
import json
import getpass
import re

#######################################################################
# this program takes the username and password for a sms api          #
# and sends the inputted text message to and from the numbers given.  #
# This script will reformat the numbers to the standard +1xxxxxxxxxx  #
#######################################################################

# the necessary variables for the functions and the api
username = raw_input('USERNAME: ')
password = getpass.getpass('PASSWORD: ')
sms=raw_input('ENTER MESSAGE HERE: ')
to_number = raw_input('ENTER NUMBER YOUR ARE TEXTING TO: ')
from_number = raw_input('ENTER YOUR API NUMBER: ')

# assigns num_format to the number that is input into the fixphonenumber function
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

# this procedure uses the requests library to talk to the api
def send_sms(to_number,from_number,username,password,sms):
    # calls the fixphonenumber function on the numbers inputted in to_number and from_number variables
    destination = fixphonenumber(to_number)
    phonecomnumber = fixphonenumber(from_number)

    # here is where requests talks to the sms api
    sms_messege = json.dumps({"from":phonenumber,"to":destination,"message":sms}, sort_keys=True,indent=4)
    print "Sending text to {0} from {1}....\n".format(destination, phonecomnumber)
    p = requests.post('[api url]', auth=(username, password), data=sms_messege)
    json_response = p.json()
    if p.status_code == 200:
        unique_identifier = json_response[u'response'][u'data'][u'resource_id']
        g = requests.get('[api url]'.format([api unique identified]), auth=(username, password))
        print "Text successfully sent! See more info below:\n"
        print json_response
        print g.json()
    else:
        print "An error occurred. See below:\n"
        print json_response

# this procedure reformats numbers that are given in '(xxx) xxx-xxxx' OR ten or eleven digits (without '+')
def fixphonenumber(number):
    correct_format = num_format.search(number)
    # assign all the necessary groups from the regex to variables in order to reformat into correct number for api
    number, addition_plus, start_parenthesis, area_code, end_parenthesis, separator1, nxx, separator2, last_four = correct_format.groups()
    # checks if the '+1' is already on the number and adds it if not
    if addition_plus:
        return "{0}{1}{2}{3}".format(addition_plus, area_code, nxx, last_four)
    else:
        return "+1{0}{1}{2}".format(area_code, nxx, last_four)

# run the send_sms function to get everything started
send_sms(to_number,from_number,username,password,sms)
