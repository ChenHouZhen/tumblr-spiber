# -*- coding=utf-8 -*-
from threading import Thread
import queue
import requests
import re
import os
import sys
import time


api_url='http://%s.tumblr.com/api/read?num=50&start='
UQueue=queue.Queue()
def getpost(uid,queue):
    url='http://%s.tumblr.com/api/read?num=50'%uid
    r = requests.get(url)
    page=r.content
    print(r.url)
    print(r.content)
    # total=re.findall('<posts start="0" total="(.*?)">',page)[0]
    pattern = re.compile('<posts start="0" total="(.*?)">')
    total = pattern.findall(page.decode('utf-8'))[0]
    total=int(total)
    a=[i*50 for i in range(1000) if i*50-total<0]
    ul=api_url%uid
    for i in a:
        queue.put(ul+str(i))


extractpicre = re.compile(r'(?<=<photo-url max-width="1280">).+?(?=</photo-url>)',flags=re.S)   #search for url of maxium size of a picture, which starts with '<photo-url max-width="1280">' and ends with '</photo-url>'
extractvideore=re.compile('/tumblr_(.*?)" type="video/mp4"')

video_links = []
pic_links = []
vhead = 'https://vt.tumblr.com/tumblr_%s.mp4'

class Consumer(Thread):

    def __init__(self, l_queue):
        super(Consumer,self).__init__()
        self.queue = l_queue

    def run(self):
        session = requests.Session()
        while 1:
            link = self.queue.get()
            print('start parse post: ' + link)
            try:
                content = session.get(link).content
                videos = extractvideore.findall(content.decode('utf-8'))
                video_links.extend([vhead % v for v in videos])
                pic_links.extend(extractpicre.findall(content.decode('utf-8')))
            except:
                print('url: %s parse failed\n' % link)
            if self.queue.empty():
                break


def main():
    task=[]
    for i in range(min(10,UQueue.qsize())):
        t=Consumer(UQueue)
        task.append(t)
    for t in task:
        t.start()
    for t in task:
        t.join
    while 1:
        for t in task:
            if t.is_alive():
                continue
            else:
                task.remove(t)
        if len(task)==0:
            break


def write():
    videos=[i.replace('/480','') for i in video_links]
    pictures=pic_links
    with open('pictures.txt','w') as f:
        for i in pictures:
            f.write('%s\n'%i)
    with open('videos.txt','w') as f:
        for i in videos:
            f.write('%s\n'%i)


if __name__=='__main__':
    #name=sys.argv[1]
    #name=name.strip()
    name='haha321fan'
    getpost(name,UQueue)
    main()
    write()