
### Entropy Weights ###############




#
# hn, nc = 1, 1
# # hn is the number of header rows, nc is the number of header columns

# import pandas as pd
#
# matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx'
#                        ,sheet_name='Sentiment')
# matrix.set_index('Hotel_Name',inplace=True)
#

# def entropy(data0):  # Return the	index	of	each	sample
# 	# Number of samples, number of indicators
# 	n, m = np.shape(data0)  # one	line	One	sample, one	column and one	indicator
# 	# Below is the normalized
# 	maxium = np.max(data0, axis=0)
# 	minium = np.min(data0, axis=0)
# 	data = (data0 - minium) * 1.0 / (maxium - minium)
# 	##Calculate the jth index, the proportion of the i-th sample in the index
# 	sumzb = np.sum(data, axis=0)
# 	data = data / sumzb
# 	# Processing ln0
# 	a = data * 1.0
# 	a[np.where(data == 0)] = 0.0001
# 	#
# 	# Calculate the entropy of each indicator
# 	e=(-1.0/np.log(n))*np.sum(data* np.log(a),axis=0)
# 	#
# 	# Calculate weight
# 	w=(1-e)/np.sum(1-e)
# 	recodes = np.sum(data * w, axis=1)
# 	return w
#
# weights = entropy(matrix.drop(columns='Rating').values)
#

###### TOSIS ###############



# from topsis import Topsis
import numpy as np
import pandas as pd

evaluation_matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')
evaluation_matrix.drop(columns=['Hotel','Ranking'],inplace=True)
evaluation_matrix = evaluation_matrix.values
# evaluation_matrix = np.array([
#     [1,2,3,4],
#     [4,3,2,1],
#     [3,3,3,3],
# ])




weights = [0.041, 0.276, 0.1438, 0.0647, 0.2550, 0.2194]

# import matplotlib.pyplot as plt
# a = pd.DataFrame(data={'Criteria': ['Υποδομές / Παροχές\nστο σύνολο των Πελατών', 'Δωμάτιο', 'Τοποθεσία', 'Φαγητό', 'Εξυπηρέτηση', 'Αξία'], 'Weights': [0.041,0.276,0.1438,0.0647,0.255,0.2194]}).set_index('Criteria').sort_values(by='Weights',ascending=False)
# weights = a.Weights.to_list()
# criteria = a.index.to_list()
# plt.rcParams['font.size'] = 20.0
# plt.title('Βάρη Κριτηρίων',  fontsize=40, fontweight='bold')
# plt.pie(weights, labels=criteria, autopct="%1.2f%%")


'''
if higher value is preferred - True
if lower value is preferred - False
'''
criterias = np.array([True, True, True, True, True,  True])

t = Topsis(evaluation_matrix, weights, criterias)

t.calc()

print("best_distance\t", t.best_distance)
print("worst_distance\t", t.worst_distance)

matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')
# matrix['TopsisBest'] = t.rank_to_best_similarity()
# matrix['TopsisWorst'] = t.rank_to_worst_similarity()

#
# matrix.groupby(by='Ranking').boxplot(column=['TopsisBest','TopsisWorst'])

matrix['TopsisBest'] = t.best_similarity
matrix['TopsisWorst'] = t.worst_similarity

dct = matrix.groupby(by='Ranking').Hotel.count().to_dict()
for key in dct.keys():
	dct[key] = str(key)+'\n('+str(dct[key])+')'
matrix.Ranking.replace(to_replace=dct,inplace=True)


matrix.rename(columns={'TopsisBest': 'Καλύτερη Λύση','TopsisWorst':'Χειρότερη Λύση','Ranking':'Κατάταξη'},inplace=True)

import matplotlib.pyplot as plt
fig, axes = plt.subplots(2)
counter = 0
for x in ['Καλύτερη Λύση','Χειρότερη Λύση']:
	ax = matrix.boxplot(column=x,by='Κατάταξη', ax=axes[counter])

	ax.set_xlabel('Κατάταξη\n(Πλήθος Ξενοδοχείων)')
	ax.set_ylabel('Ομοιότητα με\n'+x, fontsize=15,color='green')
	axes[counter].set_title('')

	counter += 1
fig.suptitle('BoxPlot Κατανομής Ομοιότητας με\nΚαλύτερη/Χειρότερη Λύση TOPSIS\nΞενοδοχείων Ανά Κατάταξη',fontsize=15,color='blue')
# print("weighted_normalized",t.weighted_normalized)

# print("worst_similarity\t", t.worst_similarity)
# print("rank_to_worst_similarity\t", t.rank_to_worst_similarity())

# print("best_similarity\t", t.best_similarity)
# print("rank_to_best_similarity\t", t.rank_to_best_similarity())


########## Analysis

# matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')
#
dct = {
		'Hotel': matrix.Hotel.values,
		'Ranking': matrix.Ranking.values,
		'RankingCont': matrix.Ranking,
		't2bd': t.best_similarity,
		't2br': t.rank_to_best_similarity(),
		't2wd': t.worst_similarity,
		't2wr': t.rank_to_worst_similarity()
}

tpsres = pd.DataFrame(dct)
#
# def norm(x,cat, inv=False):
# 	mn = tpsres[cat].min()
# 	mx = tpsres[cat].max()
# 	if inv == True: return (mx-x)/(mx-mn)
# 	return (x-mn)/(mx-mn)
#
# tpsres['Ranking'] = tpsres.Ranking.apply(lambda x: norm(x,'Ranking'))
# tpsres['t2bd'] = tpsres.t2bd.apply(lambda x: norm(x,'t2bd'))
# tpsres['t2wd'] = tpsres.t2wd.apply(lambda x: norm(x,'t2wd',inv=True))




