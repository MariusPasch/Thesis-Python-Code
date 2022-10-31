import pandas as pd


cdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\Semantria\Data&Matrices\SemantriaProcessedResults.csv')

from ast import literal_eval as eval
def literal_return(val):
	try:
		return eval(val)
	except (ValueError, SyntaxError) as e:
		return []


cdf.loc[:,['topics']] = cdf.topics.apply(literal_return)
cdf.loc[:,['themes']] = cdf.themes.apply(literal_return)
cdf.loc[:,['auto_categories']] = cdf.auto_categories.apply(literal_return)
#simple
def titles_count(cdf,column):
	countdict = {}
	for revcolumn in cdf[column]:
		if revcolumn:
			for dct in revcolumn:
				title = dct['title']
				if title not in countdict.keys():
					countdict[title] = 1
				else:
					countdict[title] += 1
	return {k: v for k, v in sorted(countdict.items(),reverse=True, key=lambda item: item[1])}

dct = titles_count(cdf,'topics')
topics = pd.DataFrame(data={'topic': dct.keys(),'times': dct.values()})


import pandas as pd
import pickle
cdf = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\OnyThemesSemantriaResults.p', 'rb'))


def total_titles(cdf):
	lst = []
	for theme in cdf.themes:
		for dct in theme:
			# if dct['title'] not in lst:
			lst.append(dct['title'])
	return lst

titles = total_titles(cdf)

import gensim

def sent_to_words(sentences):
	for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

words = list(sent_to_words(titles))

# bigram = gensim.models.Phrases(words, min_count=5, threshold=70) # higher threshold fewer phrases.threshold=100
# bigram_mod = gensim.models.phrases.Phraser(bigram)

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]
def make_trigram(texts):
    return [trigram_mod[doc] for doc in texts]
from nltk.stem import WordNetLemmatizer
from gensim.models import phrases
import nltk
stemmer = WordNetLemmatizer()
for i in range(len(words)):
	for j in range(len(words[i])):
		words[i][j] = stemmer.lemmatize(words[i][j])
bigram = gensim.models.Phrases(words,scoring='npmi', min_count=100, threshold=0.5, connector_words=phrases.ENGLISH_CONNECTOR_WORDS) #  higher threshold fewer phrases.threshold=100
bigram_mod = gensim.models.phrases.Phraser(bigram)

trigram = gensim.models.Phrases(bigram[words], threshold=100)
trigram_mod = gensim.models.phrases.Phraser(trigram)


texts = make_bigrams(words)
texts = make_trigram(texts)
# import random
#
# u = []
# for lst in texts:
# 	if 'seating' in lst: u.append(lst)
# 	# for word in lst:
# 	# 	if '_' in word:
# 	# 		u.append(word)
# random.shuffle(u)
# print(u[:100])
# print('words with _: ',len(u))
# print('total words: ',len(texts))
#

u = {}
for lst in texts:
	for word in lst:
		if word not in u.keys():
			u[word] = 1
		else:
			u[word] += 1
u = {k: v for k, v in sorted(u.items(),reverse=True, key=lambda item: item[1])}
import pandas as pd
udf = pd.DataFrame(data={'titles': u.keys(),'times': u.values()})
print(len(udf))

print(udf.loc[:250].times.sum())
print(udf.loc[:250])
######
count = 0
for index in cdf.index:
	themes = []
	for t in cdf.loc[index].themes:
		title = list(sent_to_words([t['title']]))[0]
		for i in range(len(title)):
			title[i] = stemmer.lemmatize(title[i])
		title = make_bigrams([title])[0]
		t['title'] = title
		themes.append(t)
	cdf.loc[index, 'themes'] = themes
	count += 1
	if count==100:
		break

def bigramm_themes(ldct):
	themes = []
	for d in ldct:
		title = list(sent_to_words([d['title']]))[0]
		for i in range(len(title)):
			title[i] = stemmer.lemmatize(title[i])
		title = make_bigrams([title])[0]
		d['title'] = title
		themes.append(d)
	return themes

