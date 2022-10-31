import pandas as pd

# sdf = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Semantria\Data&Matrices\TitleThemes2AspectsFinal.xlsx')
sdf = pd.read_excel( r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\ThemesKeywords2Aspects.xlsx',
                     sheet_name = 'Themes2Aspects')

sdf = sdf.loc[sdf.Aspects.dropna().index]
Aspects = {}
for index in sdf.index:
	Aspects[sdf.loc[index]['titles']] = sdf.loc[index]['Renewed']

import pickle
cdf = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Semantria\Data&Matrices\OnlyThemesSemantriaBigrammed.p','rb'))



# scdf = cdf.sample(frac=0.3,random_state=0)
# def presence(themes,word):
# 	for dict in themes:
# 		if word in dict['title']:
# 			return True
# 	return False
#
# def keyword(themes,word):
# 	temp = []
# 	for dict in themes:
# 		if word in dict['title']:
# 			temp.append(dict['title'])
#
# 	return temp
#
# title = 'home'
#
# def dosto(title):
# 	scdf = cdf.sample(frac=1)
# 	k = scdf.loc[scdf.BigrammProcessed.apply(lambda x: presence(x,title))].BigrammProcessed.apply(lambda x: keyword(x,title))
# 	print(k)
# 	c = scdf.loc[scdf.BigrammProcessed.apply(lambda x: presence(x,title))].Comment
# 	if '_' in title: title = title.replace('_',' ')
# 	print([s for s in c.values[0].split('.') if title in s])
# 	print([s for s in c.values[1].split('.') if title in s])
# 	print([s for s in c.values[2].split('.') if title in s])
#
#
# dosto('')


#####################
# import pandas as pd
# sdf = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Semantria\Data&Matrices\TitleThemes2AspectsFinal.xlsx')
#
# sdf.rename(columns={'titles':'ThemesKeyWords','Renewed':'Specific_Aspects'},inplace=True)
#
# dct = {'Facilities_Total':['Facilities','Spa','Internet','Sports Activities','Bar/Entertainment','Family Friendly','Swim','Pool','Beach'],
#        'Room_Total':['Room','Room Facilities','View','Apartment/Autonomy','Room Types','Bathroom','Sleep'],
#        'Location_Total': ['Location','Transportation','Near Area','Walkability','Attractions'],
#        'Food_Total': ['Food','Restaurant','Breakfast/Buffet'],
#        'Service_Total': ['Service','Staff','Reservation/Check In','Cleanliness','Atmosphere'],
#        'Value_Total': ['Value','Price','Reviews']}
# def trans(aspect):
# 	for key in dct.keys():
# 		for item in dct[key]:
# 			if item == aspect:
# 				return key.split('_')[0]
# 	return aspect
#
# sdf['Aspects'] = sdf.Specific_Aspects.apply(trans)
#
#
# with pd.ExcelWriter('test.xlsx') as writer:
# 	sdf[['ThemesKeyWords', 'times', 'Aspects']].to_excel(writer,sheet_name='Themes2Aspects',index=False)
# 	sdf[['ThemesKeyWords', 'times', 'Specific_Aspects']].to_excel(writer, sheet_name='Themes2AspectsSpecific',index=False)
# 	for key in dct.keys():
# 		key1 = key.split('_')[0]
# 		sdf.loc[sdf.Aspects == key1][['ThemesKeyWords','times']].to_excel(writer,sheet_name=key,index=False)
# 		for a in dct[key]:
# 			key2 = a.replace('/', '-')
# 			sdf.loc[sdf.Specific_Aspects == a][['ThemesKeyWords','times']].to_excel(writer,sheet_name=key2,index=False)

##########

import pandas as pd
adf = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\ThemesKeywords2Aspects.xlsx', sheet_name = 'Themes2Aspects')
adf = adf.loc[adf.Aspects.dropna().index]
Aspects = {}
for index in adf.index:
	Aspects[adf.loc[index]['ThemesKeyWords']] = adf.loc[index]['Aspects']

df = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdReviews.csv')

import pickle
cdf = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Semantria\Data&Matrices\OnlyThemesSemantriaBigrammed.p','rb'))
cdf = cdf.loc[cdf.Row.isin(df.Row.values)]

cdf.drop(columns=['Comment', 'themes'], inplace=True)


existingTitles = Aspects.keys()


def Theme2Aspect(themes):
	temporary = []
	# print('.|.')
	for theme in themes:
		titles = theme['title']
		aspects = []
		for word in titles:
			if word in existingTitles:
				if Aspects[word] not in aspects:
					aspects.append(Aspects[word])
		# themes[i]['title'] = aspects
		if aspects :
			temp={}
			for key in ['strength_score','sentiment_score','sentiment_polarity']:
				temp[key] = theme[key]
			temp['title'] = aspects
			temporary.append(temp)
	# cdf.loc[index, 'Aspects'] = themes
	# longlist.append(temporary)
	return temporary


cdf['Aspects'] = cdf.BigrammProcessed.apply(Theme2Aspect)

