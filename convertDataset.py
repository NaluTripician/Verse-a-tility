import os


n = 0
for sub,dir,files in os.walk("Dataset/"):
    for filename in files:
        if filename.endswith(".mp3"):

            command = "ffmpeg -i \'" + sub + "/" + filename +"\' \'" + sub + "/" + filename[:-4] + ".wav\'"
            os.system(command)
