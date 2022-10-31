import pandas as pd
import numpy as np
# df = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Reviews-Aspect-Sentiment-PlusAllValues.csv')

pl = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\MultiDimensionalMatrix.csv')

hot = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')

hotels = pl.Hotel.values

price = []
for h in hotels:
	price.append(hot.loc[hot.Name == h]['Price'].values[0])


selected = hot.loc[hot.Name.isin(hotels)]
uniques = {}
for key in ['Amenities', 'Room_features', 'Room_Types']:

	selected[key] = selected[key].apply(eval).values
	uniques[key] = []
	for i in selected[key].values:
		for d in i:
			if d not in uniques[key]:
				uniques[key].append(d)

def removeblank(list):
	while '' in list:
		list.remove('')
	return list

for key in uniques.keys():
	uniques[key] = removeblank(uniques[key])

for key in uniques.keys():
	selected[key] = selected[key].apply(lambda x: removeblank(x))



def types2bool(list,key):
	boolean = []
	for i in range(len(uniques[key])):
		if uniques[key][i] in list:
			boolean.append(1)
		else:
			boolean.append(0)
	return boolean

for key in uniques.keys():
	for idx in selected.index:
		selected[key][idx] = types2bool(selected[key][idx],key)

data = {}
for key in uniques.keys():
	# data[key] = {}
	for i in range(len(uniques[key])):
		type = uniques[key][i]
		data[key+type] = []
		for idx in selected.index:
			data[key+type].append(selected[key][idx][i])




X = pd.DataFrame(data=data).values

y = np.array(selected.Hotel_Class.fillna(value=0.5).apply(lambda x: int((x*2)-1)).values)


from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

clf = LinearDiscriminantAnalysis(solver='eigen',shrinkage='auto',store_covariance=True)

clf.fit(X, y)


from sklearn.decomposition import PCA
val = []
for n in range(31,70):

	clf = PCA(n_components=20,svd_solver='auto')
	clf.fit(X)
	newX = clf.transform(X)
	reverse = clf.inverse_transform(newX)
	result = False
	for v in range(5,12):
		v = v/10
		if np.all(reverse[X == 1] >= v) == True & np.all(reverse[X == 0] < v) == True:
			value = (n,v)
			result = True

	if  result == False:
		val.append((n,result))
	else:
		val.append(value)

print(val)


##########Entropy


def entropy(data0):
         # Return index each sample
         # Of samples, the number of indicators
    n,m=np.shape(data0)
         # Row of a sample, a one indicator
         # The following is normalized
    maxium=np.max(data0,axis=0)
    minium=np.min(data0,axis=0)
    data= (data0-minium)*1.0/(maxium-minium)
         # Item ## calculates indexes j, i-th sample index representing the proportion
    sumzb=np.sum(data,axis=0)
    data=data/sumzb
         # Of ln0 processing
    a=data*1.0
    a[np.where(data==0)]=0.0001
 # # Entropy is calculated for each indicator
    e=(-1.0/np.log(n))*np.sum(data*np.log(a),axis=0)
 # # Calculate the weight
    w=(1-e)/np.sum(1-e)
    recodes=np.sum(data*w,axis=1)
    return recodes