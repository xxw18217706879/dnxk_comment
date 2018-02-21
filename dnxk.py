# -*- coding: utf-8 -*-
import json
import threading
import os
import requests
import codecs
import base64
from Crypto.Cipher import AES
import pymongo
from config import *

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]
table=db[MONGO_TABLE]

client = pymongo.MongoClient('localhost', 27017)
db = client['test']


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    # print(type(text))
    #  print(type(pad))
    #  print(type(pad * chr(pad)))
    #  text = text + str(pad * chr(pad))
    if isinstance(text, bytes):
      # print("type(text)=='bytes'")
        text = text.decode('utf-8')
    text = text + str(pad * chr(pad))
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def rsaEncrypt(text, pubKey, modulus):
   text = text[::-1]
   rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
   return format(rs, 'x').zfill(256)

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'

def createSecretKey(size):
   return (''.join(map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]


def get_info(page):
    text = {
        'rid': '',
        'offset': page*20,
        'total': 'false',
        'limit':'20',
        'csrf_token':''

    }
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {
            'params':encText,
            'encSecKey':encSecKey
    }
    headers = {
        'Accept':'*/*',
        'Connection':'keep-alive',
        'Content-Length':'20',
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    try:
        proxy_=proxy()
        print(proxy_)
        proxies={"http":'http://'+proxy_}#使用代理
        response = requests.post('http://music.163.com/weapi/v1/resource/comments/R_SO_4_531051217?csrf_token=', headers=headers, data=data, proxies=proxies,timeout=10)
        if response.status_code==200:
            print(proxies)
            return response.text
        else:
            print("请求网页失败!",proxy_)
            return get_info(page)
    except Exception as e:
        print(e)
        return get_info(page)

def proxy():
    response=requests.get('http://api.logicjake.xyz/get_proxy/?_action=getIP&validcode=xuxiaowu')
    if response.status_code==200:
        response_proxy=response.text
        response_proxy=json.loads(response_proxy)
        if response_proxy['code']==0:
            ip_port=response_proxy['data']
            proxy_=ip_port['IP']+":"+ip_port['PORT']
            return proxy_






def parse_json(json_text,page):
    try:
        if json_text:
            json_text=json.loads(json_text)
            json_comments=json_text["comments"]
            for json_comment in json_comments:
                dic1={}
                dic1['userId']=json_comment['user']['userId']
                dic1['avatarUrl']=json_comment['user']['avatarUrl']
                dic1['nickname']=json_comment['user']['nickname']
                dic1['time']=json_comment['time']
                dic1['commentId']=json_comment['commentId']
                dic1['likedCount']=json_comment['likedCount']
                dic1['content']=json_comment['content']
                Replied_lists=json_comment['beReplied']
                if Replied_lists:
                    list_replied=[]
                    dic={}
                    dic['replied_total']=len(Replied_lists)
                    for Replied_list in Replied_lists:
                        dic2={}
                        dic2['replied_userId']=Replied_list['user']['userId']
                        dic2['replied_avatarUrl']=Replied_list['user']['avatarUrl']
                        dic2['replied_nickname']=Replied_list['user']['nickname']
                        dic2['replied_content']=Replied_list['content']
                        list_replied.append(dic2)
                        #print(list_replied)
                        dic['replied_information']=list_replied
                    dic1['beReplied']=dic
                    #print(dic1)
                #save_to_mongo(dic1,page)
                print(dic1)
    except Exception as e:
        print(e)
        return parse_json(json_text,page)

def save_to_mongo(result,page):
    try:
        if result:
            if table.insert(result):
                print('插入数据成功!',result)
    except Exception as e:
        print('插入失败!')
        print(e)



def main(start,end):
    for page in range(start,end):
        json_text=get_info(page)
        parse_json(json_text,page)
        th=threading.current_thread()
        print("线程{}完成爬取第{}页!".format(th.getName(),str(page+1)))
    th=threading.current_thread()
    print("线程{}结束工作!".format(th.getName(),str(page)))


if __name__=="__main__":
    threadpool=[]
    for i in range(1):
        start=i*100+500
        end=i*100+501
        th =threading.Thread(target=main,name="线程"+str(i),args=(start,end))
        threadpool.append(th)
        print("线程{}开始爬取{}-{}页!".format(str(i),str(start),str(end)))
        th.start()
    for th in threadpool:
        threading.Thread.join(th)



