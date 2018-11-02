from PIL import Image
from datetime import datetime 
import math
import operator
import os
import time


def main():
	'''
		1. Get user to select an image to be the topic class average
		2. Get the user to select an image to be the non-topic class average
		3. iterate through images and assign them to classes (save these into two separate lists
		4. if the either class list is empty: ask user if they would like to change their choices.
		5. re-calculate the average for each class and repeat from step 3
		6. Do the above steps until the average no longer changes (ie no image changes classification)
		7. Use the average value of the final topic class as the new image

		
		This is far too computationally expensive. Numerous nested loops mean that this would take a very long time for large datasets.
		It already takes long enough on 10-50 images.
		I think it could be improved if I used matrices with numpy but I don't think it's worth it.
		I would prefer to work on a way to collect images that are already "correctly" labelled.
		
		Just checked the images that it selects and the whole thing is pointless.
		Also worth mentioning that it only takes one iteration for it to reach a steady state (the average doesn't change)
		(the second iteration is just to check that it won't change
		
		Just realised that there is a much much faster way of doing this.
		You don't need to completely recalculate the ave 
		you only need to multiply by n_topics etc and then subtract the images that are no longer in that class and add those that now are. 
		Then divide by how many there are now.
		DONE
	'''


	

	#retrieve the file names
	folders = [name for name in os.listdir('.')] 
	print(folders)
	folder = folders[int(input("Select folder by number: ")) - 1]
	#start timing
	start_time = time.time()
	
	files = [name for name in os.listdir("./" + folder)]
	n_files = len(files)
	
	topic_ave = list(Image.open(folder + "/" + get_image_name(folder, n_files, "topic")).getdata())
	other_ave = list(Image.open(folder + "/" + get_image_name(folder, n_files, "other")).getdata())	
	
	images = []
	image_names = []
	last_topic_ave = []
	for i, file in enumerate(files):
		im = Image.open(folder + '/' + file)
		if im.size != (640,640):
			continue
		image_names.append(file)
		images.append(list(im.getdata()))
		
	topic_ims = []
	other_ims = []
	while(last_topic_ave != topic_ave):
		print("\nNew while loop")
		last_topic_ave = topic_ave
		last_other_ave = other_ave
		i =0
		image = []
		
		for i in range(len(topic_ave)):
			topic_ave[i] = (topic_ave[i][0]*len(topic_ims),topic_ave[i][1]*len(topic_ims),topic_ave[i][2]*len(topic_ims))
		for i in range(len(other_ave)):
			other_ave[i] = (other_ave[i][0]*len(other_ims),other_ave[i][1]*len(other_ims),other_ave[i][2]*len(other_ims))
		
		for i,image in enumerate(images):
			print("Up to image #{}".format(i), end='\r')
			if euc_dist(image, last_topic_ave) < euc_dist(image, last_other_ave):
				if i in other_ims:
					other_ims.remove(i)
					for j, pixel in enumerate(image):
						other_ave[j] = tuple(map(operator.sub, other_ave[j], pixel))
				if i not in topic_ims:
					topic_ims.append(i)
					for j, pixel in enumerate(image):
						topic_ave[j] = tuple(map(operator.add, topic_ave[j], pixel))
			else:
				if i in topic_ims:
					topic_ims.remove(i)
					for j, pixel in enumerate(image):
						topic_ave[j] = tuple(map(operator.sub, topic_ave[j], pixel))
				if i not in other_ims:
					other_ims.append(i)
					for j, pixel in enumerate(image):
						other_ave[j] = tuple(map(operator.add, other_ave[j], pixel))
		
		for i in range(len(topic_ave)):
			topic_ave[i] = (topic_ave[i][0]//len(topic_ims),topic_ave[i][1]//len(topic_ims),topic_ave[i][2]//len(topic_ims))
		for i in range(len(other_ave)):
			other_ave[i] = (other_ave[i][0]//len(other_ims),other_ave[i][1]//len(other_ims),other_ave[i][2]//len(other_ims))
	

	
	new = Image.new('RGB', (640,640))
	new.putdata(topic_ave)
	dt = datetime.now().strftime('%d-%m-%Y_%H%M_')
	new.save("./Averages/" + dt + folder.split('_')[-1] + ".png")
	print("--- %s seconds ---" % (time.time() - start_time))
	
	return
	
def get_image_name(folder, max_val, used_for):
	num = -1
	file = ""
	while(True):
		try:
			num = int(input("What image should be used for the {} average: ".format(used_for)))
		except:
			print("That wasn't an integer. Try again.")
			continue
		if num < max_val and num >= 0:
			file = "image_" + str(num) + ".png"
			if Image.open(folder + '/' + file).size == (640,640):
				break
			print("Image isn't the right size. Try again.")
		else:
			print("Number is out of range. Try again.")
	return file
	
	
def euc_dist(image1, image2):
	sum = 0
	for i, pix in enumerate(image1):
		for j in range(3):
			sum += (pix[j] - image2[i][j])**2
	return math.sqrt(sum)

if __name__ == "__main__":
	main()