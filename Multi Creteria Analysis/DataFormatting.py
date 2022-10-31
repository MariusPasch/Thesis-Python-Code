import pandas as pd
import numpy as np

#
# hdf =  pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')
#
# hdf['Country'] = hdf['Hotel Region'].apply(lambda x: x.split(' ,')[-1])
#
# hdf['Region'] = hdf['Hotel Region'].apply(lambda x: x.split(' ,')[0])
#
# import pickle
# infod = pickle.load(open(r'C:\Users\pasch\Documents\TripAdvisor_Scrapping\HotelLocationInfoOld.p','rb'))
# info = infod['info']
# hotelnames = infod['hotelnames']
#
# s = []
# for index in hdf.index:
# 	for i in range(len(info)):
# 		if index == info[i][0]:
# 			s.append(info[i][1])
# new = pd.DataFrame(data={'Info': s})
#
# def attrreturn(x,pos,toint=False):
# 	if toint is True:
# 		if x == '':
# 			return 0
# 		return int(x.split('\n')[pos])
# 	if x == '':
# 		return ''
#
# 	return x.split('\n')[pos]
#
#
# new['Walkability_Grade'] = new['Info'].apply(lambda x: attrreturn(x,0,toint=True))
# new['Walkability'] = new['Info'].apply(lambda x: attrreturn(x,1))
#
# new['Restaurants'] = new['Info'].apply(lambda x: attrreturn(x,3,toint=True))
# new['Restaurants_Distance'] = new['Info'].apply(lambda x: attrreturn(x,5))
#
# new['Attractions'] = new['Info'].apply(lambda x: attrreturn(x,6,toint=True))
# new['Attractions_Distance'] = new['Info'].apply(lambda x: attrreturn(x,8))
#
# keys = ['Walkability_Grade','Walkability','Restaurants','Restaurants_Distance','Attractions','Attractions_Distance']
#
# for key in keys:
# 	hdf['Location_'+key] = new[key]
#
# hdf.drop(columns='Hotel Region',inplace=True)
# ##Reviews################################################################################################################
#
# rdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Reviews_Total_OnlyEnglish.csv')
#
#
# #Throw Duplicates
#
# rdf = rdf.loc[~(rdf.duplicated(keep=False) & rdf.duplicated())]
#
# rdf.drop(columns='Hotel_Region',inplace=True)
#
# import pandas as pd
# import numpy as np
# rdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Reviews.csv')
# hdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')
# hts = hdf.Name.values
# keys=[]
# for index in rdf.Hotel_Name.index:
# 	hn = rdf.Hotel_Name[index]
# 	if hn not in hts:
# 		if hn not in keys:
# 			keys.append(hn)
#
#
# for key in keys:
# 	rdf = rdf.loc[~(rdf.Hotel_Name == key)]
#
# rdf.dropna(subset='Reviewer_Username',inplace=True)
#
# countries = []
# regions = []
#
# for index in rdf.index:
# 	row = hdf.loc[hdf.Name == rdf['Hotel_Name'][index]]
# 	countries.append(row.Country.values[0])
# 	regions.append(row.Region.values[0])
# #
# rdf['Hotel_Country'] = countries
# rdf['Hotel_Region'] = regions
#
#
# rdf.rename(columns={'Reviewer Username': 'Reviewer_Username', 'Reviewer Link': 'Reviewer_Link', 'Country': 'Reviewer_Country',
# 			'Date of stay': 'Date_of_stay', 'Date of review': 'Date_of_review','Helpful Votes': 'Helpful_Votes',
#             'Contribution Votes': 'Contribution_Votes', 'Trip Type': 'Trip_Type',
#             'Value Stars': 'Value_Stars', 'Rooms Stars': 'Rooms_Stars',
#             'Service Stars': 'Service_Stars', 'Cleanliness Stars': 'Cleanliness_Stars',
#             'Location Stars': 'Location_Stars', 'Sleep Quality Stars': 'Sleep_Quality_Stars', 'Hotel Name': 'Hotel_Name',
#             'Hotel Reviews': 'Hotel_Reviews', 'Hotel Region': 'Hotel_Region'},inplace=True)
#
#
# rdf.to_csv('Reviews.csv')

hdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')


keys = ['Location_Walkability_Grade',
       'Location_Walkability', 'Location_Restaurants',
       'Location_Restaurants_Distance', 'Location_Attractions',
       'Location_Attractions_Distance']

def permile(num,dist):
	if np.isnan(num) == True:
		return ''
	if dist == 'within 0.3 miles':
		return num/0.3
	if dist == 'within 0.75 miles':
		return num/0.75
	if dist == 'within 5 miles':
		return num/5


new = hdf[keys]
new['Location_Restaurants_PerMile'] = new[['Location_Restaurants',
       'Location_Restaurants_Distance']].apply(lambda x: permile(x.Location_Restaurants,x.Location_Restaurants_Distance),axis=1)
new['Location_Attractions_PerMile'] = new[['Location_Attractions',
       'Location_Attractions_Distance']].apply(lambda x: permile(x.Location_Attractions,x.Location_Attractions_Distance),axis=1)


a=new.Location_Walkability.fillna(0).replace([ 'Great for walkers','Good for walkers','Somewhat walkable','Car recommended'],[4,3,2,1])
b=pd.qcut(new.Location_Restaurants_PerMile.fillna(0),6,duplicates='drop',labels=[0,1,2,3,4]).astype('int')
c=pd.qcut(new.Location_Attractions_PerMile.fillna(0),6,duplicates='drop',labels=[0,1,2,3,4]).astype('int')


from pandas.plotting import scatter_matrix

scatter_matrix(m[['b','a','c']], alpha=0.2, figsize=(6, 6), diagonal="kde")

from pandas.api.types import CategoricalDtype
cat_dtype = CategoricalDtype(
    categories=[4, 3, 2, 1], ordered=True)


# selected = ['Name', 'Link', 'Price', 'Reviews', 'Stars',
# 'Stars_Location', 'Stars_Cleanliness', 'Stars_Service', 'Stars_value', 'Hotel_Class',
# 'Amenities','Room_Features', 'Room_Types',
# 'Revs_Ecxellent', 'Revs_Verygood', 'Revs_Average', 'Revs_Poor',
# 'Revs_Terrible', 'Country', 'Region',
# 'Location_Walkability','Location_Restaurants_PerMile',
# 'Location_Attractions_PerMile']
#
# key = 'Room_Types'
# pos = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Matrices\Amenities - Room Features - Room Types.xlsx',sheet_name=key)
# tr = hdf[key].apply(eval).values
# pos = pos[pos.columns[0]].values
# boolist = []
# for index in hdf.index:
# 	bool = ''
# 	for p in pos:
# 		if p in tr[index]:
# 			bool += '1'
# 		else:
# 			bool += '0'
# 	boolist.append(bool)
# hdf[key] = boolist

##########Amenities RoomTypes RoomFeatures##############################
import pandas as pd
# hdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')
hdf = pd.read_csv(r'/old/crpdHotels.csv')

items = ['Amenities', 'Room_features', 'Room_Types']
def removeblank(x):
	while '' in x:
		x.remove('')
	return x
writer = pd.ExcelWriter('Amenities - Room Features - Room Types.xlsx', engine='xlsxwriter')
itemdataframe = []
for item in range(len(items)):
	new = hdf[items[item]].apply(eval).apply(removeblank).to_list()

	trnew = []
	for n in new:
		temp = []
		for i in n:
			if 'amenity_' in i:
				i = i.split('amenity_')[-1].replace('_',' ').capitalize()
			if i == 'tags_category_tag_non_smoking_rooms_1':
				i = 'Non-smoking rooms'
			temp.append(i)
		trnew.append(temp)

	new = trnew
	uniques = []
	for l in new:
		for a in l:
			# if '' in l:
			# 	print(l)
			# 	break
			if a not in uniques:
				uniques.append(a)

	def presence(x,key):
		if key in x: return 1
		if key not in x: return 0

	dct = {}
	for key in uniques:
		dct[key] = [presence(x,key) for x in new]

	itemdataframe = pd.DataFrame(data=dct)
	itemdataframe.describe().transpose().to_excel(writer,sheet_name=items[item])
