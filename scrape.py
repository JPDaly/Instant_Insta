from classes import Browser
from scrape_functions import *
import time


def scrape():
	br = Browser()
	todays_topic(br)

	#start timing
	start_time = time.time()
	
	get_images(br, data_size())
	print("\nNumber of images scraped = {}".format(len(br.posts)))
	#show_images(br.driver, br.sources)
	folder = download_images(br)
	
	#Show runtime
	print("\n--- %s seconds ---\n" % (time.time() - start_time))
	
	if input("Close Chrome? (y/n): ") != 'n':
		br.driver.close()
	return folder



if __name__ == "__main__":
	scrape()