Aspects = []
for a in cdf.Aspects[:1000]:
	for d in a:
		for w in d['title']:
			if w not in Aspects:
				Aspects.append(w)






# hotelPass = df.Hotel_Name.value_counts().keys()[df.Hotel_Name.value_counts()>30]
# df = df.loc[df.Hotel_Name.isin(hotelPass)]

df.drop(columns=['Reviewer_ID', 'Reviewer_Username', 'Reviewer_Number_of_Reviews',
       'Reviewer_Link', 'Reviewer_Country', 'Date_of_stay',
       'Date_of_review', 'Title', 'Comment', 'Comment_Word_Count',
       'Helpful_Votes', 'Contribution_Votes', 'Trip_Type',  'Hotel_Link', 'Hotel_Reviews',
       'Comment_Memory_Size'] ,inplace=True)
# df.set_index('Row',inplace=True)

cdf.set_index('Row',inplace=True)
df.set_index('Row',inplace=True)

df['Polarity'] = cdf['sentiment_polarity']
df['Sentiment_Score'] = cdf['sentiment_score']


temp = {'Hotel_Country': df.Hotel_Country.unique(),
        'Hotel_Region': df.Hotel_Region.unique(),
        'Hotel_Name': df.Hotel_Name.unique()
		}

import numpy as np


def sentiment(theme):
	dctaspect = {}
	for a in Aspects:
		dctaspect[a] = np.nan
	for dct in theme:
		for s in dct['title']:
			if pd.isna(dctaspect[s]):
				dctaspect[s] = dct['sentiment_score']

			else:
				dctaspect[s] += dct['sentiment_score']

	return dctaspect

d = cdf.Aspects.apply(lambda x: pd.Series(sentiment(x)))

frames = [df,d]

matrix = pd.concat(frames,axis=1)

matrix = matrix[['Hotel_Country', 'Hotel_Region', 'Hotel_Name', 'Rating', 'Polarity',
    'Sentiment_Score','Value_Stars', 'Rooms_Stars', 'Service_Stars',
    'Cleanliness_Stars', 'Location_Stars', 'Sleep_Quality_Stars','Service', 'Facilities', 'Room', 'Location', 'Food', 'Value']]



# hotelpass = matrix.Hotel_Name.value_counts().loc[matrix.Hotel_Name.value_counts()>=75]
# matrix = matrix.loc[matrix.Hotel_Name.isin(hotelpass)]
#
#
matrix.to_excel(r'Matrix(75revsndGreater).xlsx')

matrix.groupby(by=['Hotel_Country','Hotel_Region','Hotel_Name']).mean().to_excel('SentimenHotelMatrix.xlsx')



import pandas as pd

matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Matrix.xlsx')

# from sklearn.model_selection import train_test_split
# X = matrix.Sentiment_Score.values.reshape(-1,1)
# y = matrix.Rating.values.reshape(-1,1)
# X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True)
#
# from sklearn.naive_bayes import GaussianNB
# gnb = GaussianNB()
# gnb.fit(X_train, y_train)
# print('Accuracy of GNB classifier on training set: {:.2f}'
#      .format(gnb.score(X_train, y_train)))
# print('Accuracy of GNB classifier on test set: {:.2f}'
#      .format(gnb.score(X_test, y_test)))




nontrip = ['Value','Room','Service','Cleanliness','Near Area','Sleep']

trip = ['Value_Stars', 'Rooms_Stars',
       'Service_Stars', 'Cleanliness_Stars', 'Location_Stars',
       'Sleep_Quality_Stars']

asps = [ 'Facilities', 'Food', 'Service', 'Room',
       'Entertainment & Family Friendly', 'Near Area', 'Atmosphere', 'Value',
       'Sea', 'Sleep', 'Cleanliness', 'Transportation']

#
# for a in range(len(trip)):
# 	print('\n',trip[a])
# 	same = matrix.loc[matrix[trip[a]].dropna().index][nontrip[a]].dropna().index
# 	print('Accuracy of GNB classifier on test set: {:.2f}'
# 	     .format(gnb.score(matrix.loc[same][nontrip[a]].values.reshape(-1,1), matrix.loc[same][trip[a]].values.reshape(-1,1))))
#


cols = trip + asps
# temp = {'Hotel_Country': matrix.Hotel_Country.unique(),
#         'Hotel_Region': matrix.Hotel_Region.unique(),
#         'Hotel_Name': matrix.Hotel_Name.unique()
# 		}

res = matrix.groupby(by=['Hotel_Country','Hotel_Region','Hotel_Name']).mean()

countries = res.index.get_level_values(level=0).unique()
regions = matrix.Hotel_Region.unique()

for country in countries:
	print('\n', country,sum(res.loc[country][cols].apply(lambda x: any(pd.isna(x)),axis=1)),'\n')
	regions = res.loc[country].index.get_level_values(level=0).unique()
	for region in regions:
		print(region, sum(res.loc[country,region][cols].apply(lambda x: any(pd.isna(x)),axis=1)), len(res.loc[country,region][cols].apply(lambda x: any(pd.isna(x)),axis=1)))







