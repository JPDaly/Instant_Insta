from PIL import Image
from datetime import datetime 
from constants import *
import operator
import os
import time



def main():
	#retrieve the file names
	folders = [name for name in os.listdir(DOWNLOAD_FOLDER_DIR)] 
	print(folders)
	folder = DOWNLOAD_FOLDER_DIR + folders[int(input("Select folder by number: ")) - 1] + "/"
	
	#start timing
	start_time = time.time()
	
	files = [name for name in os.listdir(folder) if FILE_EXTENSION in name]
	n_files = len(files)
	
	
	ave = []
	images_used = 0
	for file in files:
		im = Image.open(folder + file)
		if im.size != (640,640):
			continue
		print("On image #{}".format(images_used), end='\r'	)
		images_used += 1
		pixels = list(im.getdata())
		for i, pixel in enumerate(pixels):
			try:
				ave[i] = tuple(map(operator.add, ave[i], pixel))
			except:
				ave.append(pixel)
	
	for i in range(len(ave)):
			ave[i] = (ave[i][0]//images_used,ave[i][1]//images_used,ave[i][2]//images_used)
	
	new = Image.new('RGB', (640,640))
	new.putdata(ave)
	dt = datetime.now().strftime('%Y-%m-%d_%H%M_')
	# File names are in the format year_month_day_hourminute_topic_images_used.extension
	new.save("./Averages/" + dt + folder.split('_')[-1][:-1] + "_" + str(images_used) + FILE_EXTENSION)
	
	#print runtime
	print("\n--- %s seconds ---" % (time.time() - start_time))
	
	return

if __name__ == "__main__":
	main()
	
	
	
'''
If you want to be able to see the average size of the images scraped
	ave = [0,0]
	counter = 0
	smallest = 1000
	for file in files:
		im = Image.open(folders[folder] + "/" + file)
		if im.size == (640,640):
			counter += 1
		elif im.size[0] < smallest:
			smallest = im.size[0]
		ave[0] += im.size[0]
		ave[1] += im.size[1]
	ave[0] = ave[0]/len(files)
	ave[1] = ave[1]/len(files)
	print(counter)
	print(smallest)
	print(ave)
'''