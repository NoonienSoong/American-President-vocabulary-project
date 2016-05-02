from collections import Counter
import re
import json


"""Main .py file to take clean url and generate data. This code 
creates two JSON files: presidents and all of their 
scraped speeches, and presidents and their word_count
scores."""

clean_slugs = clean_slug(url)
master_speech_list = {}
for i in clean_slugs:
    # clip president name and add as key
    pres_name = i[11:i.find('/speeches')]
    speech = get_speech(base_url + i)
    if not pres_name in master_speech_list.keys():
        master_speech_list[pres_name] = speech
    else:
        master_speech_list[pres_name].append(speech)
        
json_string = json.dumps(master_speech_list)
with open('NJ_data1.json', 'w') as fp:
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
    _president_wordcount.append((i,[float(_speech_counter_foreach)/635]))

pres_wc = dict(_president_wordcount)
with open('pres_wc.json','w') as fd:
    json.dumps(pres_wc,fd)
fd.close()
