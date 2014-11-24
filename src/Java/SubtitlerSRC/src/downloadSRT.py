import sys,getopt,os

def main(argv):
    link = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hl:o:",["link=","ofile="])
    except getopt.GetoptError:
        print 'dowloadSRT.py -l <link> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'dowloadSRT.py -l <link> -o <outputfile>'
            sys.exit()
        elif opt in ("-l", "--link"):
            link = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print JAVA Command:,'java -cp ../lib/commons-io-2.4.jar:../lib/jdom.jar:. Ozan '+link+' '+outputfile
    os.system('java -cp ../lib/commons-io-2.4.jar:../lib/jdom.jar:. Ozan '+link+' '+outputfile)

    print 'Link file is "', link
    print 'Output file is "', outputfile

if __name__ == "__main__":
    print sys.argv[1:] 
    main(sys.argv[1:])