writer.save()

# from sklearn.cluster import KMeans
# import numpy as np
#
# kmeans = KMeans(n_clusters=5, random_state=0).fit(amenities.values)




hdf.drop(columns=['Link', 'Location'])
########################################################################################################################
import pandas as pd
import numpy as np
rdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Reviews.csv')
reviewersinfo = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\ReviewersInfo.csv')

uniques = {}
times = {}
usernames = rdf.Reviewer_Username.values
usrnm2num = []
counter = 1
for u in usernames:
	if u not in uniques.keys():
		uniques[u] = counter
		times[u] = 1
		usrnm2num.append(counter)
	else:
		times[u] += 1
		usrnm2num.append(uniques[u])
	counter += 1
print(len(uniques.keys()))

# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="geoapiExercises")
# countries = []
# mrating = []
# srating = []
# trptp = []
# nms = list(uniques.keys())
# counter  = -10000
for i in range(40258,len(nms)):
	key = nms[i]
	rdata = rdf.loc[rdf.Reviewer_Username == key]
	c = rdata.Reviewer_Country.values[0]

	if c == '~~~':
		countries.append(np.nan)
	elif type(c) ==  str:
		try:
			countries.append(geolocator.geocode(c, language="en")[-2].split(', ')[-1])
		except:
			countries.append(c.split(', ')[-1])
	else:
		countries.append(c)
	trptp.append(rdata.Trip_Type.describe()['top'])
	mrating.append(rdata.Rating.mean())
	srating.append(rdata.Rating.std())
	if i == counter +10000:
		print(i)
		counter = i

countries = []
counter = -10000
i =0
dct = reviewersinfo[['Reviewer_Username','ID']].set_index('Reviewer_Username').to_dict()['ID']

for n in rdf.Reviewer_Username.values:
	countries.append(dct[n])

	if i == counter +10000:
		print(i)
		counter = i
	i += 1
# rdf = rdf.loc[rdf.Reviewer_Username.dropna()]

# for key in uniques.keys():
# 	trptp.append(rdf.loc[rdf.Reviewer_Username == key].Trip_Type.describe()['top'])

# reviewers = pd.DataFrame(data={
#                                'usernames': uniques.keys(),
#                                'reviews': times.values(),
#                                 'Country': countries,
# 								'Trip_Type': trptp,
# 								'Means_Rating': mrating,
# 								'STD_Rating': srating})
ids=[]
multiple = []
helpful = []
for n in reviewersinfo.usernames.values:
	ids.append(uniques[n])
	if rdf.loc[rdf.Reviewer_Username == n].Hotel_Country.describe()['unique'] >= 2:
		multiple.append(1)
	else:
		multiple.append(0)
	try:
		helpful.append(rdf.loc[rdf.Reviewer_Username == n].Helpful_Votes.mean())
	except:
		helpful.append(0)

reviewersinfo['ID'] = ids
reviewersinfo['MultipleHotelCountrie'] = multiple
reviewersinfo['HelpfulVotesAverage'] = helpful

reviewersinfo.to_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\ReviewersInfo.csv',index=False)

import operator

sorted_x = sorted(times.items(), key=operator.itemgetter(1))

rdf.drop(columns='',inplace=True)
# replacement = {'nan': '', 'Traveled solo': 1, 'Traveled with family': 2,
# 				'Traveled as a couple':3, 'Traveled with friends': 4, 'Traveled on business': 5,
#                 'Travelled as a couple': 6, 'Travelled with family': 7,
#                 'Travelled with friends': 8, 'Travelled solo': 9, 'Travelled on business': 10}
#
# rdf['Trip_Type'] = rdf['Trip Type'].replace(replacement)
# def contryrev()
# rdf.Country.apply()
#
# c = rdf.Country.values
# for i in range(len(c)):


