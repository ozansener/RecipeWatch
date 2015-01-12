import numpy as np
from ModalDB import *
import re
import pickle

class LanguageFeatues:
  def getWordSet(self,fileName):
    SetWords = re.sub('\n','',open(fileName,'r').read())
    SetOfWords=SetWords.split(' ')
    self.wordList = SetOfWords

  def getVideoLists(self,fileName,nickNames):
    fC = open(fileName,'r').read().split('\n')
    fC.pop()
    for vN in fC:
      self.fileDic[vN]=nickNames

  def featurizeVideo(self,InputVideo):
    for frame in InputVideo.iter_children(Frame):
      self.langFeatures[str(frame)]=np.zeros(len(self.wordList))
      for w in frame['subtitles'].split():
        if w in self.wordList:
          self.langFeatures[str(frame)][self.wordList.index(w)]+=1
      if np.sum(self.langFeatures[str(frame)])>0:
        self.langFeatures[str(frame)]=self.langFeatures[str(frame)]/np.sum(self.langFeatures[str(frame)])
  def featurizeMDB(self,modal):
    self.fileDic = {}
    self.getVideoLists('howToHardBoilAnEggvideoList.txt','howToHardBoilAnEggwordList.txt')
    self.getVideoLists('howToMakeOmmelettevideoList.txt','howToMakeOmmelettewordList.txt')

    self.langFeatures = {}
    for vidd in self.fileDic:
      try:
        vid = modal.get(Video,vidd)
        if 'subtitle_file' in vid:
          self.getWordSet(self.fileDic[vidd])
          self.featurizeVideo(vid)
      except:
        print 'Error at'+vidd
    pickle.dump(self.langFeatures,open('langFeatures.bn','wb'))
