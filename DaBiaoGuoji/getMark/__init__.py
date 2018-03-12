#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : __init__.py.py
# @Author: wangyx
# @Date  : 2018-03-11
# @Desc  :


from captcha.image import ImageCaptcha
from random import sample

image = ImageCaptcha() #fonts=[ "font/Xenotron.ttf"]
characters =  list("abcdefghijklmnopqrstuvwxyz")

def generate_data(digits_num, output, total):
    num = 0
    while(num<total):
        cur_cap = sample(characters, digits_num)
        cur_cap =''.join(cur_cap)
        _ = image.generate(cur_cap)
        image.write(cur_cap, output+cur_cap+".png")
        num += 1

generate_data(4, "images/four_digit/", 10000)  #产生四个字符长度的验证码
# # generate_data(5, "images/five_digit/", 10000) #产生五个字符长度的验证码
# # generate_data(6, "images/six_digit/", 10000) #产生六个字符长度的验证码
# generate_data(7, "images/seven_digit/",10000) # 产生七个字符长度的验证码