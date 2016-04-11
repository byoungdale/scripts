import argparse
import os

parser = argparse.ArgumentParser(description='This script uses the mergecap and editcap commandline tools that come with Wireshark to merge pcaps into one and remove duplicates')
parser.add_argument('-f','--folder', help='specify the path of the folder you have your pcaps in', required=True)
parser.add_argument('-n','--name',help='specify name you want for the completed pcap file', required=True)
args = parser.parse_args()

folder = args.folder
pcap_name = args.name
merged_pcap_name = "duplicates_{0}".format(pcap_name)

cwd = os.getcwd

if cwd != folder:
    os.chdir(folder)

for directory, subdir, files in os.walk(folder):
    for item in files:
        if item == '.DS_Store':
            files.remove(item)

print files
"\n"
pcap_string = " ".join(files)
merge_command = "mergecap -w {0} {1}".format(merged_pcap_name, pcap_string)
duplicate_command = "editcap -d {0} {1}".format(merged_pcap_name, pcap_name)
print merge_command
"\n"
print duplicate_command
"\n"
os.system(merge_command)
os.system(duplicate_command)
