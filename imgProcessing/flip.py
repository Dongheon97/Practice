# image up-down flip, left-right flip 
from PIL import Image
import os

path = "/Users/dongheon97/Desktop/dataset/4"

file_list = os.listdir(path)
# Check image file
print(file_list)

dstPath = path + "/output"
if dstPath not in os.listdir():
  os.mkdir(dstPath)

# processing
for file in file_list:
  # file path 
  filepath = path + "/" + file
  print(filepath)
  
  # take image
  src = Image.open(filepath)
  
  # updown file path
  updownFile = dstPath + "/updown" + file
  
  # image processing & save
  updown = src.transpose(Image.FLIP_TOP_BOTTOM)
  updown.save(updownFile)

  # leftright file path
  leftrightFile = dstPath + "/leftright" + file

  # image processing & save
  leftright = src.transpose(Image.FLIP_LEFT_RIGHT)
  leftright.save(leftrightFile)

  uplfFile = dstPath + "/uplf" + file
  uplf = updown.transpose(Image.FLIP_LEFT_RIGHT)
  uplf.save(uplfFile)
