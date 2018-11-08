import time
import os
from datetime import datetime 
from urllib.request import urlretrieve
from constants import *
import string

#Used to print loading text (specified by the string parameter) with a changing number of dots
def loading_text(string, dots):
	#make output line empty
	print(" "*int(len(string)+50), end='\r')
	#print string with #dots dots 
	print(string + "."*int(dots), end='\r')
	if dots == 3:
		return 0
	return dots+1

#Get the user's preference for the number of images to scrape
def data_size():
	size = 0
	while(True):
		#try is used just in case the input can't be converted to int
		try:
			size = int(input("Number of images to scrape: "))
			break
		except:
			print("Error. Please enter an integer.")
	return size

# Get user's preference for the topic to scrape
def todays_topic(br):
	while(True):
		br.topic = input("What is the topic for today?\nEnter Topic: ")
		#remove spaces because that won't work in the url
		br.topic = br.topic.replace(" ", "")
		#go to that page
		br.get_tag(br.topic)
		#Let user check and decide if they want to change their choice
		if input("Happy with this choice? (y/n): ") != 'n':
			break
	return

'''
This function receives the source url's for the images on the page
Note: 
	-The html only shows 17 rows of images at a time. Therefore, as you scroll it updates.
	-You will also notice that set(br.sources) is used rather than just br.sources. This is because
	when set wasn't used the program was scraping duplicates

'''
def get_images(br, n_images):
	dots = 0

	#loop until we have enough images
	while(len(set(br.posts)) < n_images):
		#scroll until we have a new set of 17 rows
		br.scroll(IMG_START+str(1)+IMG_MID+str(1)+IMG_END, True)
		#loop through available 17 rows
		for row in range(1,17):
			errors = 0
			#loops through the 3 images in the row
			for i in range(1,4):
				#try to retrieve the source of the image
				try:
					element = br.driver.find_element_by_xpath(IMG_START+str(row)+IMG_MID+str(i)+IMG_END)
					br.posts.append((element.get_attribute('src'), element.get_attribute('alt').replace('\n', '')))
				except:
					errors += 1
				#if we have enough images before 17 rows are iterated through return early
				if(len(set(br.posts)) >= n_images):
					br.posts = set(br.posts)
					return
			#If all 3 images in the row weren't found scroll until that row is found
			if errors >= 3:
				#scroll until that row is found
				br.scroll(IMG_START+str(row)+IMG_MID+str(i)+IMG_END)
				#try the row again
				row -= 1
			dots = loading_text("Scraping images", dots)
	br.posts = set(br.posts)
	return

#Used for testing but simply displays the images in the browser
def show_images(driver, image_set):
	for i, src in enumerate(image_set):
		driver.get(src)
		print("Showing image #{}".format(i), end='\r')
		time.sleep(1)
	return

#Creates a folder and downloads all the images into it
def download_images(br):
	#Use time to create an independent name for the folder
	dt = datetime.now().strftime('%d-%m-%Y_%H%M_')
	newfolder = DOWNLOAD_FOLDER_DIR + dt + br.topic
	
	#Create new folder
	if not os.path.exists(newfolder):
		os.makedirs(newfolder)
	else:
		#unlikely but
		print("This folder already exists. Images can't be saved")
		return
		
	#Save all images into folder
	for i,post in enumerate(br.posts):
		loading_text("Downloading image #{}".format(i+1), 0)
		try:
			urlretrieve(post[0],newfolder + "/" + FILE_NAME + str(i) + FILE_EXTENSION)
		except:
			print("\nCouldn't download image #{}".format(i))
	print("")
	
	#save descriptions to a txt file
	dots = 0
	printable_chars = string.printable
	file = open(newfolder + "/" + "descriptions.txt", 'w+')
	for post in br.posts:
		dots = loading_text("Saving descriptions", dots)
		for c in post[1]:
			if c in printable_chars:
				file.write(c)
		file.write("\n")
	print("")
	return
	
	