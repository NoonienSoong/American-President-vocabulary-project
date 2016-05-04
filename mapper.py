#!/usr/bin/env python
#!/share/apps/python/2.7.11/bin/python
""" NOTE: use second shebang only when running on Dumbo"""

import sys
import os
import re
from collections import Counter
import json
import re
import ast

list_of_keys = ['"adams":', '"arthur":', '"bharrison":', '"buchanan":', '"bush":', '"carter":', '"cleveland":', '"clinton":', '"coolidge":', '"eisenhower":', '"fdroosevelt":', '"fillmore":', '"ford":', '"garfield":', '"grant":', '"gwbush":', '"harding":', '"harrison":', '"hayes":', '"hoover":', '"jackson":', '"jefferson":', '"johnson":', '"jqadams":', '"kennedy":', '"lbjohnson":', '"lincoln":', '{"madison":', '"mckinley":', '"monroe":', '"nixon":', '"obama":', '"pierce":', '"polk":', '"reagan":', '"roosevelt":', '"taft":', '"taylor":', '"truman":', '"tyler":', '"vanburen":', '"washington":', '"wilson":']
list_of_pres = []


""" This method converts a string that is in the proper form of a dictionary
into a dictionary using the ast"""

def convert_string_into_dict(str_in_dict_form):
    split_string = str_in_dict_form.split()
    for i in range(len(split_string)):
        if split_string[i][-1:] == ':':
            split_string[i] = '(' + '"' + ' '.join(re.findall('[a-zA-Z1-9]',split_string[i])) + '"'+','
        elif split_string[i][-2:] == '],':
            split_string[i] = ' '.join(re.findall('[a-zA-Z1-9]',split_string[i])) + ']),'
        elif split_string[i][-2:] == ']}':
            split_string[i] = ' '.join(re.findall('[a-zA-Z1-9]',split_string[i])) + '])'
    
    string_to_tuple = list(ast.literal_eval(' '.join(split_string)))
    return dict(string_to_tuple)          

def main():
    # input comes from STDIN
    all_data = sys.stdin.read()
    for i in list_of_keys:
        list_of_pres.append((i, all_data.split().index(i)))
    list_of_pres.sort(key=lambda x: x[1])   

    newlist = all_data.split()
    for k in range(len(all_data.split())):
        if newlist[k] in list_of_keys:
            newlist[k] = "@"

    # Create list of speeches divided by special character "@"
    squiggly = " ".join(newlist).split("@")
    squiggly = squiggly[1:]

    # Get total word count for normalization
    total_wc = 0
    for m in range(len(squiggly)):
        total_wc += len(squiggly[m].split())


    for n in range(len(list_of_keys)):
        uniq = len(Counter(squiggly[n].split()))
        # Normalize and emit
        print(list_of_keys[n], float(uniq)/total_wc)      


if __name__ == "__main__":
    main()

