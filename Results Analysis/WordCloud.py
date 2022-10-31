import pickle
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag



en_stop = nltk.corpus.stopwords.words('english')
en_stop.extend(['from', 'subject', 're', 'edu', 'use'])
en_stop = set(en_stop)
stemmer = WordNetLemmatizer()

from nltk.corpus import wordnet
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def preprocess_text(document):
	#Remove all the special characters
	document = re.sub(r'\W',' ', str(document))

	#Remove all single characters
	document = re.sub(r'\s+[a-zA-Z]\s+', ' ',  document)

	#Remove single characters from the start
	document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

	#Subtituting multiple spaces with single space
	document = re.sub(r'\s+', ' ',document, flags = re.I)

	#Removing prefixed 'b'
	document = re.sub(r'^b\s+', '', document)

	#Converting to Lowercase
	document = document.lower()
	tokens = nltk.word_tokenize(document)
	tokens = nltk.pos_tag(tokens)
	newtokens = []
	for token in tokens:
		if get_wordnet_pos(token[1]) != '':
			newtokens.append(stemmer.lemmatize(token[0], get_wordnet_pos(token[1])))
		else:
			newtokens.append(stemmer.lemmatize(token[0]))
	tokens = [word for word in newtokens if word not in en_stop]
	tokens =  [word for word in tokens if len(word) > 2]

	#Lemmatization
	# tokens = document.split()
	# tokens = [stemmer.lemmatize(word) for word in tokens]
	# tokens = [word for word in tokens if word not in en_stop]
	# tokens =  [word for word in tokens if len(word) >= 3]

	return ' '.join(tokens)

l = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\selectedComments.p','rb'))
pr=[]
for i in range(len(l)):
	pr.append(preprocess_text(l[i]))

pr = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\processed.p','rb'))

reviews_df = pd.DataFrame(data={'com':pr})


def show_wordcloud(data, title=None):
    wordcloud = WordCloud(
            background_color='white',
            max_words=200,
            max_font_size=40,
            scale=3,
            random_state=42
    ).generate(str(data))

    fig = plt.figure(1, figsize=(10, 10))
    plt.axis('off')
    if title:
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()


# print wordcloud
show_wordcloud(reviews_df["com"])

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words='english', ngram_range = (1,1), max_df = .6, min_df = .01)
X = vectorizer.fit_transform(doc)
feature_names = vectorizer.get_feature_names()

dense = X.todense()
denselist = dense.tolist()
df = pd.DataFrame(denselist, columns=feature_names)

wordcloud = WordCloud().generate_from_frequencies(df.transpose())
plt.imshow(wordcloud)


import pickle

processed_data = pickle.load(open(r'C:\Users\pasch\Documents\NaturalLanguage\LDA\processed_data.p', "rb"))

for item in range(len(processed_data)):
    for word in processed_data[item]:
        if word in unwanted:
            processed_data[item].remove(word)


for item in range(len(processed_data)):
    reviews_df._set_value(index=item,col='Comment', value=' '.join(processed_data[item]))





from itertools import chain
from collections import Counter
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
processed_data = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\tokensNouns.p','rb'))

c = Counter(chain(*[x for x in processed_data]))
#
# import itertools
# lst = list(itertools.chain.from_iterable(processed_data))
# text = ' '.join(lst)



def show_wordcloud(dct, title=None):
    wordcloud = WordCloud(background_color='white',
            max_words=300,
            max_font_size=300,
            width=2000,height=2000,
            scale=3,
            random_state=42).generate_from_frequencies(frequencies=dct)

    fig = plt.figure(1, figsize=(10, 10))
    plt.axis('off')
    if title:
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()

# show_wordcloud(dct)

# print wordcloud
show_wordcloud(c)


