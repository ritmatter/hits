import sys
import urllib
import json
import urllib2
from bs4 import BeautifulSoup
import requests

def get_top_40():
    page = requests.get('http://www.bigtop40.com/chart/archive/2015/33/').text
    page_soup = BeautifulSoup(page)
    uls = page_soup.select(".chart_list")

    # HTML structure slightly different for some pages
    ul = uls[0]
    lis = ul.select("li")

    i = 1
    for li in lis:

        if li.h3.a:
            title = li.h3.a.find(text=True, recursive=False)
        else:
            title = li.h3.find(text=True, recursive=False)
        artist = li.h3.span.text

        artist = artist.replace("by", "").strip()
        title = title.replace("by", "").strip()
        print str(i) + "," + title + "," + artist
        i += 1

get_top_40()
