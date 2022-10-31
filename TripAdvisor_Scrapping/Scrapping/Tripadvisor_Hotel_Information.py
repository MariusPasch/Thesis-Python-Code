def Hotel_Info(Link):


	from selenium import webdriver
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC
	import time

	ng = 'N/A'



	# Link = 'https://www.tripadvisor.com/Hotel_Review-g616162-d14965680-Reviews-High_Beach_White-Malia_Crete.html'
	# Link = 'https://www.tripadvisor.com/Hotel_Review-g503710-d499801-Reviews-Simple_Hotel_Hersonissos_Sun-Hersonissos_Crete.html'

	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument("start-maximized")
	options.add_argument("--lang=en-US")
	options.add_argument("headless")
	driver = webdriver.Chrome(options=options)
	driver.get(Link)
	try:

		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="OK"]'))).click()
	except:
		print('nop')
	# try:
	# counter = 0
	# cookie_clicked = 0
	# while True:
	# 	if cookie_clicked == 0:
	# 		try:
	# 			WebDriverWait(driver, 3).until(
	# 					EC.element_to_be_clickable((By.XPATH, '//button[text()="Manage Settings"]'))).click()
	# 			cookie_clicked = 1
	# 		except:
	# 			print('\nNo cookie')
	#
	# 	try:
	# 		try:
	# 			time.sleep(2)
	# 			driver.find_element_by_xpath('//button[text()="Decline All"]').click()
	# 		except:
	# 			WebDriverWait(driver, 2).until(
	# 					EC.element_to_be_clickable((By.XPATH, '//button[text()="Decline All"]'))).click()
	# 		break
	# 	except:
	# 		print('\nNo Decline')
	# 	if counter >= 3:
	# 		driver.refresh()
	# 		break
	# 	if counter == 2:
	# 		driver.refresh()
	# 	counter += 1

	time.sleep(1)
	try:
		driver.find_element_by_xpath('//span[@class="_33O9dg0j"]').text
	except:
		driver.close()
		return 'No reviews'

	reviews = driver.find_element_by_xpath('//span[@class="_33O9dg0j"]').text.split()[0]

	stars = float(driver.find_element_by_xpath('//a[@class="_15eFvJyR _3nlVsadw"]/span').get_attribute('class').split('_')[-1])/10

	location = driver.find_element_by_xpath('//span[@class="_3ErVArsu jke2_wbp"]').text

	stars_location = ng
	stars_cleanliness = ng
	stars_service = ng
	stars_value = ng
	try:

		for s in driver.find_elements_by_class_name('_1krg1t5y'):
			if 'Location' in s.text:
				stars_location = float(s.find_element_by_tag_name('span').get_attribute('class').split('_')[-1])/10
			elif 'Cleanliness' in s.text:
				stars_cleanliness = float(s.find_element_by_tag_name('span').get_attribute('class').split('_')[-1])/10
			elif 'Service' in s.text:
				stars_service = float(s.find_element_by_tag_name('span').get_attribute('class').split('_')[-1]) / 10
			elif 'Value' in s.text:
				stars_value = float(s.find_element_by_tag_name('span').get_attribute('class').split('_')[-1]) / 10
	except:
		stars_location = ng
		stars_cleanliness = ng
		stars_service = ng
		stars_value = ng


	try:
		WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, '//div[@class="_80614yz7" and text()="Show more"]'))).click()
		WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
				(By.XPATH, '//div[@class="_1yStC7yf"]/div/div[@data-test-target="amenity_text"]')))
		amenities = [a.text for a in driver.find_elements_by_xpath(
			'//div[@class="_1yStC7yf"]/div/div[@data-test-target="amenity_text"]')]

	except:
		try:
			amenities = [a.text for a in driver.find_element_by_xpath(
					'//div[text()="Property amenities"]//following-sibling::div').find_elements_by_class_name(
				'_2rdvbNSg')]
		except:
			amenities = []
	try:
		WebDriverWait(driver, 4).until(EC.element_to_be_clickable(
				(By.XPATH, '//span[@class="_2GIfqQkr _3csHgUwM" and text()="Room features"]'))).click()
		WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
				(By.XPATH, '//div[@class="_1yStC7yf"]/div/div[@data-test-target="amenity_text"]')))
		room_features = [a.text for a in driver.find_elements_by_xpath(
				'//div[@class="_1yStC7yf"]/div/div[@data-test-target="amenity_text"]')]

	except:
		try:
			room_features = [a.text for a in driver.find_element_by_xpath(
					'//div[text()="Room features"]//following-sibling::div').find_elements_by_class_name('_2rdvbNSg')]
		except:
			room_features = []

	try:
		WebDriverWait(driver, 4).until(
				EC.element_to_be_clickable(
						(By.XPATH, '//span[@class="_2GIfqQkr _3csHgUwM" and text()="Room types"]'))).click()
		WebDriverWait(driver, 4).until(EC.presence_of_all_elements_located(
				(By.XPATH, '//div[@class="_1yStC7yf"]/div/div[@data-test-target="amenity_text"]')))
		room_types = [a.text for a in
		              driver.find_elements_by_xpath(
			              '//div[@class="_1yStC7yf"]/div/div[@data-test-target="amenity_text"]')]

	except:
		try:
			room_types = [a.text for a in driver.find_element_by_xpath(
					'//div[text()="Room types"]//following-sibling::div').find_elements_by_class_name('_2rdvbNSg')]
		except:
			room_types = []


	try:
		WebDriverWait(driver, 4).until(
			EC.element_to_be_clickable((By.XPATH, '//div[@class="_2EFRp_bb _9Wi4Mpeb" and @aria-label="Close"]'))).click()

	except:
		print('\nCant click amenities')
	try:
		hotel_class = driver.find_element_by_xpath('//div[@class="_2dtF3ueh"]/span').find_element_by_tag_name('svg').get_attribute('aria-label')
		hotel_class=hotel_class.replace('bubbles','Stars')
	except:
		hotel_class = ng


	for r in driver.find_element_by_class_name('_2lcHrbTn').find_elements_by_tag_name('li'):
		if r.find_element_by_class_name('_2PPG44IR._1o34NnSP').text == 'Excellent':
			revs_excellent = r.find_element_by_class_name('_3fVK8yi6').text
		elif r.find_element_by_class_name('_2PPG44IR._1o34NnSP').text == 'Very Good':
			revs_verygood = r.find_element_by_class_name('_3fVK8yi6').text
		elif r.find_element_by_class_name('_2PPG44IR._1o34NnSP').text == 'Average':
			revs_average = r.find_element_by_class_name('_3fVK8yi6').text
		elif r.find_element_by_class_name('_2PPG44IR._1o34NnSP').text == 'Poor':
			revs_poor = r.find_element_by_class_name('_3fVK8yi6').text
		elif r.find_element_by_class_name('_2PPG44IR._1o34NnSP').text == 'Terrible':
			revs_terrible = r.find_element_by_class_name('_3fVK8yi6').text



	Information={'Reviews': reviews,
	             'Stars': stars,
	             'Location': location,
	             'Stars_Location': stars_location,
	             'Stars_Cleanliness': stars_cleanliness,
	            'Stars_Service': stars_service,
	            'Stars_value': stars_value,
	            'Amenities': amenities,
	            'Room_features': room_features,
	            'Room_Types': room_types,
	            'Hotel_Class': hotel_class,
	            'Revs_Ecxellent': revs_excellent,
	            'Revs_Verygood': revs_verygood,
	            'Revs_Average': revs_average,
	            'Revs_Poor': revs_poor,
	            'Revs_Terrible': revs_terrible}


	driver.close()

	return Information