from pytube import YouTube
import sys

download_location = '/Users/Bradl/Downloads/ytdl'


link = sys.argv[1]
yt = YouTube(link)

print("title: ", yt.title)

print("Views: ", yt.views)

ytdl = yt.streams.get_highest_resolution()

ytdl.download(download_location)