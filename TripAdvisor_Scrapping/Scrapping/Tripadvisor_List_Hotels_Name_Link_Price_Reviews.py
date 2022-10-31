# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import csv
#Original Website of total region

# #Heraklion
# WebSite="https://www.tripadvisor.com/Hotels-g1746299-Heraklion_Prefecture_Crete-Hotels.html"

# #Majiorca
# WebSite = "https://www.tripadvisor.com/Hotels-g187462-Majorca_Balearic_Islands-Hotels.html"

# #Rhodes
# WebSite = "https://www.tripadvisor.com/Hotels-g189449-Rhodes_Dodecanese_South_Aegean-Hotels.html"

# #Corfu
# WebSite = "https://www.tripadvisor.com/Hotels-g189458-Corfu_Ionian_Islands-Hotels.html"

# #Zakynthos
# WebSite = "https://www.tripadvisor.com/Hotels-g189462-Zakynthos_Ionian_Islands-Hotels.html"

# #Chania
# WebSite = "https://www.tripadvisor.com/Hotels-g1699518-Chania_Prefecture_Crete-Hotels.html"

#Spain
# #Lanzarote
# WebSite = "https://www.tripadvisor.com/Hotels-g187477-Lanzarote_Canary_Islands-Hotels.html"

# #Tenerife
# WebSite = "https://www.tripadvisor.com/Hotels-g187479-Tenerife_Canary_Islands-Hotels.html"

# #Fuerteventura
# WebSite = "https://www.tripadvisor.com/Hotels-g187467-Fuerteventura_Canary_Islands-Hotels.html"

# #Gran Canaria
# WebSite = "https://www.tripadvisor.com/Hotels-g187471-Gran_Canaria_Canary_Islands-Hotels.html"

###Turkey
# #Antalya
# WebSite = "https://www.tripadvisor.com/Hotels-g312737-Oludeniz_Mugla_Province_Turkish_Aegean_Coast-Hotels.html"

# #Mugla
# WebSite = "https://www.tripadvisor.co.uk/Hotels-g298019-Mugla_Province_Turkish_Aegean_Coast-Hotels.html"


###Frace
# #Nice
# WebSite = "https://www.tripadvisor.com/Hotels-g187234-Nice_French_Riviera_Cote_d_Azur_Provence_Alpes_Cote_d_Azur-Hotels.html"

# #Marseille
# WebSite = "https://www.tripadvisor.com/Hotels-g187253-Marseille_Bouches_du_Rhone_Provence_Alpes_Cote_d_Azur-Hotels.html"

# #Bordeaux
# WebSite = "https://www.tripadvisor.com/Hotels-g1934712-Gironde_Nouvelle_Aquitaine-Hotels.html"

# #Calais
# WebSite = "https://www.tripadvisor.com/Hotels-g196659-Calais_Pas_de_Calais_Hauts_de_France-Hotels.html"

# #Corsica
# WebSite = "https://www.tripadvisor.com/Hotels-g187139-Corsica-Hotels.html"


###Italy

# #Amalfi Coast
# WebSite = "https://www.tripadvisor.com/Hotels-g187779-Amalfi_Coast_Province_of_Salerno_Campania-Hotels.html"

# #Sicily
# WebSite = "https://www.tripadvisor.com/Hotels-g187886-Sicily-Hotels.html"

# #Sardinia
# WebSite  = "https://www.tripadvisor.com/Hotels-g187879-Sardinia-Hotels.html"


###Portugal

# #Madeira
# WebSite = "https://www.tripadvisor.com/Hotels-g189165-Madeira_Islands-Hotels.html"

# #Porto
# WebSite = "https://www.tripadvisor.com/Hotels-g2618568-Porto_District_Northern_Portugal-Hotels.html"

# #Algarve
# WebSite = "https://www.tripadvisor.com/Hotels-g189111-Algarve-Hotels.html"


# ###Cyprus
#
WebSite = "https://www.tripadvisor.com/Hotels-g190372-Cyprus-Hotels.html"



