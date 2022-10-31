import pickle
import gensim
# import pandas as pd
import random
import re
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
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

	return tokens

import pandas as pd

rdf = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\crpdReviews.csv')
columns = rdf.columns
columns = columns.drop(['Row','Comment'])
rdf = rdf.drop(columns=columns)
rdf['tokens'] = rdf.Comment.apply(preprocess_text)

data_lemmatized = rdf['tokens'].to_list()


# pickle.dump(data_lemmatized, open("processed_data_lemmatized_bi_trigrams_ONLYNOUNS.p", "wb"))


# random.shuffle(data_lemmatized)

from gensim import corpora
# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)
# unwanted = ['olu_deniz','love','heraklion','lindo','bordeaux','turkey','turkish','marmaris','lato','corfu','cyprus','majorca','greece','greek','pm','madeira','bodrum','chania','year','week','day','return','thank','george','holiday','com']

bad_ids = []
for word in unwanted:
	bad_ids.append(id2word.token2id[word])
id2word.filter_tokens(bad_ids=bad_ids)

id2word.filter_extremes(no_below=10)
len(id2word)
# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

import pandas as pd
data = pd.read_csv(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\test.csv')

import pickle
id2word = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Final Model\id2wordFinal.p','rb'))
corpus = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Final Model\corpusFinal.p','rb'))
data_lemmatized = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Final Model\revsFinal.p','rb'))
lda_model = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\18Modified\LdaModel18Modified(Coherence0.432).p','rb'))
coherence_scores = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Final Model\CoherenceScores.p','rb'))
model_list = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Final Model\LdaModelList.p','rb'))
# rdf = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Final Model\tokensdf.p','rb'))
# data_lemmatized = rdf.tokens_bi.tolist()
# Build LDA model alpha='auto'
import gensim
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=18,
                                           alpha='symmetric',
                                           iterations=135,
                                           eta='auto',
                                           minimum_probability=0.1,
                                           # per_word_topics=True,
                                           # minimum_phi_value=0.05
                                           )

topics = lda_model.print_topics(num_words=50)
countertopics = 1
for topic in topics:
	print('\tTopic ',countertopics,'\n')
	countertopics += 1
	words = ''
	count = 0
	for w in range(len(topic[1].split('"'))):
	    if count == 1:
	        words += topic[1].split('"')[w] + ', '
	        count = 0
	    else:
	        count += 1
	print(words,'\n')
	# print('\n', topic)

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

# pyLDAvis.enable_notebook()
lda_vis = gensimvis.prepare(lda_model, corpus, id2word, sort_topics=False)
pyLDAvis.save_html(lda_vis,r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Final Model\LdaModelTopicsNew.html')

from gensim.models.coherencemodel import CoherenceModel
import warnings
warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity
coherencemodel = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherencescore = coherencemodel.get_coherence()
print(coherencescore)

pickle.dump(lda_model,open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\18Modified\LdaModel18Modified(Coherence0.432).p','wb'))

# pickle.dump(corpus, open('corpus_ldamodel8topicsNouns.pkl', 'wb'))
# id2word.save('id2word_ldamodel8topicsNouns.gensim')
# lda_model.save('ldamodel8topicsNouns.gensim')

# id2word = gensim.corpora.Dictionary.load(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Model8\id2word_ldamodel8topicsNouns.gensim')
# corpus = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Model8\corpus_ldamodel8topicsNouns.pkl', 'rb'))
# lda_model = gensim.models.ldamodel.LdaModel.load(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\Model8\ldamodel8topicsNouns.gensim')




processed_data_file = r'C:\Users\pasch\Documents\NaturalLanguage\processed_data_spellcorrected_ratings.csv'
reviews_df = pd.read_csv(processed_data_file)



from gensim.models.coherencemodel import CoherenceModel
import warnings
warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity
import gensim

from gensim.models.ldamodel import LdaModel
def compute_coherence_values(id2word, corpus, data_lemmatized, limit, start=2, step=3):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        # model=LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
        model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=num_topics
                                                # alpha='auto',
                                                # iterations=135,
                                                # eta='auto',
                                                # minimum_probability=0.1,
                                                # per_word_topics=True,
                                                # minimum_phi_value=0.05
                                                )
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
        print('num_topics = ',num_topics)
    return model_list, coherence_values

model_list, coherence_values = compute_coherence_values(id2word=id2word, corpus=corpus, data_lemmatized=data_lemmatized, start=3, limit=35, step=1)
# Show graph
import matplotlib.pyplot as plt
limit=35; start=3; step=1;
x = range(start, limit, step)
plt.plot(x, coherence_values)
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')
plt.show()





import pickle
corpus = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\18Modified\corpusFinal.p','rb'))
id2word = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\18Modified\id2wordFinal.p','rb'))
lda_model = pickle.load(open(r'C:\Users\pasch\Documents\Aspect-Sentiment-MCDM\LDA\18Modified\LdaModel18Modified(Coherence0.432).p','rb'))

vocab = id2word.token2id.keys()
