from selenium import webdriver
from constants import *
from functions import *
import time

class Browser:
	sources = []
	driver = webdriver.Chrome(CHROMEDRIVER_DEST)
	scroll_dist = SCROLL_INCREMENT

	def get_tag(self, tag):
		self.driver.get(TAGS+tag)
		temp = []
		while(len(temp) == 0):
			time.sleep(0.5)
			temp = self.driver.find_elements_by_tag_name('img')

	def scroll(self, xpath, checklist=None):
		dots = 0
		if checklist:
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
		return