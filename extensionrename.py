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

from model import FileFlips

def main():
  #strfilepath = os.path.realpath(__file__)
  #dir = "%s/" % (os.path.dirname(strfilepath),)


  parser = argparse.ArgumentParser(description='open/close specific filenames')
  parser.add_argument('action',
                     help='open/close the filenames')
  parser.add_argument('--test',
                     help='test run only')
  parser.add_argument('--dir',
                     help='the working directory')

  args = parser.parse_args()
  print args
  #print args.accumulate(args.integers)
  dir = os.getcwd()
  if args.dir:
    dir = args.dir
  print dir
  filename_list = []
  direction = args.action
  ff = FileFlips(dir,direction)

  if args.test:
    print ff.filename_list
  else:
    list_size = ff.get_length()
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=list_size).start()
    ff.renameFiles(pbar.update)
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
    cmd = "open %s" % dir
    os.system(cmd)
    greeting = "enjoy"
  print greeting


main()
