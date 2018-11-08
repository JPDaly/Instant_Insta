from scrape import *
from classifier import *
from average import *

def main():
	if input("Do you want to scrape (s) new images or use an existing (e) folder? (s/e): ") == 's':
		folder = scrape()
	else:
		folder = None
	if input("\nWould you like to use classifier.py to remove outliers? (y/n): ") != 'n':
		classifier(folder)
	if input("\nWould you like to use average.py to generate an image? (y/n): ") != 'n':
		average(folder)
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