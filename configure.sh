#=====[ Make sure python can find ModalDB ]=====
export PYTHONPATH=$PYTHONPATH:`pwd`/src/
export CLASSPATH=$CLASSPATH:`pwd`/src/Java/Subtitle.jar:`pwd`/src/Java/commons-io-2.4.jar:`pwd`/src/Java/jdom.jar


export PROJECT_DIR=`pwd`
export DATA_DIR=`pwd`/data

export MONGODB_DBPATH=`pwd`/data/db

#===[ Add Caffe to Path ]===
export CAFFE_ROOT_PATH=/home/ozan/caffe
export PYTHONPATH=$PYTHONPATH:$CAFFE_ROOT_DIR/python
