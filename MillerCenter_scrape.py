


#Nicholaus Jackson 05/03/2016
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from collections import Counter
import re
import nltk
import json
import urllib2
import matplotlib.pyplot as plt
import buildStopWordPattern as bsw
import ast
import numpy
plt.rcParams['axes.grid'] = True
plt.rcParams['figure.figsize'] = 11,7
get_ipython().magic(u'matplotlib inline')



"""This code is meant to be an R&D step for a larger Hadoop analytic.It scrapes 
http://millercenter.org/president/speeches and gathers speeches from all U.S. presidents it then
presents the presidents word count in a scatter plot with a fitted regression line. This set of functions
also produces two .json files(NJ_data.json and pres_wc.json) these files contain a json file with presidents
as a key and their speeches (with keywords stripped) as values and a file with presidents as keywords and their
unique word count as values respectivley."""



def loadStopWords(stopWordFile):
    stopWords = []
    for line in open(stopWordFile):
        if (line.strip()[0:1] != "#"):
            for word in line.split( ): #in case more than one per line
                stopWords.append(word)
    return stopWords


def buildStopwordRegExPattern(pathtostopwordsfile):
      stopwordlist = loadStopWords(pathtostopwordsfile)
      stopwordregexlist = []
      for wrd in stopwordlist:
          wrdregex = '\\b' + wrd + '\\b'
          stopwordregexlist.append(wrdregex)
      stopwordpattern = re.compile('|'.join(stopwordregexlist), re.IGNORECASE)
      return stopwordpattern



# Grab all links from the website
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
    clean_speech = [ ]
    stop_words = buildStopwordRegExPattern('stopwords.txt')
    for i in stripped_speech:
        clean_speech.append(re.sub(stop_words,'|',i))
        
    cleanest_speech.append( ' '.join(' '.join(clean_speech).split('|')))
    return cleanest_speech, len(' '.join(cleanest_speech).split())



"""Main take clean url and generate data. This code 
creates two JSON files: presidents and all of their 
scraped speeches, and presidents and their word_count
scores."""

clean_slugs = clean_slug(url)
master_speech_list = {}
total_word_count = 0
for i in clean_slugs:
    # clip president name and add as key
    pres_name = i[11:i.find('/speeches')]
    speech , one_speech_wc = get_speech(base_url + i)
    if not pres_name in master_speech_list.keys():
        master_speech_list[pres_name] = speech
    else:
        master_speech_list[pres_name].append(speech)
    total_word_count += one_speech_wc
        
json_string = json.dumps(master_speech_list)
with open('NJ_data.json', 'w') as fp:
    json.dump(master_speech_list, fp)
fp.close()
    
_president_wordcount = []
for i in master_speech_list.keys():
    _speech_counter_foreach = 0
    for k in range(len(master_speech_list[i])): 
        if k == 0:
            _speech_counter_foreach += len(Counter(master_speech_list[i][k].split()))
        else:
            _speech_counter_foreach += len(Counter(master_speech_list[i][k][0].split()))
            #append president name as key and normalized wordcount
    _president_wordcount.append((i,[float(_speech_counter_foreach)/total_word_count]))

pres_wc = dict(_president_wordcount)
with open('pres_wc.json','w') as fd:
    json.dumps(pres_wc,fd)
fd.close()



wc_array = [pres_wc.values()[i][0] for i in range(len(pres_wc.keys()))]
order_array = [pres_wc.values()[i][1] for i in range(len(pres_wc.keys()))]


plt.scatter(order_array,wc_array,marker='*',s=60)
plt.plot(order_array, numpy.poly1d(numpy.polyfit(order_array, wc_array, 1))(order_array),'r--')
plt.ylim = [0,max(wc_array)]
plt.xlim = [0,max(order_array)]
plt.xlabel('presidents',fontsize=20)
plt.ylabel('weighted unique word count',fontsize=20)
plt.axis('tight')
plt.show()

