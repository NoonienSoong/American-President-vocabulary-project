#!/usr/bin/env python
#!/share/apps/python/2.7.11/bin/python 
""" NOTE: use second shebang only when running on Dumbo"""

from operator import itemgetter
import sys
import collections
import re

# input comes from STDIN
for line in sys.stdin:
    pair = line.split()
    key = "".join(re.findall("[a-zA-Z]+", pair[0]))
    value = "".join(re.findall("[a-zA-Z0-9.]+", pair[1]))
    print(key, value)