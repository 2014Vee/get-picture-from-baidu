#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 2014Vee

import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os

num = 0
numPicture = 0
file = ''
List = []


def Find(url):
    """

    :param url: 输入的下载图片url
    :return: 返回当前的搜索url下的图片url数量
    """
    global List
    print('正在检测图片总数，请稍等.....')
    t = 0
    i = 1
    s = 0
    while t < 1000:
        Url = url + str(t)
        try:
            Result = requests.get(Url, timeout=7)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Result.text
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  # 先利用正则表达式找到图片url
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s


def recommend(url):
    Re = []
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re


def dowmloadPicture(html, keyword):
    global num
    # t =0
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url
    print('找到关键词:' + keyword + ' 的图片，即将开始下载图片...')
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，图片地址:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            string = file + r'\\' + keyword + '_' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return


if __name__ == '__main__':  # 主函数入口
    # 删去了"戴黑色口罩", "戴口罩人脸", "医护人员", "医护人员戴口罩", "医生戴口罩", "戴白色口罩", "戴口罩"
    #                "戴蓝色口罩", "香港口罩事件", "明星戴口罩", "戴口罩明星", "医务人员戴口罩",
    wordAll = ["医务人员"]


    for word in wordAll:

        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&pn='
        tot = Find(url)
        Recommend = recommend(url)  # 记录相关推荐
        print('经过检测%s类图片共有%d张' % (word, tot))
        num = 0;
        numPicture = 700; # 具体一类中想取出多少图片
        # if word == "香港口罩事件":
        #     numPicture = 50;
        # elif word == "医护人员戴口罩":
        #     numPicture = 300;# 具体一类中想取出多少图片
        # else:
        #     numPicture = 200;
        file = "./face" # 存储爬取数据的文件夹
        y = os.path.exists(file)
        if y != 1:
            os.mkdir("./face")

        t = 0
        tmp = url
        while t < numPicture:
            try:
                url = tmp + str(t)
                result = requests.get(url, timeout=3) # 原来是timeout=10
                print(url)
            except error.HTTPError as e:
                print('网络错误，请调整网络后重试')
                t = t + 60
            else:
                dowmloadPicture(result.text, word)
                t = t + 60

    # # 推荐相关搜索关键词
    # print('当前搜索结束，感谢使用')
    # print('猜你喜欢')
    # for re in Recommend:
    #     print(re, end='  ')

