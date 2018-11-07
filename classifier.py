from PIL import Image
import numpy as np
import pandas as pd
import os
import time
from sklearn import cluster

IMAGES_DEST = './Downloads/'
DESC_FILE = "descriptions.txt"
INCREMENT = 51 #factors are 1,3,5,15,17,51,85,255

def main():
	#retrieve the file names
	folders = [name for name in os.listdir(IMAGES_DEST)] 
	print(folders)
	folder = folders[int(input("Select folder by index: ")) - 1] + "/"
	topic = folder.split("_")[-1][:-1]
	
	image_files = get_file_names(folder)#[name for name in os.listdir(IMAGES_DEST + folder) if ".png" in name]
	descriptions = open(IMAGES_DEST + folder + DESC_FILE, 'r').read().split('\n')[:-1]
	
	
	#start timing
	start_time = time.time()
	
	feature_df = pd.DataFrame()
	#Descriptions aren't working properly so these aren't used anymore
	#feature_df.insert(loc=0, column='N_Tags', value=num_tags(descriptions))
	#feature_df.insert(loc=1, column='Related_tags', value=num_related_tags(descriptions, topic))
	#feature_df.insert(loc=2, column='Mentions', value=cap_mentions(descriptions, topic))
	common_cols = common_colours(image_files)
	
	for i in range(len(common_cols[0])):
		feature_df.insert(loc=i, column='Colour #' + str(i), value=[im[i] for im in common_cols])
	
	feature_df = structure_df(feature_df)
		
	print(feature_df)
	data = feature_df.values
	k_means = cluster.KMeans(n_clusters=2)
	k_means.fit(data)
	labels = k_means.labels_
	
	topic_class = 0
	if sum(labels) >= len(labels)/2:
		topic_class = 1
	for i,label in enumerate(labels):
		if label != topic_class:
			print(image_files[i])
	
	print(labels)
	
	#print runtime
	print("\n--- %s seconds ---" % (time.time() - start_time))
	return
	
# --------Functions--------

def get_file_names(folder):
	temp = []
	files = []
	for name in os.listdir(IMAGES_DEST + folder):
		if ".png" not in name:
			continue
		num = int(name.split('_')[-1].split('.')[0])
		temp.append([name, num])
	temp = sorted(temp, key=lambda l:l[1])
	files = [IMAGES_DEST + folder + name[0] for name in temp]
	return files
	
	
def structure_df(df):
	col_sums = []
	bottom_cols = []
	
	for column in df.columns:
		col_sums.append(sum(df[column]))
	for i in range(len(col_sums)-10):
		index = col_sums.index(min(col_sums))
		bottom_cols.append(df.columns[index])
		col_sums[index] = float('inf')
	
	return df.drop(bottom_cols, axis=1)	
	

def common_colours(image_files):
	fraction = 255/INCREMENT + 1
	common_cols = [[0]*int(fraction**3) for i in range(len(image_files))]
	
	for i,image_file in enumerate(image_files):
		print("Up to image #{}".format(i+1), end='\r')
		im = Image.open(image_file, 'r')
		pixels = list(im.getdata())
		n_pixels = len(pixels)
		for pixel in pixels:
			common_cols[i][int(round(pixel[0]/INCREMENT)*((fraction**2)) + round(pixel[1]/INCREMENT)*(fraction**1) + round(pixel[2]/INCREMENT))] += 1/n_pixels
		im.close()
	print("")
	return common_cols
	
#These functions work but they don't seem to be useful. The image with the best result turned out to be the worst image.
def num_related_tags(descriptions, topic):
	related = [0]*len(descriptions)

	for i,description in enumerate(descriptions):
		tags = description.split("#")[1:]
		for tag in tags :
			if topic in tag:
				related[i] += 1
			elif tag in topic:
				related[i] += 1
	
	return related
		
def num_tags(descriptions):
	n_tags = [0]*len(descriptions)
	
	for i,desc in enumerate(descriptions):
		n_tags[i] += len(desc.split("#")[1:])
	
	return n_tags
	
def cap_mentions(descriptions, topic):
	mentions = [0]*len(descriptions)
	
	for i,desc in enumerate(descriptions):
		caption = desc.split("#")[0]
		if topic in caption:
			mentions[i] += 1
		elif caption in topic:
			mentions[i] += 1
	
	return mentions
		
		
if __name__ == "__main__":
	main()	