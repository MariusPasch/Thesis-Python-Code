import pandas as pd
from ast import literal_eval as eval

adf = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Amenities - Room Features - Room Types.xlsx')

hdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdHotels.csv')
hdf['Amenities'] = hdf.Amenities.apply(eval)
hdf['Room_features'] = hdf.Room_features.apply(eval)
hdf['Room_Types'] = hdf.Room_Types.apply(eval)

def presence(lstOlst,types):
	dct = {}
	for lst in lstOlst:
		temp = ''
		for tp in types:
			if tp in lst:
				temp += ' +|+ ' + tp
		# if temp != '': break
		if temp in dct.keys():
			dct[temp] += 1
		else:
			dct[temp] =1

	return {k: v for k, v in sorted(dct.items(), reverse=True, key=lambda item: item[1])}




def slct(select):
	return(adf.loc[adf.Types.isin([select])].Amenities.values)

types = slct('Clean Service')


tot = hdf.Amenities.values





import numpy as np
cls = [np.nan, 1.0, 1.5,2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

# for c in cls:
# 	tot = hdf.loc[hdf.Hotel_Class == c].Amenities.values
# 	print('\n\n C = ',c,'\n')
# 	print(presence(tot,types))


def swim(lst):
	pool = ['Pool', 'Outdoor pool''Indoor pool', 'Pool with view',
       'Shallow end in pool', 'Adult pool', 'Infinity pool',
       'Rooftop pool', 'Plunge pool', 'Saltwater pool','Swimup bar']
	beach = ['Beach', 'Private beach']
	if any(x in lst for x in beach+pool) == False:
		return 0
	elif (any(x in lst for x in pool) and any(x in lst for x in beach)) is True:
		return 2
	else:
		return 1

hdf['Swim_Rating'] = hdf.Amenities.apply(swim)

def internet(lst):
	intrt =['Wifi', 'Free High Speed Internet (WiFi)', 'Free internet',
       'Internet', 'Public wifi']
	if any(x in lst for x in intrt) is True:
		return 1
	else:
		return 0

hdf['Internet_Rating'] = hdf.Amenities.apply(internet)


def spa(lst):
	spafaciities = [ 'Spa', 'Sauna', 'Hot tub','Salon', 'Heated pool', 'Hammam', 'Steam room', 'Solarium']
	massage = ['Massage','Full body massage', 'Facial treatments', 'Foot massage', 'Head massage','Couples massage',  'Neck massage', 'Hand massage', 'Manicure', 'Pedicure']
	if any(x in lst  for x in massage+spafaciities) is False:
		return 0
	elif (any(x in lst for x in massage) and (x in lst for x in spafaciities)) is True:
		return 2
	else:
		return 1
hdf['Spa_Rating'] = hdf.Amenities.apply(spa)


def sports(lst):
	basic = ['Fitness Center with Gym / Workout Room', 'Billiards', 'Table tennis', 'Game room',
	         'Darts','Fitness classes', 'Aerobics', 'Yoga classes',
	         'Fitness Centre with Gym / Workout Room']
	special = ['Tennis court', 'Diving', 'Horseback riding', 'Fishing', 'Windsurfing',
       'Golf course', 'Canoeing', 'Mini golf', 'Water park', 'Hiking']

	if any(x in lst for x in basic+special) is False:
		return 0
	elif any(x in lst for x in special):
		return 2
	else:
		return 1

hdf['Sports_Rating'] = hdf.Amenities.apply(sports)


def bar(lst):
	bartypes = ['Bar / lounge', 'Poolside bar', 'Sun terrace',
       'Shared lounge / TV area', 'Evening entertainment','Rooftop terrace',
        'Coffee shop', 'Sun deck', 'Rooftop bar', 'Patio']
	if any(x in lst for x in bartypes) is False:
		return 0
	elif sum(x in lst for x in bartypes) >=3:
		return 2
	else:
		return 1

hdf['BarEntertainment_Rating'] = hdf.Amenities.apply(bar)


def food(lst):
	rstr = ['Restaurant']
	br = ['Breakfast buffet', 'Free breakfast', 'Breakfast available']
	special = ['Snack bar','Breakfast in the room', 'Special diet menus', 'Outdoor dining area']
	# if any(x in lst for x in rstr+br+special) is False:
	# 	return 0
	# elif (any(x in lst for x in rstr) and any(x in lst for x in br) and any(x in lst for x in special)) is True:
	# 	return 2
	# else:
	# 	return 1

	if (any(x in lst for x in rstr) and any(x in lst for x in br) and any(x in lst for x in special)) is True:
		return 4
	elif any(x in lst for x in ['Restaurant','Outdoor dining area']) is True:
		return 3
	elif 'Free breakfast' in lst:
		return 2
	elif any(x in lst for x in ['Breakfast buffet', 'Breakfast available']):
		return 1
	else:
		return 0

hdf['Food_Rating'] = hdf.Amenities.apply(food)


def family(row):
	lst = row.Amenities
	vrbasic = ['Children Activities (Kid / Family Friendly)']
	basic = ['Kids club',  "Kids' meals",
       "Kids' outdoor play equipment", 'Kids pool',
       "Children's television networks", 'Kid-friendly buffet',
       "Children's playground", 'Indoor play area for children']
	special = ['Babysitting', 'Entertainment staff']
	if any(x in lst for x in vrbasic+basic+special) is False and 'Family rooms' not in row.Room_Types:
		return 0
	elif (any(x in lst for x in special) and any(x in lst for x in vrbasic) and any(x in lst for x in basic)) is True:
		return 2
	else:
		return 1

hdf['Family_Rating'] = hdf[['Amenities','Room_Types']].apply(family,axis=1)


def transport(lst):
	basic = ['Free parking', 'Airport transportation','Parking', 'Taxi service',
	         'Street parking', 'Free public parking nearby', 'Parking garage', 'Secured parking']
	special = ['Car hire', 'Bicycle rental', 'Shuttle bus service']
	if any(x in lst for x in basic+special) is False:
		return 0
	elif any(x in lst for x in special) is True:
		return 2
	else:
		return 1

hdf['Transportation_Rating'] = hdf.Amenities.apply(transport)





def services(lst):
	basic = ['Baggage storage', '24-hour front desk', 'Express check-in / check-out',
	         '24-hour check-in', 'Private check-in / check-out']
	safeguard = ['Concierge', '24-hour security', 'Doorperson']

	if any(x in lst for x in basic+safeguard) is False:
		return 0
	elif (any(x in lst for x in basic) and any(x in lst for x in safeguard)) is True:
		return 2
	else:
		return 1

hdf['Services_Rating'] = hdf.Amenities.apply(services)

def cleaningservices(lst):
	tps = ['Laundry service', 'Dry cleaning', 'Ironing service']
	if any(x in lst for x in tps) is True:
		return 0
	else:
		return 1

hdf['CleanService_Rating'] = hdf.Amenities.apply(cleaningservices)

per = [i/100 for i in range(0,100,5)]
############ROOM################
# import pandas as pd
# from ast import literal_eval as eval

adf = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Amenities - Room Features - Room Types.xlsx')

# hdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdHotels.csv')
# hdf['Amenities'] = hdf.Amenities.apply(eval)
# hdf['Room_features'] = hdf.Room_features.apply(eval)
# hdf['Room_Types'] = hdf.Room_Types.apply(eval)

rofdf = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Amenities - Room Features - Room Types.xlsx',sheet_name='Room_features')

rotdf = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Amenities - Room Features - Room Types.xlsx',sheet_name='Room_Types')


import numpy as np
essential =  np.concatenate((rofdf.loc[rofdf.Categorization == 'Essential'].Room_Amenities.values,rotdf.loc[rotdf.Categorization == 'Essential'].Room_Types.values))

basic = np.concatenate((rofdf.loc[rofdf.Categorization == 'Basic'].Room_Amenities.values,rotdf.loc[rotdf.Categorization == 'Basic'].Room_Types.values))

extra = np.concatenate((rofdf.loc[rofdf.Categorization == 'Extra'].Room_Amenities.values,rotdf.loc[rotdf.Categorization == 'Extra'].Room_Types.values))

luxury = np.concatenate((rofdf.loc[rofdf.Categorization == 'Luxury'].Room_Amenities.values,rotdf.loc[rotdf.Categorization == 'Luxury'].Room_Types.values))

def roomamnts(lsts):
	lst = lsts.Room_features + lsts.Room_Types
	if sum(x in lst for x in essential) >= 4:
		if sum(x in lst for x in basic) >= 5:
			if sum(x in lst for x in extra) >= 3:
				if sum(x in lst for x in luxury) >= 2:
					return 4
				return 3
			return 2
		return 1
	return 0

# x = hdf[['Room_features','Room_Types']].apply(roomamnts,axis=1)
# print('\n0',x.loc[x == 0].size)
# print('\n1',x.loc[x == 1].size,len(essential))
# print('\n2',x.loc[x == 2].size,len(basic))
# print('\n3',x.loc[x == 3].size,len(extra))
# print('\n4',x.loc[x == 4].size,len(luxury))



hdf['Room_Grade'] = hdf[['Room_features','Room_Types']].apply(roomamnts,axis=1)


import pandas as pd
cdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdReviews.csv')

roomstars = cdf.groupby(by='Hotel_Name').Rooms_Stars.mean()
lst = []
for hotel in hdf.Name:
	lst.append(roomstars[hotel])
hdf['Stars_Room'] = lst

def myround(x, base=10):
	try:
		x = x * 10
		x = base * round(x /base)
		return x/10
	except:
		return 1
hdf['Stars_Room'] = hdf.Stars_Room.apply(myround)





cleanlinessstars = cdf.groupby(by='Hotel_Name').Cleanliness_Stars.mean()
lst = []
for hotel in hdf.Name:
	lst.append(cleanlinessstars[hotel])
hdf['Stars_Cleanliness'] = lst


hdf['Stars_Cleanliness'] = hdf.Stars_Cleanliness.apply(myround)


sleepstars = cdf.groupby(by='Hotel_Name').Sleep_Quality_Stars.mean()
lst = []
for hotel in hdf.Name:
	lst.append(sleepstars[hotel])
hdf['Stars_Sleep'] = lst


hdf['Stars_Sleep'] = hdf.Stars_Sleep.apply(myround)
# hdf.plot.scatter(y='Hotel_Class',x='Room_Features_Grade')
#
# def presence(lstOlst,types,oldkeys):
# 	dct = {}
# 	for lst in lstOlst:
# 		for tp in types:
# 			if tp in lst:
# 				if tp not in oldkeys:
# 					if tp in dct.keys():
# 						dct[tp] +=1
# 					else:
# 						dct[tp] =1
#
# 	return {k: v for k, v in sorted(dct.items(), reverse=True, key=lambda item: item[1])}
# import numpy as np
# cls = [np.nan, 1.0, 1.5,2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
#
# for  name in rofdf.Types.unique():
# 	oldkeys = []
# 	types = rofdf.loc[rodf.Types == name].Room_Amenities.values
# 	print('\n',name,'\n\n')
# 	for c in cls:
# 		tot = hdf.loc[hdf.Hotel_Class == c].Room_features.values
# 		print('\n\n C = ',c, len(tot),'\n')
# 		dct = presence(tot,types, oldkeys)
# 		print(dct)
# 		oldkeys += dct.keys()





###################

def walk(grade):
	if pd.isna(grade) is True:
		return 0
	elif grade == 'Car recommended':
		return 1
	elif grade == 'Somewhat walkable':
		return 2
	elif grade == 'Good for walkers':
		return 3
	elif grade == 'Great for walkers':
		return 4
hdf['Location_Walkability_Score'] = hdf.Location_Walkability_Grade
hdf['Location_Walkability_Grade'] = hdf.Location_Walkability.apply(walk)

# 5 25 60 100

def attractions(values):
	if pd.isna(values.Location_Attractions):
		return 0
	elif values.Location_Attractions <= 1:
		return 0
	elif values.Location_Attractions <= 10 and values.Location_Attractions_Distance == 'within 0.3 miles':
		return 1
	elif values.Location_Attractions <= 30:
		if values.Location_Attractions_Distance == 'within 0.3 miles':
			return 2
		elif values.Location_Attractions_Distance == 'within 0.75 miles':
			return 1
		elif values.Location_Attractions_Distance == 'within 5 miles':
			return 0
	elif values.Location_Attractions <= 70:
		if values.Location_Attractions_Distance == 'within 0.3 miles':
			return 3
		elif values.Location_Attractions_Distance == 'within 0.75 miles':
			return 2
		elif values.Location_Attractions_Distance == 'within 5 miles':
			return 1
	elif values.Location_Attractions > 70:
		if values.Location_Attractions_Distance == 'within 0.3 miles':
			return 4
		elif values.Location_Attractions_Distance == 'within 0.75 miles':
			return 3
		elif values.Location_Attractions_Distance == 'within 5 miles':
			return 2


# hdf[['Location_Attractions_Distance','Location_Attractions']].apply(attractions,axis=1).describe(percentiles=[i/100 for i in range(0,100,5)])
hdf['Location_Attraction_Grade'] = hdf[['Location_Attractions_Distance','Location_Attractions']].apply(attractions,axis=1)

def restaurants(values):
	if pd.isna(values.Location_Restaurants):
		return 0
	elif values.Location_Restaurants <= 10:
		return 0
	elif values.Location_Restaurants <= 25 and values.Location_Restaurants_Distance == 'within 0.3 miles':
		return 1
	elif values.Location_Restaurants <= 80:
		if values.Location_Restaurants_Distance == 'within 0.3 miles':
			return 2
		elif values.Location_Restaurants_Distance == 'within 0.75 miles':
			return 1
		elif values.Location_Restaurants_Distance == 'within 5 miles':
			return 0
	elif values.Location_Restaurants <= 160:
		if values.Location_Restaurants_Distance == 'within 0.3 miles':
			return 3
		elif values.Location_Restaurants_Distance == 'within 0.75 miles':
			return 2
		elif values.Location_Restaurants_Distance == 'within 5 miles':
			return 1
	elif values.Location_Restaurants >160:
		if values.Location_Restaurants_Distance == 'within 0.3 miles':
			return 4
		elif values.Location_Restaurants_Distance == 'within 0.75 miles':
			return 3
		elif values.Location_Restaurants_Distance == 'within 5 miles':
			return 2


# hdf[['Location_Restaurants_Distance','Location_Restaurants']].apply(restaurants,axis=1).describe(percentiles=[i/100 for i in range(0,100,5)])
hdf['Location_Restaurants_Grade'] = hdf[['Location_Restaurants_Distance','Location_Restaurants']].apply(restaurants,axis=1)







# hdf['Location_Restaurants_Per_Mile_Grade'] = pd.qcut(hdf.Location_Restaurants_PerMile.fillna(0),5,duplicates='drop',labels=[0,1,2,3,4]).astype('int')
#
#
# hdf['Location_Attractions_Per_Mile_Grade'] = pd.qcut(hdf.Location_Attractions_PerMile.fillna(0),5,duplicates='drop',labels=[0,1,2,3,4]).astype('int')







import pandas as pd
cdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdReviews.csv')
sdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Semantria\Data&Matrices\SemantriaProcessedResults.csv')
sdf.drop(columns=['Unique_ID', 'Comment',
       'topics', 'themes', 'auto_categories'],inplace=True)
Rows = cdf.Row.values
sdf = sdf.loc[sdf.Row.isin(Rows)]
cdf['Sentiment_Polarity'] = sdf.sentiment_polarity.values
cdf['Sentiment_Score'] = sdf.sentiment_score.values


# hdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdHotels.csv')

cdf.set_index('Hotel_Name',inplace=True)


def first_impression(hotel):
	vls = cdf.loc[hotel].sort_values(by='Helpful_Votes')[['Helpful_Votes','Sentiment_Score']].values[-5:]
	votes = []
	sent = []
	for v in vls:
		votes.append(v[0])
		sent.append(v[1])
	w=[]
	for v in votes:
		w.append(v/sum(votes))
	tot = 0
	for i in range(len(sent)):
		tot += sent[i]*w[i]
	if tot<-0.5:
		return 0
	elif tot < -0.05:
		return 1
	elif tot < 0.05:
		return 2
	elif tot <=0.5:
		return 3
	elif tot > 0.5:
		return 4
	return tot


hdf['Revs_First_Impression'] = hdf.Name.apply(first_impression)





# hdf['Hotel_Class'] = hdf.Hotel_Class.fillna(0.5)
#
# pd.qcut(hdf[['Price','Hotel_Class']].apply(lambda x: x.Price/x.Hotel_Class,axis=1),5)

hdf['Price_Grade'] = pd.qcut(hdf.Price,5,labels=[5,4,3,2,1]).astype(int)


hdf['Stars_value'] = hdf.Stars_value.fillna(0)
hdf['Stars_Location'] = hdf.Stars_Location.fillna(0)
hdf['Stars_Service'] = hdf.Stars_Service.fillna(0)
hdf['Stars_Room'] = hdf.Stars_Room.fillna(0)
hdf['Stars_Cleanliness'] = hdf.Stars_Cleanliness.fillna(0)
hdf['Stars_Sleep'] = hdf.Stars_Sleep.fillna(0)

####### Sentiment #########
h = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Sentiment_Matrix.xlsx')
h.sort_values(by='Hotel_Name',inplace=True)
hdf.sort_values(by='Name',inplace=True)

for key in h.keys()[1:]:
	hdf[key + '_Sentiment'] = h[key]

############FINAL#######################################




dct = {'Facilities_Total_Grade': ['Swim_Rating', 'Internet_Rating',
                                'Spa_Rating', 'Sports_Rating',
                                'BarEntertainment_Rating', 'Family_Rating', 'Facilities_Sentiment'],

       'Room_Total_Grade': ['Stars_Room', 'Room_Grade', 'Room_Sentiment'],

       'Location_Total_Grade': ['Stars_Location', 'Transportation_Rating',
                                'Location_Walkability_Grade', 'Location_Attraction_Grade',
                                'Location_Restaurants_Grade', 'Location_Sentiment'],

       'Food_Total_Grade': ['Food_Rating', 'Food_Sentiment'],

       'Value_Total_Grade': ['Stars_value', 'Revs_First_Impression', 'Price_Grade', 'Value_Sentiment'],

       'Service_Total_Grade': ['Stars_Service', 'Services_Rating', 'CleanService_Rating',
                               'Stars_Cleanliness', 'Service_Sentiment']
}

def matrixcreation(row):
	tempdct = {}
	for key in dct.keys():
		temp = 0
		for item in dct[key]:
			temp += row[item] / hdf[item].max()
		temp = temp/len(dct[key])
		tempdct[key] = temp
	return tempdct



a = hdf.apply(matrixcreation,axis=1)
a = a.apply((pd.Series))

a['Hotel'] = hdf.Name.values






##### Cut into 10 equal in size bins for Ranking

# a['Ranking'] = pd.qcut(cdf.groupby(by='Hotel_Name').Rating.mean(),q=10,labels=list(range(10,0,-1))).astype(int).values

###### Rank from individual stars rating avg
import numpy as np

a['Ranking'] = cdf.groupby(by='Hotel_Name').Rating.mean().round(3).rank(method='min',ascending=False).astype(int).values


## Ranking as Stars of TripAdvisor

def ranking(stars):
	try:
		return 11 - int(stars * 2)
	except:
		return 10

a['Ranking'] = hdf.Stars.apply(ranking).values




a = a[['Hotel',  'Facilities_Total_Grade', 'Room_Total_Grade', 'Location_Total_Grade',
       'Food_Total_Grade', 'Value_Total_Grade', 'Service_Total_Grade',
       'Ranking']]


writer = pd.ExcelWriter('Hotel_Criteria_Grade_Sentiment_MatrixContinuous.xlsx', engine='xlsxwriter')

a.rename(columns={'Facilities_Total_Grade': 'Facilities',
                  'Room_Total_Grade': 'Room',
                  'Service_Total_Grade': 'Service',
                  'Room_Total_Grade': 'Room',
                  'Location_Total_Grade': 'Location',
                  'Food_Total_Grade': 'Food',
                  'Value_Total_Grade': 'Value',},inplace=True)
a.to_excel(writer,sheet_name='Grades',index=False)
# h.to_excel(writer,sheet_name='Sentiment',index=False)
writer.close()

for key in a.keys():
	hdf[key] = a[key]

# hdf.sort_values(by='Name',inplace=True)
hdf = hdf[[ 'Country', 'Region', 'Name',
            'Facilities', 'Swim_Rating', 'Internet_Rating', 'Spa_Rating',
            'Sports_Rating', 'BarEntertainment_Rating', 'Family_Rating',
			'Room', 'Stars_Room', 'Room_Grade',
			'Location', 'Stars_Location', 'Location_Walkability_Score', 'Location_Attraction_Grade',
                'Location_Restaurants_Grade', 'Transportation_Rating', 'Location_Walkability_Grade',
                'Location_Walkability','Location_Restaurants',
                'Location_Restaurants_Distance', 'Location_Attractions',
                'Location_Attractions_Distance',
			'Food','Food_Rating',
			'Value','Stars_value','Revs_First_Impression', 'Price_Grade','Hotel_Class','Hotel_Class',
                'Price', 'Reviews', 'Stars',
            'Service', 'Stars_Cleanliness', 'Stars_Service', 'Services_Rating',
            'CleanServce_Rating',   'Stars_Sleep',
        ]]

# #MARKEX CREATION
# import pandas as pd
#
#
#
# df = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')
#
# # df = df.sample(100,ignore_index=True)
# # df = df.head(30)
# r = df.Ranking.unique().tolist()
# r.sort(reverse=True)
# r = pd.Series(r)
# def rank(x):
# 	return r.loc[r == x].index[0] + 1
# df['Ranking'] = df.Ranking.apply(rank)
# # df['Ranking'] = df.Ranking.apply(lambda x: 11-x)
# # df.sort_values(by='Ranking',inplace=True)
# # df['Hotel'] = df.Hotel.apply(lambda x: x.replace(r' ', '_'))
#
# # def trans(x):
# #     return int(round(x,1)*10) + 1
# #
# # for key in df.keys()[1:-1]:
# #     df[key] = df[key].apply(trans)
#
# df = df.sample(frac=0.1,ignore_index=True)
#
# def threedigits(x):
# 	return int(round(x*1000,0))
# for key in df.keys()[1:-1]:
#     df[key] = df[key].apply(threedigits)
#
# options = {'Consumers': 1,
#            'Criteria': 6,
#            'Alternatives': len(df),
#            'Epsilon': 0.0001,
#            'Delta': 0.05,
#            'Post-Optimization': 1
# 			}
#
# Criteria = pd.DataFrame(data={'': df.keys()[1:-1].values,
# 							  'Mon/ty': [1] * 6,
#                               'Type': [1] * 6,
#                               'Worst': [0] * 6,
#                               'Best': [1000] * 6,
#                               'a': [11] * 6 })
#
# # AlternativesNames = x.sort_values(by='Rating',ascending=False).index.values
# # AlternativesNames = df.Hotel.values
# AlternativesNames = pd.Series(df.index).apply(lambda x: 'H' + str(x)).values
#
# keys = df.keys()[1:-1]
# questions = []
# for i in range(len(df)):
# 	questions += df.loc[i][keys].values.tolist()
#
# questions += df.Ranking.values.tolist()
#
# import xlsxwriter
#
#
# wb = xlsxwriter.Workbook('MARKEX_Hotels.xlsx')
#
# sheet1 = wb.add_worksheet(name='Options')
# i=0
# for key in options.keys():
# 	sheet1.write(i, 0, key)
# 	sheet1.write(i, 1, options[key])
# 	i += 1
#
# sheet2 = wb.add_worksheet(name='Criteria')
# j=0
# for key in Criteria.keys():
# 	i=0
# 	sheet2.write(i, j, key)
# 	for v in Criteria[key].values:
# 		i += 1
# 		sheet2.write(i, j, v)
# 	j += 1
#
# sheet3 = wb.add_worksheet(name='AlternativesNames')
# i=0
# for name in AlternativesNames:
# 	sheet3.write(i, 0, name)
# 	i += 1
#
# sheet4 = wb.add_worksheet(name='Answers')
# sheet4.write(0, 0, 'Consumer/Question')
# sheet4.write(1, 0, 1)
#
# for i in range(len(questions)):
# 	sheet4.write(1, i+1, questions[i])
# 	sheet4.write(0, i+1, i+1)
#
# sheet5 = wb.add_worksheet(name='Questions')
# counter = 0
# q = 1
# sheet5.write(1, counter, 'Question No')
# sheet5.write(2, counter, 'consumer')
# sheet5.write(3, counter, 1)
# for i in range(len(AlternativesNames)):
# 	counter += 1
# 	sheet5.write(0, counter, AlternativesNames[i])
# 	for key in df.keys()[1:-1]:
# 		counter += 1
# 		sheet5.write(0, counter, key)
# 		sheet5.write(1, counter, q)
# 		q += 1
# counter += 1
# sheet5.write(0, counter, 'RANKING')
# for j in range(len(AlternativesNames)):
# 	counter += 1
# 	sheet5.write(0, counter, AlternativesNames[j])
# 	sheet5.write(1, counter, q)
# 	q += 1
#
# wb.close()