################### PIVOT TABLES ################################################################
import pandas as pd

hdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')

rdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Reviews.csv')

reviewersinfo = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\ReviewersInfo.csv')

r''
pivot = rdf[['Hotel_Name','Trip_Type']].groupby(by='Hotel_Name')

############## Formatting ########################################################################3





# wordcount = []
# def comment_word_count(comment):
# 	return len(comment.split())
#
# rdf['Comment_Word_Count'] = rdf.Comment.apply(comment_word_count)
#
# newrdf= rdf[['Row', 'Reviewer_ID', 'Reviewer_Username', 'Reviewer_Number_of_Reviews','Reviewer_Country', 'Rating', 'Comment_Word_Count', 'Date_of_stay',
#        'Date_of_review','Helpful_Votes',
#        'Contribution_Votes', 'Trip_Type', 'Value_Stars', 'Rooms_Stars',
#        'Service_Stars', 'Cleanliness_Stars', 'Location_Stars',
#        'Sleep_Quality_Stars', 'Hotel_Name','Hotel_Reviews',
#        'Hotel_Country', 'Hotel_Region']]
#
# newrdf.to_csv('Reviews.csv')

rdf['Comment_Word_Count'].describe()
rdf['Comment_Memory_Size'] = rdf.Comment.apply(lambda x: sys.getsizeof(x))

comsize = 2048

#5%-95%
revsup = 2817
revslo = 75
comup = 479
comlo = 39

#10%-90%
revsup = 1964
revslo = 125
comup = 353
comlo = 45

# one = len(rdf.loc[(rdf.Hotel_Reviews>revslo) &(rdf.Hotel_Reviews<revsup) & (rdf.Comment_Word_Count>comlo) & (rdf.Comment_Word_Count<comup)])
one = len(rdf.loc[(rdf.Hotel_Reviews>revslo) & (rdf.Comment_Word_Count>comlo) & (rdf.Comment_Word_Count<comup)])
two = len(hdf.loc[hdf.Reviews>revsup]) *revsup
print('Hotels: ',len(rdf.loc[(rdf.Hotel_Reviews>revslo)  & (rdf.Comment_Word_Count>comlo) & (rdf.Comment_Word_Count<comup)].Hotel_Name.unique()))
print('\nReviews: ',one+two)

cropped = rdf.loc[(rdf.Hotel_Reviews>revslo)  & (rdf.Comment_Word_Count>comlo) & (rdf.Comment_Memory_Size<comsize)]

counter = 0
temp = cropped.Hotel_Name[0]
lst = []
for i in cropped.index:
	if cropped.Hotel_Reviews[i] >revsup:
		if temp == cropped.Hotel_Name[i]:
			if counter < revsup:
				lst.append(i)
				counter += 1
		else:
			temp = cropped.Hotel_Name[i]
			counter = 0
			lst.append(i)
	else:
		lst.append(i)

cropped = cropped.loc[lst]

hots = cropped.Hotel_Name.unique().tolist()

lst = []
for i in hdf.index:
	if hdf.Name[i] in hots:
		lst.append(i)

hdf_cropped = hdf.loc[lst]




import pandas as pd

cdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdReviews.csv')

# cdf.Hotel_Name.value_counts().describe(percentiles=[(i/100) for i in range(0,100,5)])

hotelpass = cdf.Hotel_Name.value_counts().loc[cdf.Hotel_Name.value_counts() >= 30].keys().values

cdf = cdf.loc[cdf.Hotel_Name.isin(hotelpass)]

cdf.to_csv(r'crpdReviews.csv',index=False)

SelectedRows = cdf.Row.values

hdf = pd.read_csv(r'/old/crpdHotels.csv')

hdf = hdf.loc[hdf.Name.isin(hotelpass)]

hdf.to_csv(r'crpdHotels.csv',index=False)

comdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdComments.csv')

comdf = comdf.loc[comdf.Row.isin(SelectedRows)]

comdf.to_csv(r'crpdComments.csv',index=False)