cdf['BigrammProcessed'] = cdf.themes.apply(bigramm_themes)

import pickle
pickle.dump(cdf,open(r'NewOnlyThemesSemantriaBigrammed.p','wb'))
###




from nltk.stem import WordNetLemmatizer
import nltk
stemmer = WordNetLemmatizer()
#
def titles_count(cdf,column, pos=-1):
	countdict = {}
	strengthdict = {}
	for revcolumn in cdf[column]:
		if revcolumn:
			for dct in revcolumn:
				title = dct['title'].split()[pos]
				title = stemmer.lemmatize(title)
				if title not in countdict.keys():
					countdict[title] = 1
					strengthdict[title] = dct['strength_score']
				else:
					countdict[title] += 1
					strengthdict[title] += dct['strength_score']
	return [{k: v for k, v in sorted(countdict.items(),reverse=True, key=lambda item: item[1])}, strengthdict]

dcts = titles_count(cdf,'themes')
dct = dcts[0]
strengthdict = dcts[1]

for key in strengthdict.keys():
	strengthdict[key] = strengthdict[key]/dct[key]

lst = []
for key in dct.keys():
	lst.append(strengthdict[key])


themes = pd.DataFrame(data={'theme': dct.keys(),'times': dct.values(), 'strength_avg': lst})


# themes = pd.DataFrame(data={'theme':dct.keys(),'times':dct.values()})
from nltk.stem import WordNetLemmatizer
import nltk
stemmer = WordNetLemmatizer()
# def titles_count(cdf,column):
# 	countdict = {}
# 	for revcolumn in cdf[column]:
# 		for lst in revcolumn:
# 			title = lst['title'].lower()
# 			for word in nltk.pos_tag(nltk.word_tokenize(title)):
# 				# word = word.lower()
# 				if get_wordnet_pos(word[1]) == '':
# 					word = stemmer.lemmatize(word[0])
# 				else:
# 					word = stemmer.lemmatize(word[0], get_wordnet_pos(word[1]))
# 				if word not in countdict.keys():
# 					countdict[word] = 1
# 				else:
# 					countdict[word] += 1
# 	return {k: v for k, v in sorted(countdict.items(),reverse=True, key=lambda item: item[1])}
#
# dct = titles_count(cdf,'themes')
# themes = pd.DataFrame(data={'theme':dct.keys(),'times':dct.values()})
#
#
# count = 0
# nope = []
# yes = []
# for word in themes.theme:
# 	if word not in vocab:
# 		nope.append(word)
# 	else:
# 		yes.append(word)
# 		count += 1
#
# lst = []
# for word in yes:
# 	if lda_model[id2word.doc2bow([word])] != []:
# 		lst.append(lda_model[id2word.doc2bow([word])][0][0])
# 	else:
# 		lst.append(lda_model[id2word.doc2bow([word])])


new = pd.DataFrame(data={'Word': yes, 'LDA':lst})

# import pandas as pd
#
# data =  pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\test.csv')


def titles_count_strongest(cdf,column, pos=-1):
	countdict = {}
	for revcolumn in cdf[column]:
		temp = ['',0]
		for lst in revcolumn:
			if temp[1] < lst['strength_score']:
				temp[0] = lst['title']
				temp[1] = lst['strength_score']
		try:
			if temp[0].split()[pos] not in countdict.keys():
				countdict[temp[0].split()[pos]] = 1
			else:
				countdict[temp[0].split()[pos]] += 1
		except:
			if temp[0] not in countdict.keys():
				countdict[temp[0]] = 1
			else:
				countdict[temp[0]] += 1
	return {k: v for k, v in sorted(countdict.items(),reverse=True, key=lambda item: item[1])}


dct1 = titles_count_strongest(cdf,'themes',pos=-1)
themes1 = pd.DataFrame(data={'theme': dct1.keys(),'time': dct1.values()})
themes1