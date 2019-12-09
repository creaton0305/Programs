import os
import shutil
#the file_path that contain wrong LABEL 
wrong_label = os.listdir("./wrong_label/")

found_label = []
for item in wrong_label:
   index_of_dot = item.index('.')
   file_name_without_extension = item[:index_of_dot]
   found_label.append(file_name_without_extension)
#   print file_name_without_extension

#the file path that contain images of the wrong labels and the rest
find_wrong_image = os.listdir("./latest_image/")
#print find_wrong_image
count=0
findimage = []
for label in found_label:
   for image in find_wrong_image:
     if image == label+".jpeg":
       shutil.move("./latest_image/"+image, "./wrong_image/")   # in the end , it will be moved to /wrong_image folder
       count+=1  

print count and " images"
