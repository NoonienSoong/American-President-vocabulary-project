


#Nicholaus Jackson 05/02/2016
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import urllib2
import re
import json
from collections import Counter
import matplotlib.pyplot as plt
plt.rcParams['axes.grid'] = True
plt.rcParams['figure.figsize'] = 11,16
get_ipython().magic(u'matplotlib inline')



"""This is very similiar to the Miller Center scrape (Miller_scrape.py) this code however describes a set of 
functions that scrape http://www.presidency.ucsb.edu/ (The American Presidency project) for a specific case study
This code is mean to act as a R&D step for a larger hadoop program. These funcitons look at two presidential elecitons
one in 1960 and one in 2016, it then scrapes all speeches and remarks given by all candidates and does a weighted unique
word count. One the data is munged and compiled the results are displayed in a bar graph"""



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



def get_all_slugs(url):
    http = httplib2.Http()
    status, response = http.request(url)
    list_of_links = []
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        if link.has_attr('href'):
            list_of_links.append(link['href'])
    return list_of_links



def clean_slug(url):
    list_of_slugs = get_all_slugs(url)
    clean_slugs = []
    for i in list_of_slugs:
        if  i.find('/ws/index') > 0:
            clean_slugs.append(str(i)[2:])
    return set(clean_slugs)



def get_speech(url_plus_slug):
    word_count_of_speech = 0
    cleanest_speech  = []
    html = urllib2.urlopen(url_plus_slug).read()
    soup = BeautifulSoup(html)
    speech = soup.find(class_='displaytext')
    stripped_speech = str(speech.get_text().encode('utf-8')).split()
    clean_speech = [ ]
    stop_words = buildStopwordRegExPattern('stopwords.txt')
    for i in stripped_speech:
        clean_speech.append(re.sub(stop_words,'|',i))
        word_count_of_speech +=1
        
    cleanest_speech.append( ' '.join(' '.join(clean_speech).split('|')))
    return cleanest_speech, word_count_of_speech



def genterate_dictionary_raw_and_wcScore(base_url,url,name):
    
    clean_slugs = clean_slug(url)
    master_speech_list = {}
    total_word_count = 0
    for i in clean_slugs:
        # clip president name and add as key
        pres_name = name
        speech , one_speech_wc = get_speech(base_url + i)
        if not pres_name in master_speech_list.keys():
            master_speech_list[pres_name] = speech
        else:
            master_speech_list[pres_name].append(speech)
        total_word_count += one_speech_wc
        
    
    _president_wordcount = []
    for i in master_speech_list.keys():
        _speech_counter_foreach = 0
        for k in range(len(master_speech_list[i])): 
            if k == 0:
                _speech_counter_foreach += len(Counter(master_speech_list[i][k].split()))
            else:
                _speech_counter_foreach += len(Counter(master_speech_list[i][k][0].split()))
            #append president name as key and normalized wordcount
        _president_wordcount.append((i,[_speech_counter_foreach]))
    return master_speech_list, dict(_president_wordcount), total_word_count



base_url = 'http://www.presidency.ucsb.edu'
url = ['http://www.presidency.ucsb.edu/1960_election_speeches.php?candidate=35',
       'http://www.presidency.ucsb.edu/1960_election_speeches.php?candidate=37'
       ,'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=70&campaign=2016CLINTON&doctype=5000',
      'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=115&campaign=2016TRUMP&doctype=5001']
names = ['kennedy','nixon','hclinton','trump']


global_wc = 0
global_pres_wc = []
for i in range(len(names)):
    master_speech_list, pres_wc,tot_wc = genterate_dictionary_raw_and_wcScore(base_url,url[i],names[i])
    global_wc += tot_wc
    global_pres_wc.append(pres_wc)



#plotting
global_dict_wc = dict([(key,d[key]) for d in global_pres_wc for key in d])


for i in range(len(global_dict_wc.keys())):
    global_dict_wc[global_dict_wc.keys()[i]] = float(global_dict_wc.values()[i][0])/global_wc

colors = ['#624ea7', 'g', 'yellow', 'k', 'maroon']
plt.bar(range(len(global_dict_wc.keys())),global_dict_wc.values(),align='center',color=colors)
plt.xticks(range(len(global_dict_wc.keys())),global_dict_wc.keys())
plt.xlabel('presidents')
plt.ylabel('weighted unique word count')

