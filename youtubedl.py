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
        print "Usage %s [Youtube URL]" % (sys.argv[0])
        sys.exit(1)
    yt = YouTube(sys.argv[1])
    i=1
    quals={}
    #TODO offer most common options maybe? e.g. only 720p,1080p,mp3,ogg
    #TODO add convertion to mp3 (from best video quality)
    for st in yt.streams.filter(type='video').filter(subtype='mp4').all():
        quals[i]=st
        res = st.resolution
        if not res:
            res = st.res
        if hasattr(st,'quality'):
            qual = st.quality
        if hasattr(st,'quality_label'):
            qual = st.quality_label
        print "["+str(i)+"] ["+str(res)+"] [ Quality: "+str(qual)+"]"
        i+=1
    #TODO Add auto and verbose mode (argparse, -q 720p , -v, -u url or just [url])
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
