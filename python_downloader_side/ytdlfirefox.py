from pytube import YouTube
import sys
import json
import struct
import subprocess

download_location = 'C:/Users/Bradl/Downloads/ytdl'
#Specify whether to download mp3 or not (0 = no, 1 = just mp3, 2 = mp3 and mp4 audio)
mp3download=2

#Read a message from stdin and decode
def getMessage():
    rawLength = sys.stdin.buffer.read(4)
    if len(rawLength) == 0:
        sys.exit(0)
    messageLength = struct.unpack('@I', rawLength)[0]
    message = sys.stdin.buffer.read(messageLength).decode('utf-8')
    return json.loads(message)

#encode a message for transmission
def encodeMessage(messageContent):
    encodedContent = json.dumps(messageContent, separators=(',',':')).encode('utf-8')
    encodedLength = struct.pack('@I', len(encodedContent))
    return {'length': encodedLength, 'content': encodedContent}

#Send response over native messaging api
def sendMessage(encodedMessage):
    sys.stdout.buffer.write(encodedMessage['length'])
    sys.stdout.buffer.write(encodedMessage['content'])
    sys.stdout.buffer.flush()

#download the highest available video resolution and save to the defined location (default /Downloads)
def downloadVideo(url, loc):
    ytdl = yt.streams.get_highest_resolution()
    ytdl.download(loc)

#Download audio files and save to Downloads/audio folder
def downloadAudio(url, loc):
    ytdl = yt.streams.filter(only_audio=True).first()
    ytdl.download((loc + "/audio"))
    if mp3download == 2:
        file_in = str(loc + "/audio/" + yt.title + ".mp4")
        file_out = str(loc + "/audio/" + yt.title + ".mp3")
        subprocess.run('ffmpeg -i "'+ file_in + '" "' + file_out + '"', shell=False)

#mainloop
while True:
    #Retrieve data from browser and store as variable
    receivedMessage = getMessage()
    #Test code to check nativemessaging works. To remove/edit later
    if receivedMessage == "ping":
        sendMessage(encodeMessage("ping recieved"))
    #Parse data and attempt download
    else:
        try:
            #create list of variables from data string (might change separator)
            data = receivedMessage.split(" ")
            #create the youtube data variable and use oauth for permissions
            yt = YouTube(data[1], use_oauth=True, allow_oauth_cache=True)
            #parse selection and download as appropriate
            if data[0] == "video":
                downloadVideo(data[1], download_location)
            elif data[0] == "audio":
                downloadAudio(data[1], download_location)
            #send success message
            sendMessage(encodeMessage("downloaded: " + yt.title))
        except:
            #send failure message as well as data string for fixing
            sendMessage(encodeMessage("unable to download: "+ receivedMessage))
            