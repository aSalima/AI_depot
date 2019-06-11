import mysql.connector
import nltk
import pyodbc
import csv
import re
import string
import gensim
import numpy as np
import os
import statistics
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib import pyplot
from gensim.corpora import Dictionary
from mysql.connector import Error
from nltk.corpus import stopwords
from statistics import mean
from nltk.stem.snowball import FrenchStemmer
from gensim import similarities
from gensim.models import Word2Vec
import constantes as cs
import clean_mantis as cl
import extractData as ed

###################################################################
################### DEFINITION DES FONCTIONS ######################
###################################################################
def addDocToCorpus(corpus, doc):
    corpus = corpus.append(doc)
    return corpus

def addDataTraining(trainingData, doc):
    doc = cl.text_process(doc)
    trainingData.append(doc)
    return trainingData

file = 'mantisTest3.csv'
fileBis = os.path.splitext(file)[0]+'Bis.csv'
print('fileBis', fileBis)

###################################################################
################ RECUPERATION DES DONNEES MYSQL ###################
###################################################################
'''
query = 'SELECT id, summary FROM mantis_local.mantis_bug_table limit 10000;'
lines = ed.connMySql(cs.serverMySql, cs.databaseMySql, cs.usernameMySql, cs.passwordMySql, query)
#print('lines', lines)

file = 'mantisTest.csv'
fileBis = os.path.splitext(file)[0]+'Bis.csv'
ed.mySqlToCsv(lines, file)  # MySql --> CSV #
'''
cl.clean_file(file)         # Traitement des données récuperées #

###################################################################
######################## TRAINING DATA ############################
###################################################################
trainingData = []
with open(fileBis, 'r') as File:
    csvReader = csv.reader(File, delimiter=',')
    for row in csvReader:
            if row != []:
                #data = cl.text_process(row[1])
                data = cl.text_tTagger(row[1])
                trainingData.append(data)
    print('trainingData', trainingData)
    nbDocs = len(trainingData)

###################################################################
#################### ENTRAINEMENT DU MODELE #######################
###################################################################
model = Word2Vec(trainingData, size=3, min_count=1)
# summarize the loaded model
#print('model', model)

# summarize vocabulary
words = list(model.wv.vocab)
#print('vocabulaire', words)

# access vector for one word
#print('modele cadre', model['cadr'])
# save model
model.save('model.bin')
# load model

X = model[model.wv.vocab]
#print('X', X)

###################################################################
################# CONSTRUCTION DU DICTIONNAIRE ####################
###################################################################

dico = open('dico.txt', 'w')
for word in words:
    dico.writelines(word + '\n')
dico.close()


###################################################################
################## TEST SUR UN NOUVEAU MANTIS #####################
###################################################################
'''def newModel(model, trainingData, doc):
    trainingData.append(doc)
    #print('new trainingData', trainingData)
    model = Word2Vec(trainingData, size=3, min_count=1)
    #print('new model', model)
    #print('moyenne', np.mean(model[doc], axis=0))
    #return np.mean(model[doc], axis=0)
    return model
'''

def newModel(model, trainingData, doc):
    doc2 = [word for word in doc if word in model.wv.vocab]
    if len(doc2) == len(doc):
        model = model
    else:
        trainingData.append(doc)
        print('new trainingData', trainingData)
        model = Word2Vec(trainingData, size=3, min_count=1)
    return model

def document_vector(word2vec_model, trainingData, doc):
    # remove out-of-vocabulary words
    doc2 = [word for word in doc if word in word2vec_model.wv.vocab]
    if len(doc2) == len(doc):
        return np.mean(word2vec_model[doc], axis=0)
    else:
        '''trainingData.append(doc)
        print('newTrainingData', trainingData)
        word2vec_model = Word2Vec(trainingData, size=3, min_count=1)
        print('new model', word2vec_model)
        return np.mean(word2vec_model[doc], axis=0)
        '''
        return np.mean((newModel(word2vec_model, trainingData, doc))[doc], axis=0)

myDoc = input("Entrez un mantis : ")
#print('myDoc1', myDoc)
#myDoc = cl.text_process(myDoc)
myDoc = cl.del_stopwords(cl.text_tTagger(cl.text_cleaning(myDoc)))
print('myDoc2', myDoc)
model = newModel(model, trainingData, myDoc)
myDocVec = np.mean(model[myDoc], axis=0)
#print('new model', model)
print('myDocVec', myDocVec)
print('new trainingData', trainingData)

corpusVec = []
for doc in trainingData:
    docVec = np.mean(model[doc], axis=0)
    corpusVec.append(docVec)
print('corpusVec', corpusVec)

sims = []
maxSim = 0
if nbDocs == len(trainingData):#myDoc in trainingData:
    for i in range(0, len(corpusVec)):
        sim = cosine_similarity([myDocVec, corpusVec[i]])
        sims.append(sim[0][1])
        if (sim[0][1]) > maxSim:
            maxSim = sim[0][1]
            rang = i
else:
    for i in range(0, len(corpusVec)-1):
        sim = cosine_similarity([myDocVec, corpusVec[i]])
        sims.append(sim[0][1])
        if (sim[0][1]) > maxSim:
            maxSim = sim[0][1]
            rang = i
print('sims', sims)

maxSim2 = max(sims)

print('maxSim 1', maxSim, rang)
print('maxSim 2', maxSim2)
#print('le doc le plus similaire est: ', lines[rang][0], trainingData[rang])
print('le doc le plus similaire est: ', trainingData[rang])
'''
sims = cosine_similarity(np.array(np.mean(model[doc], axis=0) for doc in trainingData))
print('sims', sims)

corpusVec = []
for newDoc in trainingData:
    newDocVec = document_vector(model, newDoc)
    corpusVec.append(newDocVec)
print('corpusVec', corpusVec)

myDoc = input("Entrez un mantis : ")
print(myDoc)

addDocToCorpus(corpus, myDoc)
print('corpus mis à jour', corpus)

myDoc = cl.text_process(myDoc)
print(myDoc)
trainingData.append(myDoc)
print('newCorpus mis à jour', trainingData)

sims = cosine_similarity(np.array([document_vector(model, doc) for doc in newCorpus]))
print('sims', sims)


pca = PCA(n_components=2)
result = pca.fit_transform(X)
print('result', result)
# create a scatter plot of the projection
pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):
	pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()
'''