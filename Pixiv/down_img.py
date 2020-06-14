import requests
import json
import re
import os
from threading import Thread
from queue import Queue
from io import BytesIO
from PIL import Image
import time
import random

#获取该画师id
def find_artistid(artistName):
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.97Safari / 537.36'
    }
    url = 'https://api.pixivic.com/artists?artistName={}&page=1&pageSize=30'.format(artistName, idqueue)
    response = requests.get(url, headers=headers)
    str_json = json.loads(response.content.decode())
    for i in range(30):
        name = str_json['data'][i]['name']
        if name == artistName:
            id = str_json['data'][i]['id']
            idqueue.put(id)


#获取画师下所有作品id
def find_imgid(artid,queue):
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.97Safari / 537.36'
    }

    page = 1
    while True:
        url = 'https://api.pixivic.com/artists/{}/illusts/illust?page={}&pageSize=30&maxSanityLevel=10'.format(artid, page)
        response = requests.get(url, headers=headers)
        str_json = json.loads(response.content.decode())
        page += 1
        for i in range(30):
            try:
                id = str_json['data'][i]['id']
                queue.put(id)
            except:
                id = 0
                pass
        if id == 0:
            break


#url网站   path数据保存路径
def download_images(queue):
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.97Safari / 537.36'
    }
    while not queue.empty():
        url = 'https://api.pixivic.com/illusts/{}'.format(queue.get())
        response = requests.get(url, headers=headers)
        str_json = json.loads(response.content.decode())
        #取到地址,画师名，标题
        artist_name = str_json['data']['artistPreView']['name']
        title = str_json['data']['title']
        dir_name = artist_name.replace('/', '.')
        try:
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
        except:
            print('创建文件目录出错，目录名称出现特殊符号*|:?/<>')
        try:
            # 可能有多张图片
            for u in range(len(str_json['data']['imageUrls'])):
                #原图尺寸
                # img = str_json['data']['imageUrls'][u]['original']
                #下载大尺寸
                img = str_json['data']['imageUrls'][u]['large']
                string = re.findall(r'net/(.*)', img)
                true_img = 'http://wq.boxpaper.club/' + string[0]
                #间隔
                time.sleep(random.random())
                a_img = requests.get(true_img, headers=headers).content
                image = Image.open(BytesIO(a_img))
                true_title = title + str(u)
                image.convert('RGB').save(dir_name + '/' + true_title + '.jpg')
                print('下载成功:', title)
        except:
            print('下载： '+true_title + ' 出现异常！！！')
            pass


if __name__ == "__main__":
    queue = Queue()
    idqueue = Queue()
    while True:
        type_id = input("选择根据名字 or id 进行下载（1 or 2）")
        if type_id == '1':
            artistName = input("请输入画师名称")
            find_artistid(artistName)
            break
        elif type_id == '2':
            artist_id = input("请输入画师id")
            idqueue.put(artist_id)
            break

    while not idqueue.empty():
        artid = idqueue.get()
        getImg_thread = Thread(find_imgid(artid, queue))
        getImg_thread.daemon = True
        getImg_thread.start()

        #创建线程
        for x in range(10):
            download_thread = Thread(download_images(queue))
            #守护线程
            download_thread.daemon = True
            download_thread.start()
        #当队列为空时，退出线程
        queue.join()
        print('下载完毕')