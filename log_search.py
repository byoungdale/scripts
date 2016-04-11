import os
import subprocess
import sys
import argparse
import re

parser = argparse.ArgumentParser(description='filters the access and provision logs based on IP, MAC, and date/time')
parser.add_argument('-d','--directory', help='specify the directory to search', required=True)
parser.add_argument('-l','--log', help='specify the log name to search for', required=True)
parser.add_argument('-ip','--ipaddress', help='specify the customers public ip address', required=False)
parser.add_argument('-mac','--macaddress', help='specify the MAC address of a particular phone', required=False)
parser.add_argument('-d','--date', help='specify the date (YYYYMM) that you are lookin for',required=False)
args = parser.parse_args()

# assigns a variable to the result of the parser
directory = args.directory
log = args.log
ip_address = args.ipaddress
mac_address = args.macaddress
date = args.date

# find the IP address
if ip_address is not None:
    ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    grep_search = ipPattern.search(ip_address)
    grep_search = grep_search.group(0)

# find the MAC address
if mac_address is not None:
    macPattern = re.compile('[\dA-F]{2}(?:[-:][\dA-F]{2}){5}')
    grep_search = macPattern.search(mac_address)
    grep_search = grep_search.group(0)

if date is not None:
    datePattern = re.compile('(\d\d\d\d\d\d)')
    date = datePattern.search(date)
    date = date.group(0)

# assigns the current working directory to variable 'cwd'
cwd = os.getcwd()

# assigns a list of items to the contents of 'cwd'

################### THIS IS A PROBLEM #########################
# Means the script has to be run by each user from their cwd. #
# And also need to make sure that the 'os.listdir()' function #
# works with symbolic links.                                  #
###############################################################

dir_list = os.listdir(cwd)

# search through the logs
for name in dir_list:
    if directory == name:
        os.chdir(cwd + "/" + name)
        cwd = os.getcwd()
        for dirpath,dirs,files in os.walk(cwd, topdown=True, followlinks=True):
            for name in files:
                if name == '{0}.log'.format(log):
                    path_to_log = os.path.join(dirpath, name)
                    log_cmd = 'grep {0} {1}'.format(grep_search, path_to_log)
                    # run the grep command
                    os.system(log_cmd)

                if date is not None:
                    if name == '{0}{1}.log'.format(log,date):
                        path_to_date_log = os.path.join(dirpath, name)
                        date_log_cmd = 'grep {0} {1}'.format(grep_search, path_to_date_log)
                        # run the grep command
                        os.system(date_log_cmd)
