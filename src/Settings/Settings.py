from ModalDB import *
from scipy.io import loadmat, savemat
from scipy.misc import imread, imsave
import pysrt
import cPickle

data_dir =  '/home/ozan/ModalData/'
#Push them to the ModalDB
my_schema = ModalSchema({
    # Frames consist of an image (stored on disk) and accompanying subtitles (stored in memory)
    Frame:  {
                'image':{
                            'mode':'disk',                   # store it on disk, instead of mongodb
                            'filename':'image.png',          # filename to store data under
                            'load_func':lambda p: imread(p), # how to load from disk. (p = path to file)
                            'save_func':lambda x, p: imsave(p, x) # how to save to disk, when set. (optional)
                        },
              'image_scaled':{
                          'mode':'disk',                   # store it on disk, instead of mongodb
                          'filename':'image_scaled.jpg',          # filename to store data under
                          'load_func':lambda p: imread(p), # how to load from disk. (p = path to file)
                          'save_func':lambda x, p: imsave(p, x) # how to save to disk, when set. (optional)
                      },
                'subtitles':{
                            'mode':'memory'
                            }
            },

    # Videos contain subtitles, which we can store in memory (mongodb) as strings.
    Video:  {
                'thumbnail':{
                                'mode':'disk',
                                'filename':'thumbnail.png',
                                'load_func':lambda p: imread(p),
                                'save_func':lambda x, p: imsave(p, x)
                            },
                'title':{
      'mode':'memory'
    },
    'FPS':{
      'mode':'memory'
    },
    'subtitle_file':{
      'mode':'disk',
      'filename':'sub.srt',
      'load_func':lambda p:pysrt.open(p, encoding='iso-8859-1'),
                        'save_func':lambda x, p: p
    },
                # Videos also contain collections of 'Frame' dataobjects (defined below)
                'contains':[Frame]
            }
})
