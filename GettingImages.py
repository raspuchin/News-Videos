#!/usr/bin/env python
# coding: utf-8
# @Author : Sachin Pothukuchi
# @Github: raspuchin

from selenium import webdriver
from time import sleep
import base64
import os
import re
import sys

WEBDRIVER_PATH = ''
IMAGES_PATH = ''
extensions = {'jpg', 'jpeg', 'png'}

def getImageFromGoogle(keywords):
    driver = webdriver.Chrome(WEBDRIVER_PATH)

    for keyword in keywords:
        #getting the page with the images for the keywords
        sleep(1)
        url = "https://www.google.co.in/search?q="+keyword.replace(' ','+')+"&source=lnms&tbm=isch&tbs=sur:fc,isz:lt,islt:xga,ift:jpg"
        driver.get(url)

        #loading the images
        imges = driver.find_elements_by_css_selector('img.rg_i.Q4LuWd.tx8vtf')
        count = 1
        for img in imges:
            #save each image to file
            img_data = img.get_attribute('src').split(',')
            raw_img = base64.b64decode(img_data[1])
            img_type = img_data[0][(img_data[0].find('/') + 1) : img_data[0].find(';')]
            if img_type not in extensions:
                img_type = 'jpg'
            with open(IMAGES_PATH + keyword.replace(' ', '_') + str(count) + '.' + img_type, 'wb') as f:
                f.write(raw_img)
            print('Downloaded Image '+str(count)+' for '+keyword)
            count += 1
            if count > 5:
                break

    driver.close()

def checkIfImageExists(keyword):
    for img_name in os.listdir(IMAGES_PATH):
        if img_name.split('.')[0][:-1] == keyword.replace(' ', '_'):
            print(keyword + ' already present.')
            return True
    return False

def getImage(keywords):
    keywords_to_get = []
    for keyword in keywords:
        if not checkIfImageExists(keyword):
            keywords_to_get.append(keyword)
    if not keywords_to_get == []:
        getImageFromGoogle(keywords_to_get)

