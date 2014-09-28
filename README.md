RecipeWatch
===========
RecipeWatch is exploring concepts from youtube videos with no supervision. Project is composed of following sub-modules:

- [Web Crawler](#web-crawler): A python script search youtube and wikihow and dowload videos with their subtitles if available.
- [PreProcessing](#pre-processing): A preprocessing pipeline
- [Vision Module](#vision-module): An unsupervised object clustering, feature extraction system.
- [Representation Module](#representation-module): An unsupervised representational learning system.
- [Doc](#doc): Set of documents about the project including presentation, 5 minutes pitch and papers.


##Pre Processing

#####Get the subtitles
```
pipeLine_srt.py                 Get the subtitle of the youtube videos
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

##Vision Module
```
collectHistogram.m              #Run after cpmc is done to compute histograms
cpmc_base/                      #Constrained parametric min-cut for object proposals
CoProposals/                    #Code to generate co-object proposals. For the details look at the documentation
```

