#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import os

class FileFlips:
  def __init__(self, root, direction):
    self.root = root
    filemap = FileFlips.initMap(direction)
    self.filename_list = FileFlips.prepareFileList(self.root, filemap)

  def renameFiles(self, renameComplete=None):
    list_size = len(self.filename_list)
    if list_size > 0:
      #pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=list_size).start()
      
      i = 0
      #import time
      for (filename, newname) in self.filename_list:
        #time.sleep(0.5)
        #print "from %s filename to %s" % (filename, newname)
        
        try:
          os.rename(filename, newname)
        except OSError as e:
          print "cannot rename %s to %s" % (filename, newname)
          print e
        if renameComplete is not None:
          renameComplete(i)
        #pbar.update(i+1)
        i += 1
  
  def get_length(self):
    return len(self.filename_list)
    
  @staticmethod
  def prepareFileList(dir, filemap):
    filename_list = []
    p = dir

    if os.path.isdir(p):
      L = os.listdir(p)
      for l in L: 
        fullname = p + "/" + l
        if(os.path.isdir(fullname)):
          filename_list.extend(FileFlips.prepareFileList(fullname, filemap))        
        else:
          (filename, file_extension) = os.path.splitext(fullname)
          ext = file_extension.lstrip(".")
          if ext in filemap:
            src2tgt = (fullname, "%s.%s" % (filename, filemap[ext]))
            filename_list.append(src2tgt)
          
    return filename_list
  @staticmethod
  def initMap(direction):
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
    return extendNameDic

  