#!/usr/bin/env python
# coding: utf-8
# @Author: Sachin Pothukuchi
# @Github: raspuchin

from VideoMaker import makeVideo, clear_temp
from GettingImages import getImage
from KeywordExtraction import load, getKeywordList
import os
from time import sleep


load() #run only once


def run(summary, heading):
    keywords = getKeywordList(summary)
    print('Keywords: ' + str(keywords))
    getImage(keywords)
    makeVideo(summary, keywords, heading)
    sleep(10)
    clear_temp()


head = ''
summ = ''
print('Headline: '+head)
print('Summary: '+summ)
run(summ,head)

