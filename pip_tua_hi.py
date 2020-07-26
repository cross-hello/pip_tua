u='https://pypi.tuna.tsinghua.edu.cn/simple'

import os
import requests as rs
from bs4 import BeautifulSoup as bs
import _thread as qd
import time


li=[]
try:
    f=open('download.log','r',encoding='utf-8')
    c=f.read()
    f.close()
    li=c.split(' ')
    c=''
except:
    pass


r=rs.Session()
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
r.headers=headers

down=[]

num=0    

try:
    ff=open('download.log','a',encoding='utf-8')
except:
    ff=open('download.log','w',encoding='utf-8')

def sido(cc):
    global num,down,ff
    num+=1
    try:
        print(cc[1]+' start download')
        html=rs.get(cc[0],headers=headers)
    except:
        down.append(cc)
        num-=1
        return 

    f=open(cc[1],'wb')
    f.write(html.content)
    f.close()
    try:
        ff.write(cc[1]+' ')
    except:
        time.sleep(0.1)
        ff.write(cc[1]+' ')
    num-=1
    return 


def download():
    global down,num,ff
    num_time=0
    while True:
        if len (down)==0 or num>60 :
            time.sleep(3)
            if num_time>=100:
                ff.close()
                ff=open('download.log','a',encoding='utf-8')
                num_time-=100

        else:
            num_time+=1
            qd.start_new(sido,(down.pop(0),))
    ff.close()

qd.start_new(download,())

print('start get html')
html=r.get(u)

print('Please wait for parsing. . .')
soup=bs(html.content,features='html.parser')
print('Parsing finish.')
lili=soup.findAll('a')
nums=0
def sig_get(a):
    global lili,r,li,down,nums
    nums+=1
    te=a.attrs['href']
    try:
        os.mkdir(te)
    except:
        pass

    url=u+r'/'+te
    print('enter url: '+url)
    try:
        html=r.get(url)
    except:
        lili.append(a)
        nums-=1
        return 
    soup=bs(html.text,features='html.parser')
    cli=soup.findAll('a')

    for aa in cli:
        name=te+aa.attrs['href'].split('/')[-1].split('#')[0]
        if name in li:
            continue
        else:
            down.append((u[:u.rfind('/')]+aa.attrs['href'][5:],name))
    nums-=1

while len(lili):
    if nums>10:
        time.sleep(3)
    else:
        qd.start_new(sig_get,(lili.pop(0),))

