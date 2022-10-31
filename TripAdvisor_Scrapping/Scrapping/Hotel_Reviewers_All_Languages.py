
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

csv_file_Hotel_Reviewers_All_Languages = r'C:\Users\pasch\Documents\TripAdvisor_Scrapping\Data/Hotel_Reviewers_All_Languages.csv'
csv_file = r'/Data/Majorca/Hotels_Name_Link.csv'


collected_data = list(csv.DictReader(open(csv_file, encoding='utf-8')))

hotelswithreviews = []
for dt in collected_data:
	if dt['Reviews'] != '':
		d = {'Hotel Name': dt['Name'], 'Link': dt['Link']}
		hotelswithreviews.append(d)


size = len(hotelswithreviews)

revrs_info = []

for item in range(3):
	print('\nhotels progress = %.2f'%((item/size)*100) +'%')
	Link = hotelswithreviews[item]['Link']



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
			WebDriverWait(driver, 3).until(
					EC.element_to_be_clickable((By.XPATH, '//button[text()="Decline All"]'))).click()
			break
		except:
			print('\nNo Decline')
		if counter >= 3: break
		if counter ==2:
			driver.refresh()
			time.sleep(2)
		counter += 1

	try:
		last = int(WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, '//div[@class="pageNumbers"]/a[last()]'))).text)
	except:
		last = 1

	print('\nreviews pages = ', last)

	try:
		if WebDriverWait(driver, 3).until(
					EC.presence_of_element_located((By.CLASS_NAME, '_1wk-I7LS'))).text == 'All languages':
			driver.find_element_by_class_name('_1wk-I7LS').click()
	except:
		print('No All Languages')



	for page in range(5):
		print('\nPage=' + str(page + 1) + ' ' + str(((page + 1) / last) * 100) + '%')

		WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2wrUUKlw _3hFEdNs8"]')))

		# window = WebDriverWait(driver, 10).until(
		#     EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2wrUUKlw _3hFEdNs8"]')))[0]

		for window in WebDriverWait(driver, 10).until(
				EC.presence_of_all_elements_located((By.XPATH, '//div[@class="_2wrUUKlw _3hFEdNs8"]'))):

			try:
				contributions = 0
				for c in window.find_elements_by_class_name('_3fPsSAYi'):
					if 'contribution' in c.text:
						contributions = c.text.split()[0]
			except:
				contributions = 0

			if contributions != 0:

				try:
					reviewer = window.find_element_by_class_name("ui_header_link._1r_My98y").text
				except:
					reviewer = window.find_element_by_class_name("ui_header_link._1r_My98y verified").text

				try:
					reviewer_link = window.find_element_by_class_name("ui_header_link._1r_My98y").get_attribute('href')
				except:
					reviewer_link = window.find_element_by_class_name("ui_header_link._1r_My98y verified").get_attribute(
							'href')

				try:
					country = window.find_element_by_class_name("_1TuWwpYf").text
				except:
					country = ''




				revrs_info.append({"Reviewer Username": reviewer,
	                             "Reviewer Link": reviewer_link,
	                             "Country": country,
	                             "Contributions": contributions,
				                  "Hotel Name": hotelswithreviews[item]['Hotel Name']})

		if page >= last - 1: break

		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Next"]'))).click()

		time.sleep(2)

	driver.quit()


########################################################################################################################

with open(csv_file_Hotel_Reviewers_All_Languages, 'w', encoding='utf-8', newline='') as file:
    fieldnames = revrs_info[0].keys()

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for data in revrs_info:
        try:

            writer.writerow(data)

        except:
            print(data)