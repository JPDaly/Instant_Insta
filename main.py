from constants import *
from classes import *
from functions import *
import os
from PIL import Image
import time

def main():
	
	br = Browser()
	todays_topic(br)

	#start timing
	start_time = time.time()
	
	get_images(br, data_size())
	print("\nNumber of images scraped = {}".format(len(br.posts)))
	#show_images(br.driver, br.sources)
	download_images(br)
	

	#Show runtime
	print("\n--- %s seconds ---" % (time.time() - start_time))
	
	if input("Close Chrome? (y/n): ") != 'n':
		br.driver.close()
	return
	

if __name__ == "__main__":
	main()


# ***********************************************************************************
# Tips

# This is for scrolling down Y pixels I believe. Note that Y must continuously get bigger if you want to keep scrolling 
	# This is how you scroll "driver.execute_script("window.scrollTo(0, Y)")"
# This is for inputting a string into an element that is defined by name
	# driver.find_element_by_name("username").send_keys()
# Same as above except by tag name
	# images = br.find_elements_by_tag_name('img')
# Get sources from image elements
	# image.get_attribute('src')