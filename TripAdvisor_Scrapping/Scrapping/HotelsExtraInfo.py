from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import pickle
# pl = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\MultiDimensionalMatrix.csv')

df =  pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')
# hotels = pl.Hotel.values
# df = df.loc[df.Name.isin(hotels)]


d = pickle.load(open(r'C:\Users\pasch\Documents\TripAdvisor_Scrapping\HotelLocationInfoOld.p', 'rb'))
info = d['info']
hotelnames = d['hotelnames']
# info = []
#
# hotelnames = []

links =  df.Link.values

count = 0
all = [info[i][0] for i in range(len(info))]
n = df.index
for i in n:
	# index = info[i][0]
	if i not in all:
		print('\n',i, df.Link[i])
		count += 1

size = len(links)
start = len(info)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument("start-maximized")
options.add_argument("--lang=en-US")
options.add_argument("headless")
driver = webdriver.Chrome(options=options)

for index in range(start,len(links)):
	link =links[index]
	# options = webdriver.ChromeOptions()
	# options.add_argument('--ignore-certificate-errors')
	# options.add_argument('--incognito')
	# options.add_argument("start-maximized")
	# options.add_argument("--lang=en-US")
	# options.add_argument("headless")
	# driver = webdriver.Chrome(options=options)
	driver.get(link)
	if index == start:
		try:
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="OK"]'))).click()
		except:
			print('\nNo cookie')
	# try:
	# 	WebDriverWait(driver, 10).until(
	# 		EC.presence_of_element_located((By.XPATH, '//div[@id="LOCATION"]//div[@class="ui_columns"]')))
	# except:
	# 	print('Not present all reviews')
	time.sleep(3)
	try:
		hotelnames.append(driver.find_element_by_id('HEADING').text)
	except:
		hotelnames.append(driver.find_element_by_id('component_5').find_element_by_id('HEADING').text)
	loc = driver.find_element_by_id('LOCATION')
	try:
		if len(loc.find_elements_by_class_name('ui_columns')) >= 2:

			info.append((index,loc.find_element_by_class_name('ui_columns').text))
		else:
			info.append((index,''))
	except:
		info.append((index,''))


	# driver.close()
	print(round(100*index/size,4),'%')




pickle.dump({'hotelnames':hotelnames,'info':info},open('HotelLocationInfoOld.p','wb'))

