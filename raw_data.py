import urllib.request
import datetime
import os

for i in range(1,28):
    url="https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2024&type=Mean".format(i)
    wp = urllib.request.urlopen(url)
    text = wp.read()
    now = datetime.datetime.now()
    date_and_time_time = now.strftime("%d%m%Y%H%M%S")
    out = open(os.path.join('raw', 'NOAA_ID'+str(i)+'_'+date_and_time_time+'.csv'), 'wb')
    out.write(text)
    out.close()