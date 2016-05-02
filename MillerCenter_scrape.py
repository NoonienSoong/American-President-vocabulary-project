import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from collections import Counter
import re
import urllib2

""" Grab all links from the website"""
url = 'http://millercenter.org/president/speeches'
base_url = 'http://millercenter.org'  
def get_all_slugs(url):
    http = httplib2.Http()
    status, response = http.request(url)
    list_of_links = []
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        if link.has_attr('href'):
            list_of_links.append(link['href'])
    return list_of_links



""" filter all the links such that it returns all of the 
 slugs that we are interested in. Make sure you are
 using the correct base url (millercenter.org/president/speeches)"""
def clean_slug(url):
    list_of_slugs = get_all_slugs(url)
    clean_slugs = []
    for i in list_of_slugs:
        if i.find('president') == 1 and i.find('/speech-') > 0:
            clean_slugs.append(str(i))
    return set(clean_slugs)
""" grab the speech from specific url + slug 
 clean it remove all html etc.."""


def get_speech(url_plus_slug):
    cleanest_speech  = []
    html = urllib2.urlopen(url_plus_slug).read()
    soup = BeautifulSoup(html)
    speech = soup.find('div',{'id':'transcript'})
    stripped_speech = str(speech.get_text().encode('utf-8')).split()
    clean_speech = [ i for i in stripped_speech if re.match('[a-zA-Z]',i)]
    cleanest_speech.append(' '.join(clean_speech))
    return cleanest_speech
