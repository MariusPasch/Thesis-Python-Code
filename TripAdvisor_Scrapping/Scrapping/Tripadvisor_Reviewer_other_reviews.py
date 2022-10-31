def Reviewer_other_reviews(Link):
	from selenium import webdriver
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC
	import time
	from selenium.webdriver.common.action_chains import ActionChains


	# Link='https://www.tripadvisor.com/Profile/Kat59623'

	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument("start-maximized")
	options.add_argument("--lang=en-US")
	driver = webdriver.Chrome(options=options)
	driver.get(Link)

	counter = 0
	while True:

		try:
			WebDriverWait(driver, 3).until(
					EC.element_to_be_clickable((By.XPATH, '//button[text()="Manage Settings"]'))).click()
		except:
			print('\nNo cookie')
		try:
			time.sleep(2)
			WebDriverWait(driver, 2).until(
					EC.element_to_be_clickable((By.XPATH, '//button[text()="Decline All"]'))).click()
			break
		except:
			print('\nNo Decline')
		if counter >= 3:
			driver.refresh()
			time.sleep(5)
			break

		counter += 1

	WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.XPATH, '//a[@data-tab-name="Reviews"]'))).click()

	try:
		WebDriverWait(driver, 10).until(
				EC.element_to_be_clickable((By.CLASS_NAME, '_1JOGv2rJ._2oWqCEVy._3yBiBka1._3fiJJkxX'))).click()
	except:
		print('\nNo Show More')

	size = 0
	new_size = len(driver.find_elements_by_class_name('nMewIgXP.ui_card.section'))
	while size < new_size:
		size = len(driver.find_elements_by_class_name('nMewIgXP.ui_card.section'))
		time.sleep(1)
		ActionChains(driver).move_to_element(
				driver.find_elements_by_class_name('nMewIgXP.ui_card.section')[-1]).perform()
		time.sleep(7)
		new_size = len(driver.find_elements_by_class_name('nMewIgXP.ui_card.section'))

	Reviews_hotels = []
	try:

		for window in driver.find_elements_by_class_name('nMewIgXP.ui_card.section'):
			try:

				if window.find_element_by_class_name('_2IicNcbI').text == 'Date of stay:':
					date = window.find_element_by_class_name('_3Coh9OJA').text.strip('Date of stay: ')
					hotel_location = window.find_element_by_class_name('_7JBZK6_8._20BneOSW').text
					hotel_name = window.find_element_by_class_name('_2ys8zX0p.ui_link').text
					hotel_link = window.find_element_by_class_name(
						'_2X5tM2jP._2RdXRsdL._1gafur1D').find_element_by_tag_name('a').get_attribute('href')
					Reviews_hotels.append({'Date': date,
					                       'Hotel Location': hotel_location,
											'Hotel Name': hotel_name,
                                           'Hotel Link': hotel_link})
			except:
				print('\nNot hotel')

		driver.quit()
		return Reviews_hotels
	except:
		driver.quit()
		return Reviews_hotels
########################################################################################################################
def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+',encoding='utf-8', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = csv.DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)

########################################################################################################################

import csv

laptop = r'C:\Users\pasch\Documents\TripAdvisor_Scrapping'
pc = r'C:\Users\Palios\PycharmProjects\TripAdvisor'

location = laptop

Reviews_csv_file = location + r'\Data/Reviews_Total.csv'
Reviewer_other_info_csv_file = location + r'\Data\Reviewer_other_info.csv'

import random

collected_data = list(csv.DictReader(open(Reviews_csv_file, encoding='utf-8')))

selected_reviewers = []
for data in collected_data:

	if data['Contribution Votes'] == '':
		c=0
	else:
		c=int(data['Contribution Votes'].replace(',',''))

	if c >= 2 and c < 228:
		selected_reviewers.append(data)


random.shuffle(selected_reviewers)
# print(len(selected_reviewers))

sample=int(round(len(selected_reviewers)*0.1,0))
# sample=1
print('\nSample size=',sample)
reviewers_information = []

for item in range(sample):
	rvr = selected_reviewers[item]
	info = Reviewer_other_reviews(rvr["Reviewer Link"])

	for r in info:
		r.update({"Reviewer Username": rvr["Reviewer Username"],
	            "Reviewer Link": rvr["Reviewer Link"],
	            "Original Hotel": rvr['Hotel Name']})
		reviewers_information.append(r)

		fieldnames = r.keys()
		append_dict_as_row(Reviewer_other_info_csv_file, r, fieldnames)




# with open(Reviewer_other_info_csv_file, 'w', encoding='utf-8', newline='') as reviews_file:
#     fieldnames = reviewers_information[0].keys()
#
#     writer = csv.DictWriter(reviews_file, fieldnames=fieldnames)
#
#     writer.writeheader()
#     for data in reviewers_information:
#         try:
#
#             writer.writerow(data)
#
#         except:
#             print(data)
#


# Append reviews to csv
#
# fieldnames = reviewers_information[0].keys()
#
# for rev_a in reviewers_information:
# 	try:
# 		append_dict_as_row(Reviewer_other_info_csv_file, rev_a, fieldnames)
# 	except:
# 		print(rev_a)
#
#
