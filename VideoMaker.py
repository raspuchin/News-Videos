#!/usr/bin/env python
# coding: utf-8
# @Author : Sachin Pothukuchi
# @Github: raspuchin

from gtts import gTTS
import os
from random import randint
from mutagen.mp3 import MP3
from time import sleep


def clear_temp():
    os.system('rm temp/audio/*')
    os.system('rm temp/images/*')
    os.system('rm temp/video/*')

def get_speech(summary):
    tts = gTTS(text=summary)
    tts.save('temp/audio/temp.mp3')

def get_images(keywords):
    i = 1
    for keyword in keywords:
        x = randint(1,5)
        copy_name = keyword.replace(' ', '_') + str(x) + '.jpeg'
        paste_name = 'temp-' + str(i) + '.jpeg'
        os.system('cp images/'+copy_name+' temp/images/'+paste_name)
        sleep(0.1)
        i += 1

def get_video():
    os.system('ffmpeg -y -framerate 0.5 -i temp/images/temp-%d.jpeg -vf "scale=\'min(320,iw)\':\'min(180,ih)\'" -sws_flags bilinear temp/video/output.mp4')
    sleep(0.5)

def makeVideo(summary, keywords, heading):
    get_speech(summary)
    get_images(keywords)
    get_video()
    
    os.system('ffmpeg  -stream_loop -1 -i temp/video/output.mp4 -i temp/audio/temp.mp3 -shortest -map 0:v:0 -map 1:a:0 -y temp/video/uncut.mp4')
    sleep(0.5)
    os.system('ffmpeg -y -i temp/video/uncut.mp4 -ss 00:00:00 -t 00:00:31 -async 1 -strict -2 -max_muxing_queue_size 1000 outputs/singles/'+heading+'.mp4')
    sleep(0.5)
    
    print(heading+'.mp4 is ready')
    
    #clear_temp()