arg = 'TopsisBest'
percentiles = [j/10 for j in range(1,10)]
description = {}
matrix.loc[matrix.Ranking == i][arg].describe(percentiles=percentiles)
rows = ['count','mean','std','10%','20%','30%','40%','50%','60%','70%','80%','90%']
for i in range(1,8):
	description[str(i)] = matrix.loc[matrix.Ranking == i][arg].describe(percentiles=percentiles)[rows].values

descriptions = pd.DataFrame(data=description,index=rows)



############# BoxPlots By Hotel Class - Country ##############################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sheet = 'Region'
weights = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Weights.xlsx',sheet_name=sheet)
weights.set_index('Category',inplace=True)
evaluation_matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')
# evaluation_matrix.drop(columns=['Hotel','Ranking'],inplace=True)
# evaluation_matrix = evaluation_matrix.values

# dct = {'Greece': 'Ελλάδα', 'Cyprus':'Κύπρος','Portugal':'Πορτογαλία','France':'Γαλλία','Spain':'Ισπανία', 'Italy': 'Ιταλία','Turkey': 'Τουρκία'}
dct = {'Heraklion': 'Ηράκλειο', 'Chania': 'Χανιά', 'Rhodes': 'Ρόδος', 'Zakynthos': 'Ζάκυνθος', 'Corfu': 'Κέρκυρα'}
criterias = np.array([True, True, True, True, True,  True])



complete_matrix = pd.read_excel(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Hotel_Criteria_Grade_Sentiment_Matrix.xlsx')


hotel_data = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')
hotel_data.drop_duplicates(subset=['Name'],keep='first',inplace=True)
hotel_data = hotel_data.loc[hotel_data.Country == 'Greece']
# hotel_data['Hotel_Class'] = hotel_data.Hotel_Class.apply(lambda x: int(x) if not pd.isna(x) else 1)

fig, axes = plt.subplots(len(weights.index))

counter = 0
for cat in weights.index:
	names = hotel_data.loc[hotel_data[sheet] == cat].Name.values
	matrix_sample = evaluation_matrix.loc[evaluation_matrix.Hotel.isin(names)].drop(columns=['Hotel','Ranking']).values
	Category_weights = weights.loc[cat].values
	t = Topsis(matrix_sample, Category_weights, criterias)

	t.calc()

	matrix = complete_matrix.loc[complete_matrix.Hotel.isin(names)]

	dctNum = matrix.groupby(by='Ranking').Hotel.count().to_dict()
	for key in dctNum.keys():
		dctNum[key] = str(key) + '\n(' + str(dctNum[key]) + ')'
	matrix.Ranking.replace(to_replace=dctNum, inplace=True)

	matrix['TopsisBest'] = t.best_similarity
	matrix.rename(columns={'TopsisBest': 'Ομοιότητα - Καλύτερη Εναλλακτική','Ranking':'Κατάταξη'},inplace=True)

	ax = matrix.boxplot(column='Ομοιότητα - Καλύτερη Εναλλακτική',by='Κατάταξη', ax=axes[counter])
	ax.set_xlabel('')
	# ax.set_ylabel('Κλάση\nΞενοδοχείων:\n'+str(cat), fontsize=15, color='green')
	ax.set_ylabel(dct[cat], fontsize=15,color='green')
	axes[counter].set_title('')
	counter += 1
fig.suptitle('')


############# BoxPlots By Hotel Class - Country ##############################
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

weights = pd.read_excel(r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\Results Analysis\TripType_MCDM\Weights.xlsx')
weights.set_index('Category',inplace=True)
dir = r'C:\Users\pasch\Documents\Python\Aspect-Sentiment-MCDM\Results Analysis\TripType_MCDM'
# files = os.listdir(dir)[:-1]
files = ['coupleMCDM.xlsx', 'familyMCDM.xlsx', 'friendsMCDM.xlsx', 'soloMCDM.xlsx', 'businessMCDM.xlsx']

criterias = np.array([True, True, True, True, True,  True])
dct = {'couple': 'Ως Ζεύγος', 'family': 'Οικογενεικώς', 'business': 'Επαγγελματικώς', 'friends': 'Με Φίλους', 'solo': 'Μόνος'}
fig, axes = plt.subplots(len(weights.index))
counter = 0
for f in files:
	tt = f.split('M')[0]
	w = weights.loc[tt].values
	evaluation_matrix = pd.read_excel(dir+'\\'+f)
	t = Topsis(evaluation_matrix.drop(columns=['Hotel','Ranking']).values, w, criterias)
	t.calc()
	evaluation_matrix['TopsisBest'] = t.best_similarity
	dctNum = evaluation_matrix.groupby(by='Ranking').Hotel.count().to_dict()
	for key in dctNum.keys():
		dctNum[key] = str(key) + '\n(' + str(dctNum[key]) + ')'
	evaluation_matrix.Ranking.replace(to_replace=dctNum, inplace=True)
	evaluation_matrix.rename(columns={'TopsisBest': 'Ομοιότητα - Καλύτερη Εναλλακτική', 'Ranking': 'Κατάταξη'}, inplace=True)
	ax = evaluation_matrix.boxplot(column='Ομοιότητα - Καλύτερη Εναλλακτική',by='Κατάταξη', ax=axes[counter])
	ax.set_xlabel('')
	ax.set_ylabel(dct[tt], fontsize=11, color='green')
	axes[counter].set_title('')
	counter += 1
fig.suptitle('')








