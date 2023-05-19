from pytube import YouTube
import sys
import json
import struct

download_location = '/Users/Bradl/Downloads/ytdl'

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
def downloadMP4(url, loc):
    ytdl = yt.streams.get_highest_resolution()
    ytdl.download(loc)

#Download audio files and save to Downloads/audio folder
def downloadMP3(url, loc):
    ytdl = yt.streams.filter(only_audio=True).first()
    ytdl.download((loc + "/audio"))

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
            if data[0] == "mp4":
                downloadMP4(data[1], download_location)
            elif data[0] == "mp3":
                downloadMP3(data[1], download_location)
            #send success message
            sendMessage(encodeMessage("downloaded: " + receivedMessage))
        except:
            #send failure message as well as data string for fixing
            sendMessage(encodeMessage("unable to download"+ receivedMessage))
            