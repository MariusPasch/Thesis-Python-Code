import pickle
import gensim
import pandas as pd
import random
from gensim.models import KeyedVectors
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

df = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Reviews-Aspect-Sentiment-PlusAllValues.csv')

# processed_data_file = r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\processed_data_spellcorrected_ratings.csv'
# df = pd.read_csv(processed_data_file)
# Aspect Allocation

id2word = gensim.corpora.Dictionary.load(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Model8\id2word_ldamodel8topicsNouns.gensim')
# corpus = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Model8\corpus_ldamodel8topicsNouns.pkl', 'rb'))
lda_model = gensim.models.ldamodel.LdaModel.load(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Model8\ldamodel8topicsNouns.gensim')

revs = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\processed_data_lemmatized_bi_trigrams_ONLYNOUNS.p','rb'))

corpus=[id2word.doc2bow(rev) for rev in revs]

glove_vectors_file = r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\gensim_glove_vectors.txt'
glove_model = KeyedVectors.load_word2vec_format(glove_vectors_file, binary=False)

vocab = glove_model.key_to_index.keys()
def invocab(words):
    words = [word for word in words if word in vocab]
    return words



# def ldatopics(index):
# 	# print(revs[index],'\n')
# 	topics = lda_model[corpus[index]]
# 	topics.sort(key=lambda x: x[1], reverse=True)
# 	temp = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
# 	for topic in topics:
# 		temp[str(topic[0]+1)] = topic[1]
# 	topics = temp
# 	return topics
#
# def aspectlda(topics):
# 	sortedtopics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
# 	aspectgroups = {'Room': ['8'],
# 	                'Food': ['6', '3', '4'],
# 	                'Location-Facilities': ['7', '4', '3'],
# 					'Family-Entertainment': ['2', '3', '5'],
# 					'Service-Hospitality-Reservation': ['1', '3', '5']
# 					}
# 	candidates = []
# 	for key in aspectgroups.keys():
# 		tot = 0
# 		for topicnum in aspectgroups[key]:
# 			tot += topics[topicnum]
# 		if tot>=0.5: candidates.append(key)
# 	if len(candidates) == 1: return candidates[0]
# 	if '3' == sortedtopics[0][0] and '4' == sortedtopics[1][0] and topics['6'] != 0: return 'Food'
# 	if '3' == sortedtopics[0][0] and '4' != sortedtopics[1][0] and '5' != sortedtopics[1][0]:
# 		for key in aspectgroups.keys():
# 			if sortedtopics[1][0] in aspectgroups[key]:
# 				return key
# 	if topics['1'] + topics['5'] > 0.5: return 'Service-Hospitality-Reservation'
# 	if sortedtopics[0][0] in ['8', '6']: return [k for k,v in aspectgroups.items() if sortedtopics[0][0] in v][0]
#
# 	#speculations
# 	if topics['6'] >= 0.2: return 'Food'
# 	if topics['8'] >= 0.25: return 'Room'
#
#
#
# 	return 'Go to Glove'





room = ['room', 'apartment', 'bathroom', 'bed', 'balcony', 'tv', 'kitchen', 'shower', 'clean', 'fridge', 'towel', 'channel', 'floor', 'sleep', 'airconditioning']
location = ['location', 'view', 'town', 'road', 'car', 'bus', 'airport', 'port', 'beach', 'trip', 'distance', 'sea', 'area', 'walk', 'mountain']
service = ['service', 'reception', 'hospitality', 'experience', 'customer', 'manager', 'guest', 'owner', 'friend', 'english', 'welcome', 'birthday', 'waiter', 'care', 'help']

food = ['food', 'restaurant', 'breakfast', 'drink', 'meal', 'table', 'menu', 'buffet', 'dish', 'lunch', 'coffee', 'wine', 'order', 'dessert', 'glass']
facilities = ['facility', 'pool', 'spa', 'gym', 'garden', 'restaurant', 'terrace', 'sauna', 'bar', 'massage', 'building', 'bay', 'beach', 'court', 'sport']
entertainment = ['entertainment', 'drink', 'bar', 'music', 'shop', 'night', 'club', 'cocktail', 'activity', 'family', 'child', 'sport', 'dance', 'animation', 'play']

attrbts = {'food': food,
           'room': room,
        'facilities': facilities,
        'location': location,
        'entertainment': entertainment,
        'service': service,
}

def glove_sim(rev, attrbts):
	attr_similarity = {}
	if len(invocab(rev)) == 0:
		for key in attrbts.keys():
			attr_similarity[key] = 0
		return attr_similarity
	for i in range(len(rev)):
		if rev[i] == 'air_condition':
			rev[i] = 'airconditioning'
		else:
			rev[i].replace('_','-')

	glove_means = {'food': 0.665277,
                    'room': 0.681106,
                    'facilities': 0.741241,
                    'location': 0.747475,
                    'entertainment' : 0.763170,
                    'service': 0.778420
					}
	glove_std = {'food': 0.073644,
                'room': 0.075319,
                'facilities': 0.062257,
                'location': 0.062753,
                'entertainment' : 0.053807,
                'service': 0.051138
				}

	for attr in attrbts.keys():
	    # print(glove_model.n_similarity(invocab(rev),attrbts[attr]), attr)
	    attr_similarity[attr] = (glove_model.n_similarity(invocab(rev),attrbts[attr]) - glove_means[attr])/glove_std[attr]
	return attr_similarity

def glove_aspect(attr_similarity):
	glovetoaspect = {'food': 'Food',
                    'room': 'Room',
                    'facilities': 'Facilities',
                    'location': 'Location',
                    'entertainment': 'Entertainment',
                    'service': 'Service',
					}
	aspect = glovetoaspect[sorted(attr_similarity.items(), key=lambda x: x[1], reverse=True)[0][0]]
	return aspect




# ldagroups= {'1': [], '2': [], '3': [], '4': [], '5': [], '6': [], '7': [], '8': []}

glovegroups = {'food': [],
                'room': [],
                'facilities': [],
                'location': [],
                'entertainment': [],
                'service': []
				}

#
# Aspect_LDA = []
Aspect_Glove = []


for index in range(len(revs)):
	# topics = ldatopics(index)
	# for key in ldagroups.keys():
	# 	ldagroups[key].append(topics[key])
	# lda_asp = aspectlda(topics)
	attributes = glove_sim(revs[index],attrbts)
	for key in glovegroups.keys():
		glovegroups[key].append(attributes[key])
	glv_asp = glove_aspect(attributes)

	# Aspect_LDA.append(lda_asp)
	Aspect_Glove.append(glv_asp)



# Sentiment
txtblb =  df.TextBlob
vader = df.compound
sentiment=txtblb+vader
import numpy as np
m=sentiment.mean()
s=sentiment.std()
sentiment=sentiment.apply(lambda x: (x-m)/s)
sentiment = pd.cut(sentiment,bins=5,labels=np.array([1,2,3,4,5]))

sentiment = sentiment.values
sentiment = pd.Categorical(sentiment).to_list()




# CSV Data Creation

newdf = df.drop(columns=['LDA', 'GloVe', 'Sentiment', 'LDA 1', 'LDA 2', 'LDA 3', 'LDA 4', 'LDA 5', 'LDA 6',
       'LDA 7', 'LDA 8', 'GloVe food', 'GloVe room', 'GloVe facilities',
       'GloVe location', 'GloVe family', 'GloVe entertainment',
       'GloVe service', 'GloVe reservation', 'Sentiment Score'])
newdf['Aspect_GloVe'] = Aspect_Glove
newdf['Sentiment_Score'] = sentiment




for key in glovegroups.keys():
	newdf['GloVe '+key] = glovegroups[key]

newdf.to_csv('NewReviews-Aspect-Sentiment-PlusAllValues.csv',index=False)

sample = newdf.sample(frac=0.01)
sample.to_csv('sample.csv')


# Multicriteria Matrix Creation

import pandas as pd
df = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Reviews-Aspect-Sentiment-PlusAllValues.csv')




newdf = df.drop(columns=df.keys().drop(['Comment', 'Region', 'Hotel','Rating', 'Value Stars',
       'Rooms Stars', 'Service Stars', 'Cleanliness Stars', 'Location Stars','Sleep Quality Stars','Sentiment_Score','Aspect_GloVe']))
df=newdf
unique = list(df.Aspect_GloVe.unique())
aspects ={}
for key in unique:
	aspects[key] = []


for index in df.index:
	for key in unique:
		if key != df.Aspect_GloVe[index]:
			aspects[key].append(np.nan)
		else:
			aspects[key].append(df.Sentiment_Score[index])





x=df.loc[df['Service Stars'].notna().values]['Service Stars']




for index in x.index:
	aspects['Service'][index] = x[index]


aspects['Sleep_Quality'] = df['Sleep Quality Stars'].values

aspects['Hotel'] = df['Hotel'].values
aspects['Region'] = df['Region'].values
aspects['Rating'] = df['Rating'].values

# pd.DataFrame(data=aspects).to_csv('Polykritirios.csv',index=False)
pl = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Polykritirios.csv')

pl['Country'] = pl.Region.apply(lambda x: x.split(',')[-1].strip(' '))
pl['Region'] = pl.Region.apply(lambda x: x.split(',')[0].strip(' '))
complete = pl.groupby(by=['Country','Region','Hotel']).mean().dropna()

hot = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Data\Hotels.csv')

stars = []
for hotel in complete.index:
	stars.append(hot.loc[hotel[2]]['Stars'])


complete['Stars'] = stars

complete.to_csv('MultiDimensionalMatrix.csv')