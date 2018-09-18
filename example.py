import requests
from threading import Thread
import queue
import re
import os
import sys
import time

api_url = 'http://%s.tumblr.com/api/read?&num=50&start='
UQueue =queue.Queue()
def getpost(uid,queue):
    url = 'http://%s.tumblr.com/api/read'%uid
    page = requests.get(url).content
    total = re.findall('<posts start="0" total="(.*?)">',page)[0]
    total = int(total)
    print(total)
    # a=[i*50 for i in range(1000) if i*50-total<0]
    # ul = api_url%uid
    # for i in a:
    #     queue.put(ul+str(i))

if __name__ == '__main__':
    name = 'stupid-slut-girl'
    getpost(name,UQueue)