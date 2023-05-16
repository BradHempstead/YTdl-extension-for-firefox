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

def sendMessage(encodedMessage):
    sys.stdout.buffer.write(encodedMessage['length'])
    sys.stdout.buffer.write(encodedMessage['content'])
    sys.stdout.buffer.flush()

while True:
    receivedMessage = getMessage()
    if receivedMessage == "ping":
        sendMessage(encodeMessage("pong"))
    else:
        try:
            link = receivedMessage
            yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
            ytdl = yt.streams.get_highest_resolution()
            ytdl.download(download_location)
            sendMessage(encodeMessage("downloaded: " + receivedMessage))
        except:
            sendMessage(encodeMessage("unable to download"))