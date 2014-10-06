import ggplot
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt

from bokeh.plotting import *


def plotHistogramMeans(hist,fileName):
  num_clust = hist.shape[0]
  IDS = np.mat(range(0,num_clust))
  IDS = IDS.reshape(num_clust,1)

  histD = np.concatenate((IDS,hist),axis=1)

  Data = pd.DataFrame(histD,columns = ['ID']+range(0,hist.shape[1]))
  Melted = pd.melt(Data,id_vars=['ID'])
  pv =  ggplot.ggplot( ggplot.aes(x='variable',y='value'),data=Melted) +  ggplot.geom_line()  + ggplot.facet_wrap("ID")
  print "Saving mean histograms"
  ggplot.ggsave(pv,'./IMG/'+fileName)

def saveVideos(VidL):
  for i in range(len(VidL)):
    VIDD = np.concatenate((VidL[i][0],VidL[i][1]),axis=1)
    plt.imshow(VIDD,interpolation='nearest',aspect='auto')
    plt.savefig('./IMG/'+'vid'+str(i)+'.pdf')

def saveAverageVideo(ids,means,VidL,pre):
  cur = 0
  for j in range(len(VidL)):
    VV = np.zeros((1,means.shape[1]))
    for i in range(cur,cur+VidL[j][0].shape[0]):
      VV=np.concatenate((VV,means[ids[i],:].reshape(1,means.shape[1])),axis=0)
    cur = cur + VidL[j][0].shape[0]
    plt.imshow(VV[1:,:],interpolation='nearest',aspect='auto')
    plt.savefig('./IMG/'+pre+'aver_vid'+str(j)+'.pdf')

def plotSetOfArrays(arrays,names,fileName):
  IDS = np.linspace(0,1,arrays[0].shape[0])
  A = IDS.reshape(arrays[0].shape[0],1)
  for i in range(0,len(arrays)):
    A = np.concatenate((A,arrays[i]),axis=1)
  Data = pd.DataFrame(A,columns = ['noise']+names)
  Melted = pd.melt(Data,id_vars=['noise'])

  pv = ggplot.ggplot(ggplot.aes(x='noise', y='value', colour='variable'), data=Melted) +  ggplot.geom_line() + ggplot.geom_point()
  ggplot.ggsave(pv,'./IMG/'+fileName)

  output_file("iou_scores.html", title="correlation.py example")

  figure(tools="pan,wheel_zoom,box_zoom,reset,previewsave")
  hold()
  line(IDS, arrays[0][:,0], color='#A6CEE3', legend=names[0])
  line(IDS, arrays[1][:,0], color='#1F78B4', legend=names[1])
  line(IDS, arrays[2][:,0], color='#B2DF8A', legend=names[2])
  line(IDS, arrays[3][:,0], color='#33A02C', legend=names[3])

  curplot().title = "Minimum IOU"
  grid().grid_line_alpha=0.3
  show()
