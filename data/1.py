import os
import sys

for line in sys.stdin:
    userid = line.strip().split('\t')[0]
    url = "http://192.168.87.10:9999/?userid=" + userid + "&itemid=6326709127"
    print url
