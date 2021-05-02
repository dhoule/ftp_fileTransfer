#!/usr/bin/python3
from ftplib import FTP
import os
import sys
import datetime
import time
import logging

currentDT = datetime.datetime.now()
# Create a log file of the current transaction
logging.basicConfig(filename='C:\\example.log',level=logging.DEBUG)
x = 0
y = 0 
logging.info(currentDT.strftime("\n\n%d %b %Y"))

def getFile(ftp, filename, localPath):
    try:
        global x
        localfile = open(localPath + filename, 'wb')
        ftp.retrbinary("RETR " + filename ,localfile.write)
        localfile.close()
        x += 1
    except:
        global y
        localfile.close()
        os.remove(localPath + filename)
        logging.error("Error on file %s, Error: %s" % (filename, sys.exc_info()[0]) )
        y += 1

# lcd C:\Users\others\Desktop\prestashop_photos\new_images
# get all files; excluding '.' & '..'; in absolute path given. Returns a List of strings
localDir = "local\directory\goes\here"
lFiles = os.listdir(localDir)

ftp = FTP('host.server.here','username','password')     # connect to host, default port
# cd to needed directory
ftp.cwd('needed/directory/goes/here')
# get all files in current directory on server
files = ftp.nlst()

# Determine what files exist on the FTP server, but not in the local directory
difference = list(set(files) - set(lFiles)) 

for i in difference:
    getFile(ftp, i, localDir + '\\')
    time.sleep(0.05)

logging.info("\n\nFiles completed: %d \tFiles errored: %d\n\n" % (x,y) )

ftp.quit()