###
########################################################################################################################################################
csv_file = r'C:\Users\pasch\Documents\TripAdvisor_Scrapping\Data\Unprocessed_Data\Cyprus/Hotels_Name_LinkTotal.csv'


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument("start-maximized")
options.add_argument("--lang=en-US")
driver = webdriver.Chrome( options=options)
driver.get(WebSite)

# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="OK"]'))).click()

counter = 0
cookie_clicked = 0
while True:
	if cookie_clicked == 0:
		try:
			WebDriverWait(driver, 3).until(
					EC.presence_of_element_located((By.XPATH, '//button[text()="Manage Settings"]'))).click()
			cookie_clicked = 1
		except:
			print('\nNo cookie')

	try:
		try:
			time.sleep(2)
			driver.find_element_by_xpath('//button[text()="Decline All"]').click()
		except:
			WebDriverWait(driver, 2).until(
					EC.presence_of_element_located((By.XPATH, '//button[text()="Decline All"]'))).click()
		break
	except:
		print('\nNo Decline')
	if counter >= 3:
		driver.refresh()
		break
	if counter == 2:
		driver.refresh()
	counter += 1


tripadvisor_link="https://www.tripadvisor.com/"



# time.sleep(2)
last = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="taplc_main_pagination_bar_dusty_hotels_resp_0"]//div[@class="pageNumbers"]/span[last()]'))).text)
print('Last = ',last)
hotels = []
time.sleep(2)
Names = []
malakia = 0
for page in range(malakia,last):
    time.sleep(6)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'prw_rup.prw_meta_hsx_responsive_listing.ui_section.listItem')))
    try:
        for window in driver.find_elements_by_class_name('prw_rup.prw_meta_hsx_responsive_listing.ui_section.listItem'):

            Name = window.find_element_by_class_name('property_title.prominent').text

            if Name not in Names and window.find_element_by_class_name('price.__resizeWatch').text:

                Link = window.find_element_by_class_name('property_title.prominent').get_attribute('href')
                try:
                    Price = window.find_element_by_class_name('price.__resizeWatch').text.strip('€')
                except:
                    Price = 'N/A'

                try:
                    Reviews = window.find_element_by_class_name('review_count').text.split(' ')[0]
                except:
                    Reviews = 'N/A'

                Names.append(Name)

                hotels.append({'Name': Name,'Link': Link, 'Price': Price, 'Reviews': Reviews})

            else:
                print('\nAlready Taken : ' + Name + '\n')

    except:
        print('\nException')
        # driver.refresh()
        # time.sleep(10)
        # if Name == hotels[-1]['Name']:
        #     hotels.pop
        #
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located(
        #         (By.CLASS_NAME, 'prw_rup.prw_meta_hsx_responsive_listing.ui_section.listItem')))
        #
        # for window in driver.find_elements_by_class_name(
        #         'prw_rup.prw_meta_hsx_responsive_listing.ui_section.listItem'):
        #
        #     Name = window.find_element_by_class_name('property_title.prominent').text
        #
        #     if Name not in Names:
        #         Link = window.find_element_by_class_name('property_title.prominent').get_attribute('href')
        #         try:
        #             Price = window.find_element_by_class_name('price.__resizeWatch').text
        #         except:
        #             Price = 'N/A'
        #
        #         Names.append(Name)
        #
        #         hotels.append({'Name': Name, 'Link': Link, 'Price': Price})
        #
        #     else:
        #
        #         print('\nAlready Taken : ' + Name + '\n')

        #if counter >= 50: break

    print('page = ', page+1)
    malakia = page
    if page == last - 1:
        break

    else:
        # time.sleep(3)
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Next"]')))
            try:
                element.click()
            except:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[text()="Next"]'))).click()
        except:
            driver.find_element_by_xpath('//span[text()="Next"]')

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="Next"]')))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0')))

driver.close()



with open(csv_file, 'w', encoding='utf-8', newline='') as file:
    fieldnames = hotels[0].keys()

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for data in hotels:
        try:

            writer.writerow(data)

        except:
            print(data)

# #######################################
# #reader
#
# import csv
#
# with open(csv_file, newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#         print(', '.join(row))
