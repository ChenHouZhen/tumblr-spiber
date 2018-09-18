import requests
import re
print("%s%s"%(66,'ddd'))

r = requests.get('https://komos666.tumblr.com/api/read')
print(r.content)
# total = re.findall('<posts start="0" total="(.*?)">',r.content)
pattern = re.compile('<posts start="0" total="(.*?)">')
total = pattern.findall(r.content.decode('utf-8'))[0]
print(total)
total =int(total)
a=[i*50 for i in range(1000) if i*50-total<0]
print(a)