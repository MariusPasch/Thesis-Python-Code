# This is a sample Python script.

import csv
heraklion = r'/Heraklion'

laptop = r'C:\Users\pasch\Documents\TripAdvisor_Scrapping\Data\Unprocessed_Data'
pc = r'C:\Users\Palios\PycharmProjects\TripAdvidor\Data\Unprocessed_Data'

location = laptop

hotels_csv_file = location + heraklion + r'\Hotels_Name_Link.csv'
Reviews_csv_file = location + heraklion + r'/Reviews_Total.csv'
Reviewer_other_info_csv_file = location + heraklion + r'\Reviewer_other_info.csv'

# collected_data = list(csv.DictReader(open(Reviews_csv_file, encoding='utf-8')))
#
# contributions =[]
# for data in collected_data:
# 	if data['Contribution Votes'] == '':
# 		contributions.append(0)
# 	else:
# 		contributions.append(int(data['Contribution Votes'].replace(',','')))
#
# #contributions.sort()
# wanted_clusters = 15
# from sklearn.cluster import KMeans
# import numpy as np
# X=[]
# for c in contributions:
# 	try:
# 		X.append([c])
# 	except:
# 		print(c)
# X = np.array(X)
#
#
# kmeans = KMeans(n_clusters=wanted_clusters, random_state=0).fit(X,y=None)
# print(kmeans.labels_)
#
# print(kmeans.cluster_centers_)
#
#
#
# # cluster_map = pd.DataFrame()
# # cluster_map['data_index'] = data.index.values
# # cluster_map['cluster'] = km.labels_
#
# def ClusterIndicesNumpy(clustNum, labels_array): #numpy
#     return np.where(labels_array == clustNum)[0]
#
# def ClusterIndicesComp(clustNum, labels_array): #list comprehension
#     return np.array([i for i, x in enumerate(labels_array) if x == clustNum])
#
# for i in range(wanted_clusters):
# 	cl=X[ClusterIndicesNumpy(i, kmeans.labels_)]
# 	print("\nmin,max =", cl.min(),cl.max(),'\nSize of cluster=',len(cl))
# 	# print('\nSize of cluster=',len(cl))

########################################################################################################################


collected_data = list(csv.DictReader(open(Reviewer_other_info_csv_file, encoding='utf-8')))


most_common_countries = {}

for data in collected_data:
	loc = data['Hotel Location'].split(', ')[-1]
	if loc not in most_common_countries.keys():
		most_common_countries[loc] = 1
	else:
		most_common_countries[loc] += 1


most_common_countries = dict(sorted(most_common_countries.items(), key=lambda item: item[1]))
print(most_common_countries)
most_common_countries.pop('Greece')
counter=0
for key in most_common_countries.keys():
	counter += most_common_countries[key]

for key in most_common_countries.keys():
	most_common_countries[key] = (most_common_countries[key] / counter)*100

print(most_common_countries)

##################################################################
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
#
# hotels = list(csv.DictReader(open(hotels_csv_file, encoding='utf-8')))
# hother = []
# for h in hotels:
# 	hother.append(h['Name'])
#
# for item in range(len(collected_data)):
# 	try:
# 		loc = collected_data[item]['Hotel Location'].split(', ')[-2]
# 	except:
# 		loc = collected_data[item]['Hotel Location'].split(', ')[-1]
# 	if loc == 'Crete':
# 		if collected_data[item]['Hotel Name'] not in hother:
# 			Link = collected_data[item]['Hotel Link']
# 			options = webdriver.ChromeOptions()
# 			options.add_argument('--ignore-certificate-errors')
# 			options.add_argument('--incognito')
# 			options.add_argument("start-maximized")
# 			options.add_argument("--lang=en-US")
# 			driver = webdriver.Chrome(options=options)
# 			driver.get(Link)
#
# 			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="OK"]'))).click()
#
# 			l = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//div[@id="taplc_trip_planner_breadcrumbs_0"]/ul/li[4]'))).text
#
# 			collected_data[item]['Hotel Location'] = l + ', Greece'
# 			driver.close()
#
#
# 		else:
# 			collected_data[item]['Hotel Location'] = 'Heraklion Prefecture, Greece'
#
# with open(Reviewer_other_info_csv_file, 'w', encoding='utf-8', newline='') as reviews_file:
#     fieldnames = collected_data[0].keys()
#
#     writer = csv.DictWriter(reviews_file, fieldnames=fieldnames)
#
#     writer.writeheader()
#     for data in collected_data:
#         try:
#
#             writer.writerow(data)
#
#         except:
#             print(data)
##################################################################


# most_common = {}
#
# for data in collected_data:
# 	if data['Hotel Location'].split(', ')[-1] == 'Spain':
# 		break
# 		try:
# 			loc = data['Hotel Location'].split(', ')[-2]
# 		except:
# 			loc = data['Hotel Location'].split(', ')[-1]
# 		if loc not in most_common.keys():
# 			most_common[loc] = 1
# 		else:
# 			most_common[loc] += 1
#
#
# most_common = dict(sorted(most_common.items(), key=lambda item: item[1]))
#
# # most_common.pop('Heraklion Prefecture')
# # most_common.pop('London')
#
# counter=0
# for key in most_common.keys():
# 	counter += most_common[key]
#
# for key in most_common.keys():
# 	most_common[key] = (most_common[key] / counter)*100
#
# print(most_common)
