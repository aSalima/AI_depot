import mysql.connector
import nltk
import pyodbc
import csv
import re
import string
import gensim
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import statistics
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib import pyplot
from gensim.corpora import Dictionary
#import scikit-learn
#import bs4 beautifulsoup4 pour les pages web
#nltk.download('stopwords')
#nltk.download()
#import nltk.data
from mysql.connector import Error
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from statistics import mean
from nltk.stem.snowball import FrenchStemmer
from gensim import similarities
from gensim.models import TfidfModel
import constantes as cs
import clean_mantis as cl
import extractData as ed

# Récuperation des données MySql #

query = 'SELECT id, summary FROM mantis_local.mantis_bug_table limit 6;'
lines = ed.connMySql(cs.serverMySql, cs.databaseMySql, cs.usernameMySql, cs.passwordMySql, query)
print('lines', lines)
file = 'w2v.csv'
corpus = []
for line in lines:
    corpus.append(str(line[1]))
print('corpus', corpus)

ed.mySqlToCsv(lines, file)  # MySql --> CSV #
cl.clean_file(file)         # Traitement des données récuperées #

corpus2 = ['Paramétrage réglementaire : cadre emploi', 'Paramétrage réglementaire : cadre emploi', 'homme']
print('corpus', corpus)

model = gensim.models.Word2Vec(corpus2, min_count=1, size=5, window=5)

def document_vector(word2vec_model, doc):
    # remove out-of-vocabulary words
    doc = [word for word in doc if word in word2vec_model.wv.vocab]
    print('moyenne', np.mean(word2vec_model[doc], axis=0))
    return np.mean(word2vec_model[doc], axis=0)

for doc in corpus:
    document_vector(model, doc)
    print('doc vec', document_vector(model, doc))



'''
    sims = cosine_similarity(np.array([document_vector(model, doc) for doc in corpus]))
    print('sims',sims)


        # vectors
        a = np.array([1, 2, 1, 2, 2])
        b = np.array([1, 1, 4, 1, 3])
        c = np.array([1, 1, 4, 2, 1])

        print('a',a)
        print('b',b)
        print('c',c)

        # manually compute cosine similarity
        dot = np.dot(a, b)
        print('dot', dot)
        norma = np.linalg.norm(a)
        print('norma', norma)
        normb = np.linalg.norm(b)
        print('normb', normb)
        cos = dot / (norma * normb)

        print('cos',cos)

        # use library, operates on sets of vectors
        aa = a.reshape(1, 5)
        print('aa',aa)

        ba = b.reshape(1, 5)
        print('ba',ba)

        ca = c.reshape(1, 5)
        print('ca', ca)

        cos_lib = cosine_similarity(aa, ba, ca)
        print('cos_lib', cos_lib)

        print(
            dot,
            norma,
            normb,
            cos,
            cos_lib[0][1]
        )
'''
        
print('##############################################################')
'''
        for doc in corpus:
            vecs = []
            for word in doc:
                print(word, model.wv[word])
                vecs.append(model.wv[word])
            print('vecs', vecs)
            print('##################')

            colV = len(vecs[0])
            print('colV', colV)
            ligneV = len(vecs)
            print('ligneV', ligneV)
            for i in range(len(vecs)):
                for j in range(len(vecs[i])):
                    print(vecs[i][j], end=' ')
                print()

            sum = np.zeros(colV)

            for j in range(len(vecs[i])):
                for i in range(len(vecs)):
                    sum[j] = sum[j] + vecs[i][j]
                #print(sum[j])
            
            #print('sum', sum)
            moyenne = []
            for sum in sum:
                moy = sum / ligneV
                moyenne.append(moy)
            print('moyenne', moyenne)

            # moy = mean(vecs)



        
        X = model[model.wv.vocab]

       
        pca = PCA(n_components=2)

        result = pca.fit_transform(X)
        # create a scatter plot of the projection
        pyplot.scatter(result[:, 0], result[:, 1])

        words = list(model.wv.vocab)
        for i, word in enumerate(words):
            pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
        pyplot.show()
'''

