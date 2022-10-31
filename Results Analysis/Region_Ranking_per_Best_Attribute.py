import numpy as np
import pandas as pd

dct = {'Facilities': ['Swim_Rating', 'Internet_Rating',
                                'Spa_Rating', 'Sports_Rating',
                                'BarEntertainment_Rating', 'Family_Rating', 'Facilities_Sentiment'],

       'Room': ['Room_Grade', 'Stars_Sleep','Stars_Room', 'Room_Sentiment'],

       'Location': ['Transportation_Rating',
                                'Location_Walkability_Grade', 'Location_Attraction_Grade',
                                'Location_Restaurants_Grade','Stars_Location',  'Location_Sentiment'],

       'Food': ['Food_Rating', 'Food_Sentiment'],

       'Value': ['Price_Grade', 'Revs_First_Impression', 'Stars_value', 'Value_Sentiment'],

       'Service': ['Stars_Service', 'Services_Rating', 'CleanService_Rating',
                               'Stars_Cleanliness', 'Service_Sentiment']
}


evaluation_matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx').rename(columns={'Hotel':'Name'})

totalInfo = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Total_Info_MCM.xlsx')

complete_matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')

totalInfo = pd.merge(totalInfo,evaluation_matrix,on='Name')
totalInfo['Hotel_Class'] = totalInfo.Hotel_Class.fillna(0.5).apply(lambda x: int(round(x+0.5,1)))

def toper(x):
	return str(np.round(x*100,1))+'%'

#######################   Hotel Class   -     Country   ################################################################
wts = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Weights.xlsx',sheet_name='Hotel_Class').set_index('Category')

grps = totalInfo.groupby(by=['Hotel_Class','Country','Name']).first()



writer = pd.ExcelWriter('Presentation_Categorization.xlsx', engine='xlsxwriter')


for c in range(1,6):

	####################################################################################################################
	tempgrp = grps.loc[c,:,:]
	topsisweights = wts.loc[c]
	criterias = np.array([True, True, True, True, True, True])

	t = Topsis(tempgrp[['Facilities', 'Room', 'Location', 'Food', 'Value', 'Service']].values, topsisweights, criterias)

	t.calc()
	tempgrp['TopsisBestCategory'] = t.best_similarity
	####################################################################################################################

	totaldata = []
	for cntry in totalInfo.Country.unique():
		cat_biggest_weight = wts.loc[c].sort_values(ascending=False).keys()[0]
		weight_cat = wts.loc[c].sort_values(ascending=False)[0]
		data = {'Country': cntry, cat_biggest_weight +' (Weight: ' + str(weight_cat) + ')': grps.loc[c, cntry, :][cat_biggest_weight].mean(),
		        'TopsisBestCategory': toper(tempgrp.loc[cntry, :]['TopsisBestCategory'].mean())}
		small = grps.loc[c, cntry, :][dct[cat_biggest_weight]].mean()
		for key in small.keys():
			data[key] = small[key]
		totaldata.append(data)
	pd.DataFrame(totaldata).set_index('Country').sort_values(by=cat_biggest_weight +' (Weight: ' + str(weight_cat) + ')',ascending=False).round(3).to_excel(writer,sheet_name='Hotel Class (' + str(c) + ')')


writer.close()


#######################   Hotel Class   -     Country   ################################################################
wts = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Weights.xlsx',sheet_name='Country').set_index('Category')
# cat_biggest_weight = wts.loc['Greece'].sort_values(ascending=False).keys()[0]
# weight_cat = wts.loc['Greece'].sort_values(ascending=False)[0]
# cat_biggest_weight = 'Value'
# weight_cat = 0.264
cat_biggest_weight = 'Location'
weight_cat = 0.322

grps = totalInfo.groupby(by=['Country', 'Hotel_Class', 'Region', 'Name']).first().loc['Greece', :, :]

writer = pd.ExcelWriter('Presentation_Categorization_Greece('+cat_biggest_weight+').xlsx', engine='xlsxwriter')


for c in range(1,6):
	####################################################################################################################
	tempgrp = grps.loc[c,:]
	topsisweights = wts.loc['Greece']
	criterias = np.array([True, True, True, True, True, True])

	t = Topsis(tempgrp[['Facilities', 'Room', 'Location', 'Food', 'Value', 'Service']].values, topsisweights, criterias)

	t.calc()
	tempgrp['TopsisBestCategory'] = t.best_similarity
	####################################################################################################################

	totaldata = []
	for rgn in totalInfo.loc[totalInfo.Country == 'Greece'].Region.unique():

		data = {'Region': rgn, cat_biggest_weight +' (Weight: ' + str(weight_cat) + ')': grps.loc[c, rgn, :][cat_biggest_weight].mean(),
		        'TopsisBestCategory': toper(tempgrp.loc[rgn, :]['TopsisBestCategory'].mean())}
		small = grps.loc[c, rgn, :][dct[cat_biggest_weight]].mean()
		for key in small.keys():
			data[key] = small[key]
		totaldata.append(data)
	pd.DataFrame(totaldata).set_index('Region').sort_values(by=cat_biggest_weight +' (Weight: ' + str(weight_cat) + ')',ascending=False).round(3).to_excel(writer,sheet_name='Hotel Class (' + str(c) + ')')


writer.close()





