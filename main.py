import xml.etree.ElementTree as ET
from requests import get
import json
import sys


# Check if cmd args
if len(sys.argv) > 2:
    Safe_Share_Link=sys.argv[1]
    Time_Stamp_Option=sys.argv[2]
else:
    Safe_Share_Link=input('Safe Share URL: ')
    Time_Stamp_Option=int(input("Time Stamp or Large Paragraph (0 or 1): "))



Transcript=""
if 'https://safesha.re' in Safe_Share_Link:
    Video_ID=get(Safe_Share_Link).url.replace('https://safeshare.tv/x/','')
else:
    Video_ID=Safe_Share_Link.replace('https://safeshare.tv/x/','')




HTML_Data=get(f'https://www.youtube.com/watch?v={Video_ID}',headers={'Accept-Language': 'en-US'}).text
Split_HTML=HTML_Data.split('"captions":')
XML_Transcript_URL = json.loads(Split_HTML[1].split(',"videoDetails')[0].replace('\n', '')).get('playerCaptionsTracklistRenderer')['captionTracks'][0]['baseUrl']


XML_Transcript=get(XML_Transcript_URL).text
XML_Root = ET.fromstring(XML_Transcript)
for Root_Line in XML_Root.findall('text'):
    if Time_Stamp_Option==0:
        Time_Stamp=float(Root_Line.attrib['start'])
        minutes,seconds = divmod(Time_Stamp, 60)
        Time_Stamp_String = "{:02}:{:02}".format(int(minutes), int(seconds))
        Transcript+=Time_Stamp_String+' '+Root_Line.text.replace('&#39;',"'")+'\n'
    else:
        Transcript+=Root_Line.text.replace('&#39;',"'")+' '
print(Transcript)