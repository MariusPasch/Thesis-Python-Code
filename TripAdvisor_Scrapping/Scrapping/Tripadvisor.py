# -*- coding: utf-8 -*-

#from Tripadvisor_Hotel_Reviews import Reviews
#from Tripadvisor_Hotel_Information import Hotel_Info

start_csv_file = r'C:\Users\pasch\Documents\TripAdvisor_Scrapping\Data'
pr = r'\Unprocessed_Data'
countries =[r'\Greece', r'\Cyprus', r'\France', r'\Italy', r'\Portugal', r'\Spain', r'\Turkey']
country =  r'\Spain'
c = r'\Hotels_Name_Link.csv'

#
# for country in countries[6:7]:

csv_file = start_csv_file+country+c
Hotel_info_csv_file = start_csv_file+country+ r'\Hotels_Info.csv'
Reviews_csv_file = start_csv_file + country + r'\Reviews_Total.csv'

import csv
import time

collected_data = list(csv.DictReader(open(csv_file, encoding='utf-8')))


# processed_data = []
# for dt in collected_data:
# 	if dt['Price'] != None and dt['Price'] != 'N/A' and dt['Price']  != '':
# 		processed_data.append(dt)


	#######################################################################################################################

	# info = []
	# unused_info = []
	# size = len(processed_data)
	# for item in range(size):
	# 	print('\nProgramm Completed: %.2f'%((item/size)*100) + '%')
	# 	print('\nItem = ',item)
	# 	data = processed_data[item]
	#
	# 	d = {'Name': data['Name'],
	# 		 'Link': data['Link'],
	# 		 'Price': data['Price']
	# 		 }
	#
	# 	try:
	# 		h_i = Hotel_Info(data['Link'])
	# 		time.sleep(1)
	# 		if h_i == 'No reviews':
	# 			unused_info.append(d)
	# 		else:
	# 			d.update(h_i)
	# 			info.append(d)
	#
	# 	except:
	# 		unused_info.append(d)
	#
	#
	#
	#
	# with open(Hotel_info_csv_file, 'w', encoding='utf-8', newline='') as hotels_file:
	# 	fieldnames = info[0].keys()
	#
	# 	writer = csv.DictWriter(hotels_file, fieldnames=fieldnames)
	#
	# 	writer.writeheader()
	# 	for data in info:
	# 		try:
	#
	# 			writer.writerow(data)
	#
	# 		except:
	# 			print(data)


#######################################################################################################################
def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+',encoding='utf-8', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = csv.DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)


hotelswithreviews = []
for dt in collected_data:
	if int(dt['Reviews']) > 5:
		hotelswithreviews.append(dt)



reviews_info = []

unused_info_revs = []
size = len(hotelswithreviews)
print('size = ',size)
trial = range(size)

for item in trial[170:]:
	print('\nProgramm Completed: %.2f'%(((item-trial[0])/len(trial))*100) + '%')
	print('\nHotel Item = ', item)
	data = hotelswithreviews[item]

	d = {'Hotel Name': data['Name'],
		'Link': data['Link'],
	    'Hotel Reviews': data['Reviews']
		}

	# try:
	hotel_reviews = Reviews(d['Link'])
	for rev in hotel_reviews:
		rev.update(d)
		reviews_info.append(rev)
		#
		fieldnames = rev.keys()
		try:
			append_dict_as_row(Reviews_csv_file, rev, fieldnames)
		except:
			unused_info_revs.append(rev)

#
# #
# # # #Create csv file  for reviews FIELDNAMES only
# reviews_fieldnames = ['Reviewer Username', 'Reviewer Link', 'Country', 'Rating', 'Date of stay', 'Date of review', 'Title', 'Comment', 'Helpful Votes', 'Contribution Votes', 'Trip Type', 'Value Stars', 'Rooms Stars', 'Service Stars', 'Cleanliness Stars', 'Location Stars', 'Sleep Quality Stars', 'Hotel Name', 'Link', 'Hotel Reviews']
# with open(Reviews_csv_file, 'w', encoding='utf-8', newline='') as reviews_file:
#
#
#     writer = csv.DictWriter(reviews_file, fieldnames=reviews_fieldnames)
#
#     writer.writeheader()
# #





########################################################################################################################






