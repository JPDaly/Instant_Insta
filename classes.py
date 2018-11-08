from selenium import webdriver
from constants import *
from functions import *
import time

class Browser:
	posts = []
	topic = ""
	driver = webdriver.Chrome(CHROMEDRIVER_DEST)
	scroll_dist = SCROLL_INCREMENT

	#Opens the page using the chosen tag. (Also makes sure page is loaded before exiting)
	def get_tag(self, tag):
		#go to page
		self.driver.get(TAGS+tag)
		temp = []
		#wait until expected element is found
		while(len(temp) == 0):
			time.sleep(0.5)
			temp = self.driver.find_elements_by_tag_name('img')
		return

	'''
	Scroll until xpath element is found
	If check_sources is True the loop will only break if the element found wasn't already scraped
	'''
	def scroll(self, xpath, check_sources=False):
		dots = 0
		total_time = 0
		found = False
		sources = [post[0] for post in self.posts]
		
		
		while(True):
			#scroll downwards by SCROLL_INCREMENT
			self.scroll_dist += SCROLL_INCREMENT
			self.driver.execute_script("window.scrollTo(0, "+str(self.scroll_dist)+")")		
			time.sleep(0.5)
			dots = loading_text("Searching for more images", dots)
			#break if we have been searching for too long
			if total_time >= 30:
				print("\nError. Couldn't find image and timed out.")
				exit()
			try:
				#try to get the element
				element = self.driver.find_element_by_xpath(xpath)
				src = element.get_attribute('src')
				found = True
			except:
				total_time += 0.5
				# This isn't needed but it makes this more readable.
				found = False				
				
			if (check_sources and (src not in sources)) or (not check_sources and found):
				break
		return
		
		'''
		This is the old way that I did the above scroll method
		
		
		if check_sources:
			element = self.driver.find_element_by_xpath(xpath)
			while(element.get_attribute('src') in self.sources):
				self.scroll_dist += SCROLL_INCREMENT
				self.driver.execute_script("window.scrollTo(0, "+str(self.scroll_dist)+")")		
				time.sleep(0.5)
				dots = loading_text("Searching for more images", dots)
				element = self.driver.find_element_by_xpath(xpath)			
		else:
			total_time = 0
			while(1):
				try:
					element = self.driver.find_element_by_xpath(xpath)
					break		
				except:
					self.scroll_dist += SCROLL_INCREMENT
					self.driver.execute_script("window.scrollTo(0, "+str(self.scroll_dist)+")")		
					time.sleep(0.5)
					dots = loading_text("Searching for more images", dots)
					total_time += 0.5
				if total_time >= 30:
					print("\nError. Couldn't find element.")
					exit()
		'''