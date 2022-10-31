import numpy as np
import pandas as pd


# evaluation_matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')
# evaluation_matrix.drop(columns=['Hotel','Ranking'],inplace=True)
# evaluation_matrix = evaluation_matrix.values
#
# totalweights = [0.041, 0.276, 0.1438, 0.0647, 0.2550, 0.2194]
# criterias = np.array([True, True, True, True, True,  True])
#
#
# t = Topsis(evaluation_matrix, totalweights, criterias)
#
# t.calc()


totalInfo = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Total_Info_MCM.xlsx')

# totalInfo['TopsisBest'] = t.best_similarity
#
# totalInfo = totalInfo.sort_values(by='TopsisBest',ascending=False).reset_index()
# totalInfo['Restaurants'] = totalInfo['Location_Restaurants'].astype('str') + ' ' + totalInfo['Location_Restaurants_Distance']
# totalInfo['Attractions'] = totalInfo['Location_Attractions'].astype('str') + ' ' + totalInfo['Location_Attractions_Distance']
# totalInfo['Amenities'] = totalInfo.Amenities.apply(eval)
# totalInfo['Amenities'] = totalInfo.Amenities.apply(lambda x: ', '.join(x))
# totalInfo['Room_features'] = totalInfo.Room_features.apply(eval)
# totalInfo['Room_features'] = totalInfo.Room_features.apply(lambda x: ', '.join(x))
# totalInfo['Room_Types'] = totalInfo.Room_Types.apply(eval)
# totalInfo['Room_Types'] = totalInfo.Room_Types.apply(lambda x: ', '.join(x))
# totalInfo.drop(columns=['Location_Restaurants','Location_Restaurants_Distance','Location_Attractions','Location_Attractions_Distance'],inplace=True)

info = ['TopsisBest', 'Name', 'Country', 'Region','Price', 'Hotel_Class', 'Reviews', 'Stars', 'Amenities', 'Room_features', 'Room_Types',
        'Location_Walkability','Restaurants', 'Attractions']

scores = ['Swim_Rating', 'Internet_Rating', 'Spa_Rating', 'Sports_Rating', 'Family_Rating', 'BarEntertainment_Rating',
          'Room_Grade',
          'Transportation_Rating','Location_Attraction_Grade', 'Location_Restaurants_Grade', 'Location_Walkability_Grade',
          'Food_Rating',
          'Services_Rating', 'CleanService_Rating',
          'Price_Grade', 'Revs_First_Impression']

sentiment = ['Stars_Location', 'Stars_Cleanliness', 'Stars_Service', 'Stars_value',
        'Stars_Room', 'Stars_Sleep', 'Service_Sentiment',
       'Facilities_Sentiment', 'Room_Sentiment', 'Location_Sentiment',
       'Food_Sentiment', 'Value_Sentiment']


writer = pd.ExcelWriter('Hotel_Info_Presentation2.xlsx', engine='xlsxwriter')

totalInfo.head(10)[info+scores+sentiment].to_excel(writer,sheet_name='')

for clss in [[1.0,np.nan],[1.5,2.0],[2.5,3.0],[3.5,4.0],[4.5,5.0]]:
	totalInfo.loc[totalInfo.Hotel_Class.isin(clss)].head(5)[info+scores+sentiment].to_excel(writer,sheet_name='HC_'+str(clss[0])+'_'+str(clss[1]))

for cntr in totalInfo.Country.unique():
	totalInfo.loc[totalInfo.Country == cntr].head(5)[info+scores+sentiment].to_excel(writer,sheet_name=cntr)

for rgn in totalInfo.loc[totalInfo.Country == 'Greece'].Region.unique():
	totalInfo.loc[totalInfo.Country == 'Greece'].loc[totalInfo.loc[totalInfo.Country == 'Greece'].Region == rgn].head(5)[info+scores+sentiment].to_excel(writer,sheet_name=rgn)


writer.close()
