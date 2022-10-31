# import pandas as pd
#
# rdf = pd.read_csv(r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdReviews.csv')
#
# rdf.drop(['Reviewer_Number_of_Reviews','Reviewer_Username', 'Reviewer_Link', 'Reviewer_Country', 'Rating', 'Date_of_stay',
#                         'Date_of_review', 'Title', 'Comment', 'Comment_Word_Count',
#                         'Helpful_Votes', 'Contribution_Votes', 'Trip_Type', 'Value_Stars',
#                         'Rooms_Stars', 'Service_Stars', 'Cleanliness_Stars', 'Location_Stars',
#                         'Sleep_Quality_Stars', 'Hotel_Name', 'Hotel_Link', 'Hotel_Reviews',
#                         'Hotel_Country', 'Hotel_Region', 'Comment_Memory_Size'],axis=1,inplace=True)
#
# dct = rdf.groupby(by='Reviewer_ID').count().to_dict()
#
# rdf = pd.read_csv(r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdReviews.csv')
#
# rdf['Reviewer_Number_of_Reviews'] = rdf.Reviewer_ID.map(dct['Row'])


# hlpfl = rdf.loc[rdf.Helpful_Votes >= 10]


# again = rdf.loc[rdf.Reviewer_Number_of_Reviews >= 2][['Reviewer_ID', 'Hotel_Country', 'Hotel_Region']]
# countries = again.Hotel_Country.unique()
# regions = again.Hotel_Region.unique()
# cdct = {}
# for c in countries:
#     cdct[c] = again.loc[again.Hotel_Country == c]['Reviewer_ID'].to_list()
#
# for c in countries:
#     for c2 in countries:
#         print(c, c2, len(list(set(cdct[c]).intersection(cdct[c2]))))
#
# # clst.append((c, c2, len(list(set(cdct[c]).intersection(cdct[c2])))))
# rdct = {}
# for r in regions:
#     rdct[r] = again.loc[again.Hotel_Region == r]['Reviewer_ID'].to_list()
#
# rlst = []
# for r in regions:
#     for r2 in regions:
#         print(r, r2, len(list(set(rdct[r]).intersection(rdct[r2]))))
#         rlst.append((r, r2, len(list(set(rdct[r]).intersection(rdct[r2])))))
#
# rlst.sort(key=lambda x: x[2],reverse=True)
#
# rlst



import pickle
import pandas as pd

rdf = pd.read_csv(r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdReviews.csv')


sem = pickle.load(open(r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\Semantria\Data&Matrices\aspectsAllocated2Reviews.p','rb'))

# rdf.drop(['Reviewer_ID', 'Reviewer_Username', 'Reviewer_Number_of_Reviews',
#        'Reviewer_Link', 'Reviewer_Country', 'Rating', 'Date_of_stay',
#        'Date_of_review', 'Title', 'Comment', 'Comment_Word_Count','Contribution_Votes', 'Trip_Type', 'Value_Stars',
#        'Rooms_Stars', 'Service_Stars', 'Cleanliness_Stars', 'Location_Stars',
#        'Sleep_Quality_Stars', 'Hotel_Link', 'Hotel_Reviews',
#        'Hotel_Country', 'Hotel_Region', 'Comment_Memory_Size'],axis=1,inplace=True)
#
# hot = rdf.Hotel_Name.unique()
# med = rdf.groupby(by='Hotel_Name').Helpful_Votes.median().to_dict()
# rows = []
# for h in hot:
#     rows += rdf.loc[(rdf.Hotel_Name == h) & (rdf.Helpful_Votes >= med[h])].Row.to_list()
#
# sem.loc[sem.Row.isin(rows)].BigrammProcessed.apply(lambda x: [z for y in x for z in y['title']])





import pandas as pd

rdf = pd.read_csv(r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\Cropped_95-5-2048\crpdReviews.csv')

rdf.drop(['Reviewer_Username', 'Reviewer_Number_of_Reviews',
       'Reviewer_Link','Date_of_stay',
       'Date_of_review', 'Title', 'Comment', 'Comment_Word_Count',
       'Helpful_Votes', 'Contribution_Votes','Hotel_Link', 'Hotel_Reviews',  'Comment_Memory_Size'],axis=1,inplace=True)

# rdf.drop(['Reviewer_Country', 'Row', 'Reviewer_ID', 'Hotel_Name', 'Hotel_Country',
#        'Hotel_Region'],axis=1,inplace=True)

rdf['Trip_Type'] = rdf.Trip_Type.apply(lambda x: x if (pd.isna(x)) else x.split(' ')[-1])


# grp = rdf.groupby(by='Trip_Type').mean()
#
#
# grp.loc['Total'] =rdf.mean(numeric_only=True).values
#

tt = rdf.Trip_Type.unique()

def ranking(stars):
	try:
		return 11 - int(stars * 2)
	except:
		return 10


for t in tt[1:]:
    name = r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\Results Analysis\Trip_Type_MCDM'+ t +'MCDM.xlsx'
    writer = pd.ExcelWriter(name, engine='xlsxwriter')
    grades = pd.read_excel(
        r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\MCDM Creation\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')
    grades.drop(['Ranking'], axis=1, inplace=True)
    dct = rdf.loc[rdf.Trip_Type == t].groupby(by='Hotel_Name').Rating.mean().apply(ranking).to_dict()
    grades = grades.loc[grades.Hotel.isin(dct.keys())]
    r = [dct[h] for h in grades.Hotel]
    grades['Ranking'] = r
    grades.to_excel(writer,sheet_name='Grades',index=False)
    writer.close()













