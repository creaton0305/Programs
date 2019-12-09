
import os
import glob
import xml.etree.ElementTree as ET
path = '/home/ariccspstk/Downloads/export-voc-2019-06-29T18_11_25.042770/wrong_label'    #path of the wrong_label 

files = [f for f in glob.glob(path + "/*.xml", recursive=True)]

for f in files:
	print(f)
	document = ET.parse(f)
	root = document.getroot() 	
	removeList = list()
	for child in root.findall('object'): 
	  if( child.find('polygon') ):
		  root.remove(child)
	document.write(f)




