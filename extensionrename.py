#!/usr/bin/python

import os
import sys
import re
import argparse
# using progress bar lib
sys.path.append("/Users/yug/Documents/python/lib/progressbar/progressbar-2.3")
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer


level = 0

direction = "close"
if len(sys.argv) > 1:
  direction = sys.argv[1]

searchPattern = ""


extendNameDic = {
                 "via":"avi",
                 "mvw":"wmv",
                 "4mp":"mp4",
                 "sfa":"asf",
                 "pmg":"mpg",
                 "mvbr":"rmvb",
                 "mr":"rm",
                 "ivxd":"divx",
                 "kvm":"mkv",
                 "xas":"asx",
                 "3mp":"mp3",
                }

if direction != "open": 
  # the direction is to close, reverse the dictionary
  newNameDic = {}
  for keyword in extendNameDic.keys():
    valueword = extendNameDic[keyword]
    newNameDic[valueword] = keyword
  extendNameDic = newNameDic

for keyword in extendNameDic.keys():
  searchPattern += keyword
  searchPattern += "|"
searchPattern = searchPattern.rstrip('|')

def main():
  #strfilepath = os.path.realpath(__file__)
  #dir = "%s/" % (os.path.dirname(strfilepath),)


  parser = argparse.ArgumentParser(description='open/close specific filenames')
  parser.add_argument('action',
                     help='open/close the filenames')
  args = parser.parse_args()
  print args
  #print args.accumulate(args.integers)
  import pdb
  pdb.set_trace()
  dir = os.getcwd()
  print dir
  filename_list = []
  getDirList(dir, filename_list)

  renameFile(filename_list)
  print "\nmove complete\n"
  getDiskName = r"/Volumes/([^/]*)/.*$"
  greeting = "huh?"
  if direction != "open":
    print dir, getDiskName
    disknameresult = re.search(getDiskName, dir)
    if disknameresult:
      # found the disk
      diskname = disknameresult.groups()[0]
      confirm = raw_input("eject %s? [y/n]:" % diskname)
      if confirm == "y":
        cmd = "diskutil umount force '%s'" % diskname
        print "about to run: " + cmd
        os.system(cmd)
    else:
      print "not a mounted volume? exit" 
    greeting = "bye bye"
  else:
    cmd = "open ."
    os.system(cmd)
    greeting = "enjoy"
  print greeting

def getDirList( p, filename_list ):
#  print "debug: now in p:", p
  global level
  if os.path.isdir(p):
    L = os.listdir(p)
    for l in L: 
      fullname = p + "/" + l
      if(os.path.isdir(fullname)):
        #print "going into dir", fullname
        level +=1
        getDirList(fullname, filename_list)
        level -=1
      else:
        prepareFileList(fullname, level, filename_list)
  return
    

def prepareFileList(filename, level, filename_list):
  fpathandname , ftext = os.path.splitext(filename)
  global searchPattern
  global extendNameDic
  ftext = ftext.lstrip('.')
  if re.search(searchPattern, ftext, re.IGNORECASE):
    newname = fpathandname + "." + extendNameDic[ftext.lower()]
    precedingSpace = level * 2
    count = 0
    precedingString = ""
    while count < precedingSpace:
      precedingString += " "
      count +=1
    filename_list.append((filename, newname))
    #print precedingString,  "rename from", filename, "to", newname
    #os.rename(filename, newname)

def renameFile(filename_list):
  list_size = len(filename_list)
  if list_size > 0:
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=list_size).start()
    i = 0
    #import time
    for (filename, newname) in filename_list:
      #time.sleep(0.5)
      #print "from %s filename to %s" % (filename, newname)
      
      try:
        os.rename(filename, newname)
      except OSError as e:
        print "cannot rename %s to %s" % (filename, newname)
        print e
      pbar.update(i+1)
      i += 1

main()
