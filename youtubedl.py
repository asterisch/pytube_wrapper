#!/usr/bin/python
from pytube import YouTube
import sys
import time 

vsize = 0
def percent(tem, total):
        perc = (float(tem) / float(total)) * float(100)
        return perc

def progress_function(chunk, file_handle, bytes_remaining):

    global vsize
    p = 0
    progress = p
    p = percent(vsize-bytes_remaining, vsize)
    file_handle.write(chunk)
    print('%.1f%s \r' % (p,"%")),

def main():
    if len(sys.argv) < 2:
        print "Usage ./%s [Youtube URL]" % (sys.argv[0])
        sys.exit(1)
    yt = YouTube(sys.argv[1])# on_progress_callback=progress_function)
    i=0
    quals={}
    for st in yt.streams.filter(subtype='mp4').all():
        quals[i]=st
        print "["+str(i)+"] "+str(st)
        i+=1
    ch = -1
    while ch not in quals.keys():
        try:
            ch = int(raw_input("Select quality: "))
        except Exception as e:
            print(e.message)
            pass
    vst = yt.streams.get_by_itag(quals[ch].itag)
    vst.on_progress=progress_function
    global vsize
    vsize = vst.filesize
    vst.download()
    print("[+] %s %.1fMD" % (vst.default_filename, (float(vst.filesize)/float(1024))/float(1024) ))

if __name__ == "__main__":
    main()
