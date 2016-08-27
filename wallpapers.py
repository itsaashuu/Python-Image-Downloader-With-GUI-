from tkinter import *

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import urllib.request
import requests
import os
from bs4 import BeautifulSoup
from tkinter import *
import tkinter.messagebox
import time
import threading
import sys

root = Tk()
root.minsize(width=300, height=100)
label = Label(root, text="Enter the name")
label.grid(row=0, sticky=E)
entry = Entry(root,bd=5)
entry.grid(row=0, column = 1,sticky=E)
check = True
def makeurl(name, page):
    '''Make url of the entered name'''
    title = '-'.join(x.strip() for x in name.split(" "))
    url = 'http://www.santabanta.com/wallpapers/' + title.lower() + '/?page=' + str(page)
    return url


def makesoup(url):
    source_code = requests.get(url)
    soup = BeautifulSoup(source_code.text)
    return soup


def download(name, page):
    images = []
    if not os.path.exists(name):
        os.makedirs(name)
    soup = makesoup(makeurl(name, page))
    for item in soup.select('.wallpapers-box-300x180-2-img  > a'):
        href = "http://www.santabanta.com" + item.attrs['href'] + "?high=6"
        images.append(href)
    print(str(len(images)) + " is found")
    for i in range(len(images)):
        if check:
            soupinner = makesoup(images[i])
            for image in soupinner.findAll('img', {'id': 'wall'}):
                t = "Downloading Image" + str(i) + "..."
                print(t)
                n = os.path.join(name, name + " " + str(page) + " " + str(i) + " .jpg")
                urllib.request.urlretrieve(image.get('src'), n)

def down():
    try:
        for i in range(1, 10):
            if check:
                print("Downloading on Page" + str(i))
                if entry.get() == "":
                    tkinter.messagebox.showerror("ERROR","Name cannot be blanked")
                    break
                else:
                    tkinter.messagebox.showinfo("Downloading", "Your content is downloading. Have patience!")
                    download(entry.get(),i)
    except:
        pass

download_thread = threading.Thread()

def startDown():
    download_thread = threading.Thread(target=down)
    download_thread.start()

def stop():
    global check
    check = False
    root.destroy()
    sys.exit()



button = Button(root,bd=1,fg='green',command=startDown, text="Download")
button.grid(row=1,columnspan=4,sticky=N)

button2 = Button(root, bd=1, fg='red', command=stop, text="Stop Downloading")
button2.grid(row=2, columnspan=4)
root.mainloop()


