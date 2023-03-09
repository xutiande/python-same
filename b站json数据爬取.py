import io
import sys
import time

import pymysql
import requests
from hyper.contrib import HTTP20Adapter
from jsonpath import jsonpath
from lxml.html import etree
from selenium import webdriver
from selenium.webdriver.common.by import By




def connectMysql(sql, data):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='bilibili',port=3306)
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    conn.close()
video_list = []

# 获取up主视频的aid cid title放入列表中
def get_video_cid(mid):
    # 获取视频页数
    headers={
        ':authority':'api.bilibili.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
        'cookie': "buvid3=5BF0595D-9D7B-A2B9-BA9F-C94B3584C4A239152infoc; b_nut=1676272639; i-wanna-go-back=-1; _uuid=3D39C727-C134-109E4-4E1D-AAE1110F4B56B39422infoc; buvid_fp=27117bcd5ed2d5d71fcae76b57324c64; buvid4=E07FD6DC-674B-CA8D-C8FD-ECFE50B1CC3040148-023021315-fVKL0MvuC8W3aI2VA3PSDw==; nostalgia_conf=-1; CURRENT_FNVAL=4048; rpdid=|(J|k))k|Ym)0J'uY~Yk~kYY); SESSDATA=a94e162b,1691824741,9a964*21; bili_jct=03dafa40b9214d5843f80c1d5ec34eb1; DedeUserID=518448814; DedeUserID__ckMd5=d2faf82d4584395a; CURRENT_QUALITY=80; b_ut=5; header_theme_version=CLOSE; PVID=1; b_lsid=110910BFDD_186969F358A; bp_video_offset_518448814=767609311425724400; sid=e0vybtcm; innersign=0; home_feed_column=5; bsource=search_bing"
    }

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
    url = 'https://api.bilibili.com/x/space/navnum?mid={}&jsonp=jsonp'.format(mid)
    sessions=requests.session()
    sessions.mount('https://api.bilibili.com',HTTP20Adapter())
    response_up = sessions.get(url,headers=headers)
    up_json = response_up.json()
    pages = int(up_json.get('data').get('video')) // 30 + 1
    # 循环调用接口 每次页数不同
    # for i in range(1, pages + 1):
    for i in range(1, 2):
        main_api = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn={}&order=pubdate&jsonp=jsonp'.format(mid, i)
        brower=webdriver.Chrome()
        brower.get(main_api)
        time.sleep(2)
        get_test=brower.find_element(By.XPATH,'/html/body/pre').text
        false = False
        true = True
        null = ''
        txt={}
        txt.update(eval(get_test))
        content_list=jsonpath(txt,'$..vlist')[0]
        print(content_list)
        count = 0
        for content in content_list:
            detail_api = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(jsonpath(content,'$..aid')[0])
            response_detail = requests.get(detail_api)
            detail_dict = response_detail.json()
            count += 1
            # 视频信息列表中元素
            video_dict = dict()
            video_dict['aid'] = detail_dict.get('data').get('aid')
            video_dict['cid'] = detail_dict.get('data').get('cid')
            video_dict['title'] = detail_dict.get('data').get('title')
            print(video_dict)
            video_list.append(video_dict)
            time.sleep(1)
            for video in video_list:
                get_save_dm(video, table_name)
            a=1
# 根据cid以及弹幕接口获取到相关视频的弹幕
def get_save_dm(video_dict, table_name):
    """
    :param video_dict: 视频信息字典
    :return: None
    """
    time.sleep(1)
    aid = video_dict.get('aid')
    cid = video_dict.get('cid')
    title = video_dict.get('title')
    # 该接口返回的是XML数据
    dm_api = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)
    response = requests.get(dm_api)
    response.encoding = 'utf-8'
    # 解析XML
    tree = etree.HTML(response.content)
    dm_list = tree.xpath("//d/text()")
    for dm in dm_list:
        dm_str = str(dm)
        try:
            sql = 'INSERT test(aid, cid, title, dm_content) VALUES(%s, %s, %s, %s)'
            connectMysql(sql, (aid, cid, title, dm_str))
        except Exception as e:
            print(dm_str, "获取失败")
            print(e)
            continue
        else:
            print(dm_str, "获取成功")

if __name__ == '__main__':
    mid = 125526
    table_name = 'dm_' + '-LKs-'
    get_video_cid(mid)
