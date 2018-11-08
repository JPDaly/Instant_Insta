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
	
	image_files = get_file_names(folder)
	#The descriptions folder is always named the same so this just opens it
	descriptions = open(IMAGES_DEST + folder + DESC_FILE, 'r').read().split('\n')[:-1]
	
	#start timing
	start_time = time.time()
	
	feature_df = pd.DataFrame()
	#----Descriptions aren't working properly so these aren't used anymore----
	#feature_df.insert(loc=0, column='N_Tags', value=num_tags(descriptions))
	#feature_df.insert(loc=1, column='Related_tags', value=num_related_tags(descriptions, topic))
	#feature_df.insert(loc=2, column='Mentions', value=cap_mentions(descriptions, topic))
	
	#Actually gets a list of all the colours used in these images 
	common_cols = common_colours(image_files)
	
	#put these columns into the dataframe
	for i in range(len(common_cols[0])):
		feature_df.insert(loc=i, column='Colour #' + str(i), value=[im[i] for im in common_cols])
	
	#Only use the top colours
	feature_df = structure_df(feature_df)
	
	#Use clustering to hopefully remove unrelated images
	data = feature_df.values
	k_means = cluster.KMeans(n_clusters=2)
	k_means.fit(data)
	labels = k_means.labels_
	
	# Print out the images in the smaller class
	topic_class = 0
	if sum(labels) >= len(labels)/2:
		topic_class = 1
	for i,label in enumerate(labels):
		if label != topic_class:
			print(image_files[i])
	
	#print runtime
	print("\n--- %s seconds ---" % (time.time() - start_time))
	
	#ask if the user wants to delete the above printed images
	if input("Remove these images? (y/n): ") != 'n':
		for i,label in enumerate(labels):
			if label != topic_class:
				os.remove(image_files[i]) 
	
	
	return
	
# --------Functions--------

#Returns the image file names in the folder by order of the number in the file name
def get_file_names(folder):
	temp = []
	files = []
	for name in os.listdir(IMAGES_DEST + folder):
		if ".png" not in name:
			continue
		#Gets the number from the file name and passes it as an int
		num = int(name.split('_')[-1].split('.')[0])
		temp.append([name, num])
	#sort using the num value
	temp = sorted(temp, key=lambda l:l[1])
	files = [IMAGES_DEST + folder + name[0] for name in temp]
	return files
	
#removes the least common colours columns
def structure_df(df):
	col_sums = []
	bottom_cols = []
	
	#get the total sum of all the columns
	for column in df.columns:
		col_sums.append(sum(df[column]))
	#Removes the column with the smallest sum and then updates that value to infinity (do the next smallest can be found)
	for i in range(len(col_sums)-5):
		index = col_sums.index(min(col_sums))
		bottom_cols.append(df.columns[index])
		col_sums[index] = float('inf')
	
	return df.drop(bottom_cols, axis=1)	
	
# Counts how many of each colour is in each image
def common_colours(image_files):
	fraction = 255/INCREMENT + 1
	common_cols = [[0]*int(fraction**3) for i in range(len(image_files))]
	
	#iterate through the images
	for i,image_file in enumerate(image_files):
		print("Up to image #{}".format(i+1), end='\r')
		im = Image.open(image_file, 'r')
		pixels = list(im.getdata())
		n_pixels = len(pixels)
		# Goes through each pixel and maps it to a colour based on the increment value
		for pixel in pixels:
			common_cols[i][int(round(pixel[0]/INCREMENT)*((fraction**2)) + round(pixel[1]/INCREMENT)*(fraction**1) + round(pixel[2]/INCREMENT))] += 1/n_pixels
		im.close()
	print("")
	return common_cols
	
#----These functions work but they don't seem to be useful. The image with the best result turned out to be the worst image.----

# Just returns how many tags contain the topic and if the topic contains any tags
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
		
# Retuns the number of tags (Makes the assumption that the caption comes before the tags )
def num_tags(descriptions):
	n_tags = [0]*len(descriptions)
	
	for i,desc in enumerate(descriptions):
		n_tags[i] += len(desc.split("#")[1:])
	
	return n_tags
	
# Returns if the caption mentioned the topic or not
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