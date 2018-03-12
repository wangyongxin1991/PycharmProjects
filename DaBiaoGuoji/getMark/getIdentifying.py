#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : getIdentifying.py
# @Author: wangyx
# @Date  : 2018-03-12
# @Desc  : 批量获取验证码,存放到easy_img文件夹中,由于网速的的问题容易取到空的图片,
# 如果图片为空,只需要修改range里的数,重新运行程序就可以了
import urllib.request
import time
identUrl = 'http://passport.chinahr.com/m/genpic/?'

def reReadIdentify():
    for i in range(84,100):
        time.sleep(1)
        im_data = urllib.request.urlopen(identUrl).read()
        f = open('./easy_img/'+str(i)+'.png','wb')
        f.write(im_data)
        print(f)
        f.close()

reReadIdentify()