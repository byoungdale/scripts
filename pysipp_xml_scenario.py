# This script will generate a XML document that can be used with the pysipp library to run a basic UAC scenario

# PROBLEM: the saxutil library doesn't seem to be able to unescape the lt& and gt& symbols

from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree, TreeBuilder
import xml.sax.saxutils as saxutils
import datetime
# in order to prettify the XML
from bs4 import BeautifulSoup

generated_on = str(datetime.datetime.now())

scenario = Element('scenario')
scenario.set('name','Basic Sipstone UAC')

sendINVITE = SubElement(scenario,'send')
sendINVITE.set('retrans','500')

#
sendINVITE.text = "\n<![CDATA[\
      INVITE sip:[service]@[remote_ip]:[remote_port] SIP/2.0\
      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]\
      From: sipp <sip:sipp@[local_ip]:[local_port]>;tag=[pid]SIPpTag00[call_number]\
      To: sut <sip:[service]@[remote_ip]:[remote_port]>\
      Call-ID: [call_id]\
      CSeq: 1 INVITE\
      Contact: sip:sipp@[local_ip]:[local_port]\
      Max-Forwards: 70\
      Subject: Performance Test\
      Content-Type: application/sdp\
      Content-Length: [len]\
      v=0\
      o=user1 53655765 2353687637 IN IP[local_ip_type] [local_ip]\
      s=-\
      c=IN IP[media_ip_type] [media_ip]\
      t=0 0\
      m=audio [media_port] RTP/AVP 0\
      a=rtpmap:0 PCMU/8000\
    ]]\n>"

recv100 = SubElement(scenario,'recv')
recv100.set('response','100')
recv100.set('optional','true')

recv180 = SubElement(scenario,'recv')
recv180.set('response','180')
recv180.set('optional','true')

recv183 = SubElement(scenario,'recv')
recv183.set('response','183')
recv183.set('optional','true')

recv200 = SubElement(scenario,'recv')
recv200.set('response','200')
recv200.set('optional','true')

sendACK = SubElement(scenario,'send')
sendACK.text = "<![CDATA[\
      ACK sip:[service]@[remote_ip]:[remote_port] SIP/2.0\
      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]\
      From: sipp <sip:sipp@[local_ip]:[local_port]>;tag=[pid]SIPpTag00[call_number]\
      To: sut <sip:[service]@[remote_ip]:[remote_port]>[peer_tag_param]\
      Call-ID: [call_id]\
      CSeq: 1 ACK\
      Contact: sip:sipp@[local_ip]:[local_port]\
      Max-Forwards: 70\
      Subject: Performance Test\
      Content-Length: 0\
    ]]>"

pause = SubElement(scenario,'pause')
pause.set('milliseconds','2000')

sendBYE = SubElement(scenario,'send')
sendBYE.set('retrans','500')
sendBYE.text = "<![CDATA[\
      BYE sip:[service]@[remote_ip]:[remote_port] SIP/2.0\
      Via: SIP/2.0/[transport] [local_ip]:[local_port];branch=[branch]\
      From: sipp <sip:sipp@[local_ip]:[local_port]>;tag=[pid]SIPpTag00[call_number]\
      To: sut <sip:[service]@[remote_ip]:[remote_port]>[peer_tag_param]\
      Call-ID: [call_id]\
      CSeq: 2 BYE\
      Contact: sip:sipp@[local_ip]:[local_port]\
      Max-Forwards: 70\
      Subject: Performance Test\
      Content-Length: 0\
    ]]>"

recv200_to_BYE = SubElement(scenario,'send')
recv200_to_BYE.set('response','200')
recv200_to_BYE.set('crlf','true')

response_time = SubElement(scenario,'ResponseTimeRepartition')
response_time.set('value','10, 20, 30, 40, 50, 100, 150, 200')

call_length = SubElement(scenario,'CallLengthRepartition')
call_length.set('value','10, 50, 100, 500, 1000, 5000, 10000')

# saxutil keeps giving the error
# "AttributeError: 'Element' object has no attribute 'replace'"
# so I think there is a bug in the saxutil library

#scenario = saxutils.unescape(scenario)

xml_string = tostring(scenario,'ISO-8859-1', method="xml")
string_scenario = BeautifulSoup(xml_string,"xml",).prettify("ISO-8859-1")

scenario_file = open('uac_basic.xml','wb')
scenario_file.write(string_scenario)
print("You're xml file has been saved")
