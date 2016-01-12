DISCLAIMER
==========
We are currently in the process of cleaning/documenting the code hence we advise everyone to wait for the relase. For the brave ones, the code is here. In order to use it you also need ModalDB https://github.com/ozansener/ModalDB and push all your data and features into it.

RecipeWatch
===========
RecipeWatch is exploring concepts from youtube videos with no supervision. Project is composed of following sub-modules:

- [src/Crawler](#web-crawler): A python module which can search youtube and wikihow and download videos with their subtitles if available.
- [src/Settings](#settings): Set of parameters and settings used by the entire project. It also includes ModalDB schema etc.
- [Scripts](#scripts): Python scripts mostly for data crunching/processing.
- [Doc](#doc): Documents about the project including presentation, 5 minutes pitch and papers.





- [PreProcessing](#pre-processing): A preprocessing pipeline
- [Vision Module](#vision-module): An unsupervised object clustering, feature extraction system.
- [ML Module](#ml-module): An unsupervised representational learning system.


#Pre Processing

#####Get the subtitles
```
pipeLine_extractSrt.py          Read the SRT/*.srt files and crete python dict
```

#####Extract frames
```
pipeLine_frames.py              #Extract frames from video files
pipeLine_md5summary.py          #Get the md5 summary of all frames
```

#####Process saceled ones
```
pipeLine_scaledSrt.py           #Convert srt to scaled file srt
```

#####Extract srt
```
pipeLine_histLang.py            #Get the histograms of the language
```
#####Resize
```
pipeLine_scale.py               #Resize frames for cpmc
pipeLine_cpmc.py                #Create the folder structure for cpmc code
pipeLine_hist.py                #Create .mat file with the list of frames
```

#Vision Module
```
collectHistogram.m              #Run after cpmc is done to compute histograms
cpmc_base/                      #Constrained parametric min-cut for object proposals
CoProposals/                    #Code to generate co-object proposals. For the details look at the documentation
```

#ML Module

#Doc
```
ProjectLog/                      #Beamer presentation about the project
ProjectPitch/                    #5 mins pitch of the project
```
