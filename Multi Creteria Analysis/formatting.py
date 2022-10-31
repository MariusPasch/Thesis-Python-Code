import pandas as pd

# grades = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')

##############################################
# hotel_data = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')

# ######## BY HOTEL Country #########
# sorted = hotel_data.groupby(by='Country').Name.unique()
# countries = hotel_data.Country.unique()
#
# for c in countries:
#
#     smpl = grades[grades.Hotel.isin(sorted[c])]
#     print(c, ' = ', len(smpl))

##### BY HOTEL CLASS #####
# hotel_data.drop_duplicates(subset=['Name'],keep='first',inplace=True)
# hotel_data = hotel_data[hotel_data.Name.isin(grades.Hotel.values)].sort_values(by='Name').reset_index()
#
# sorted = hotel_data.Hotel_Class.unique()
# sorted.sort()
# sorted = sorted.tolist()
# sorted = sorted[-1:] + sorted[:-1]

# for plc in range(1,len(sorted),2):
#
#     smpl = grades[hotel_data.Hotel_Class.isin(sorted[plc-1:plc+1])]
#     print(sorted[plc - 1:plc + 1], ' = ', len(smpl))


# ######## BY HOTEL Country #########
#
# sorted = hotel_data.loc[hotel_data.Country == 'Greece'].groupby(by='Region').Name.unique()
# regions = hotel_data.loc[hotel_data.Country == 'Greece'].Region.unique()
#
# for c in regions:
#     smpl = grades[grades.Hotel.isin(sorted[c])]
#     print(c, ' = ', len(smpl))


##### BY TRIP TYPE #####
import os
dir = r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\Results Analysis\TripType_MCDM'
files = os.listdir(dir)


for f in files:
    grades = pd.read_excel(dir + '\\' + f)



################


    # head = smpl

    head = grades

    # head = head.sort_values(by='Ranking', ascending=False)

    string = 'Alt/cri'

    for key in head.keys()[1:]:
        string += '\t'+key
    string += '\n'

    for values in head.values:

        for value in values:
            string +=  str(value) + '\t'

        string = string.strip('\t')
        string += '\n'

    # string = string.strip('\n')
    # fstr = r'testHotels10s' + str(sorted[plc-1:plc+1]) + 'Stars.txt'
    fstr = r'testHotels10s' +f.split('M')[0] + '.txt'
    # fstr = r'testHotelsTotal.txt'
    with open(fstr,'w', encoding='utf-8') as file:
        file.write(string)

#################################################
times = 0

for times in range(10):

    smpl = grades.sample(frac=0.1)


    head = smpl

    # head = grades

    # head = head.sort_values(by='Ranking', ascending=False)

    string = 'Alt/cri'

    for key in head.keys()[1:]:
        string += '\t'+key
    string += '\n'

    for values in head.values:

        for value in values:
            string +=  str(value) + '\t'

        string = string.strip('\t')
        string += '\n'

    # string = string.strip('\n')
    fstr = r'testHotels10s' + str(times+1) + '.txt'
    # fstr = r'testHotelsTotal.txt'
    with open(fstr,'w', encoding='utf-8') as file:
        file.write(string)



metastring = 'Cri/attributes'

for word in ['Monocity', 'Type','Worst','Best','a']:
    metastring += '\t' + word
metastring += '\n'

for key in head.keys()[1:-1]:
    metastring += key
    # for v in [0, 0, 0, 1, 20]:
    # Cut: 1 , Continuous: 0
    for v in [0, 0, 0, 1, 10]:
        metastring += '\t' + str(v)
    metastring += '\n'
# metastring.strip('\n')

with open('metatestHotels10.txt','w', encoding='utf-8') as file:
    file.write(metastring)

