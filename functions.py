import time
import os
from datetime import datetime 
from urllib.request import urlretrieve
from constants import *


def loading_text(string, dots):
	print(" "*int(len(string)+10), end='\r')
	print(string + "."*int(dots), end='\r')
	if dots == 3:
		return 0
	return dots+1

def data_size():
	size = 0

	while(True):
		try:
			size = int(input("Number of images to scrape: "))
			break
		except:
			print("Error. Please enter an integer.")
	return size

def todays_topic(br):
	happy = False 
	while(True):
		br.topic = input("What is the topic for today?\nEnter Topic: ")
		br.topic = br.topic.replace(" ", "")
		br.get_tag(br.topic)
		if input("Happy with this choice? (y/n): ") != 'n':
			break
	return


def get_images(br, n_images):
	dots = 0
	while(len(set(br.sources)) < n_images):
		br.scroll(IMG_START+str(1)+IMG_MID+str(1)+IMG_END, True)
		for row in range(1,17):
			errors = 0
			for i in range(1,4):
				try:
					element = br.driver.find_element_by_xpath(IMG_START+str(row)+IMG_MID+str(i)+IMG_END)
					br.sources.append(element.get_attribute('src'))
				except:
					errors += 1
				if(len(set(br.sources)) >= n_images):
					br.sources = set(br.sources)
					return
			if errors >= 3:
				br.scroll(IMG_START+str(row)+IMG_MID+str(i)+IMG_END)
				row -= 1
			dots = loading_text("Scraping images", dots)
	return



def show_images(driver, image_set):
	for i, src in enumerate(image_set):
		driver.get(src)
		print("Showing image #{}".format(i), end='\r')
		time.sleep(1)
	return
	
def download_images(br):
	dt = datetime.now().strftime('%d-%m-%Y_%H-%M_')
	newfolder = DOWNLOAD_FOLDER_DIR + dt + br.topic
	if not os.path.exists(newfolder):
		os.makedirs(newfolder)
	for i,src in enumerate(br.sources):
		loading_text("Downloading image #{}".format(i+1), 0)
		try:
			urlretrieve(src,newfolder + "/" + FILE_NAME + str(i) + FILE_EXTENSION)
		except:
			print("Couldn't download image #{}".format(i))
	print("")
	return