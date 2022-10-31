start_csv_file = r'C:\Users\pasch\Documents\TripAdvisor_Scrapping\Data'
countries =[r'\France', r'\Italy', r'\Portugal', r'\Spain', r'\Turkey']
country = r'\Cyprus'
pr = r'\Unprocessed_Data'

# regions =[r'\Chania', r'\Corfu', r'\Heraklion', r'\Rhodes', r'\Zakynthos']
# # region = r'\Chania'

# Hotel_info_csv_file = start_csv_file + pr + country + region + r'\Hotels_Info.csv'
# Reviews_csv_file = start_csv_file + pr + country + region + r'\Reviews_Total.csv'


import csv
import time
import re
########################################################################################################################
# #Reviews
# for country in countries:
allrevs = []


Hotel_info_csv_file = start_csv_file  + country  + r'\Hotels_Info.csv'

htls = list(csv.DictReader(open(Hotel_info_csv_file, encoding='utf-8')))
htlsregions = {}

for h in htls:
	htlsregions[h["Name"]] = h['Hotel Region']


Reviews_csv_file = start_csv_file + pr + country + r'\Reviews_Total.csv'
collected_data = list(csv.DictReader(open(Reviews_csv_file, encoding='utf-8')))

for item in range(len(collected_data)):
	if collected_data[item]["Hotel Name"] in htlsregions.keys():
		collected_data[item]["Hotel Region"] = htlsregions[collected_data[item]["Hotel Name"]]
	else:
		collected_data[item]["Hotel Region"] = 'Unknown' + ', ' + country.strip('\\')
	collected_data[item]['Date of stay'] = collected_data[item]['Date of stay'].strip('Date of stay: ')

	float_list = ['Rating', 'Value Stars', 'Rooms Stars', 'Service Stars',
		   'Cleanliness Stars', 'Location Stars', 'Sleep Quality Stars']
	integer_list = ['Helpful Votes',  'Contribution Votes','Hotel Reviews']
	for key in integer_list:
		if collected_data[item][key] == '' or collected_data[item][key] == 'N/A':
			collected_data[item][key] = 0
		else:
			collected_data[item][key] = int(collected_data[item][key].replace(',', ''))
	for key in float_list:
		if collected_data[item][key] != '':
			collected_data[item][key] = float(collected_data[item][key])

	allrevs.append(collected_data[item])

collected_data = allrevs
Revs_new_file = start_csv_file + country + r'\Reviews_Total.csv'


with open(Revs_new_file, 'w', encoding='utf-8', newline='') as file:
	fieldnames = collected_data[0].keys()

	writer = csv.DictWriter(file, fieldnames=fieldnames)

	writer.writeheader()
	counter = 0
	for data in collected_data:
		try:

			writer.writerow(data)

		except:
			counter += 1
			print(data)
print(country, counter)
# ####
# counter = 0
# float_list = ['Value Stars', 'Rooms Stars', 'Service Stars',
#            'Cleanliness Stars', 'Location Stars', 'Sleep Quality Stars']
# for data in collected_data:
#     count =0
#     for key in float_list:
#         if data[key] != '':
#             count+=1
#     if count == len(float_list):
#         counter+=1
####

########################################################################################################################
#Hotels
# for country in countries:
# alldata =[]
#
# csv_file = start_csv_file + pr + country + r'\Hotels_Name_Link.csv'
# Hotel_info_csv_file = start_csv_file + pr + country  + r'\Hotels_Info.csv'
# Reviews_csv_file = start_csv_file + pr + country  + r'\Reviews_Total.csv'
#
# htls = list(csv.DictReader(open(csv_file, encoding='utf-8')))
# htlsregions = {}
# for h in htls:
# 	htlsregions[h["Name"]] = country.strip('\\')
#
# #
# hotelswithreviews = list(csv.DictReader(open(Reviews_csv_file, encoding='utf-8')))
# hwrvs = []
# for h in hotelswithreviews:
# 	if h['Hotel Name'] not in hwrvs:
# 		hwrvs.append(h['Hotel Name'])
#
# #
# collected_data = list(csv.DictReader(open(Hotel_info_csv_file, encoding='utf-8')))
# print(len(collected_data))
# for item in range(len(collected_data)):
# 	# if collected_data[item]['Name'] in hwrvs:
# 	collected_data[item]['Hotel Region'] = htlsregions[collected_data[item]["Name"]]
# 	price = int(re.findall(r'\d+', collected_data[item]['Price'])[0])
# 	collected_data[item]['Price'] = price
#
# 	if collected_data[item]['Hotel_Class'] != 'N/A':
# 		collected_data[item]['Hotel_Class'] = float(collected_data[item]['Hotel_Class'].split(' ')[0])
# 	elif collected_data[item]['Hotel_Class'] == 'N/A':
# 		collected_data[item]['Hotel_Class'] = ''
# 	float_list = ['Stars', 'Stars_Location', 'Stars_Cleanliness', 'Stars_Service', 'Stars_value', ]
# 	integer_list = ['Reviews', 'Revs_Ecxellent', 'Revs_Verygood', 'Revs_Average', 'Revs_Poor', 'Revs_Terrible']
#
# 	for key in integer_list:
# 		if collected_data[item][key] == '':
# 			collected_data[item][key] = 0
# 		else:
# 			collected_data[item][key] = int(collected_data[item][key].replace(',', ''))
# 	for key in float_list:
# 		if collected_data[item][key] != 'N/A':
# 			collected_data[item][key] = float(collected_data[item][key])
# 		elif collected_data[item][key] == 'N/A':
# 			collected_data[item][key] == ''
#
# 	for key in collected_data[item].keys():
# 		if collected_data[item][key] == 'N/A':
# 			collected_data[item][key] = ''
#
# 	alldata.append(collected_data[item])
#
#
# collected_data = alldata
# Hotels_new_file = start_csv_file + country + r'\Hotels_Info.csv'
#
# with open(Hotels_new_file, 'w', encoding='utf-8', newline='') as file:
# 	fieldnames = collected_data[0].keys()
#
# 	writer = csv.DictWriter(file, fieldnames=fieldnames)
#
# 	writer.writeheader()
# 	for data in collected_data:
# 		try:
#
# 			writer.writerow(data)
#
# 		except:
# 			print(data)
