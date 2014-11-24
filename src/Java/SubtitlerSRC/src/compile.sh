rm -f *.class
javac -cp ../lib/commons-io-2.4.jar:../lib/jdom.jar:. SubtitleDownload.java Network.java Converter.java Common.java NetSubtitle.java SRTFilter.java TableModel.java XMLFilter.java 2>abc.txt

