import csv
import string
import os
import nltk
import string
import re
import os

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer

#####  FUNCTIONS ######
def text_cleaning(text):
    text = text.lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ',  text)
    regex = re.compile(r'[\n\r\t]')
    regex1 = re.compile(r'[0-9]')
    text = regex.sub(" ", text)
    text = regex1.sub(" ", text)
    return text


def text_tokenize(text):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return tokens


def del_stopwords(word_list):
    stop_words = set(stopwords.words('french'))
    for word in word_list:
        if (len(word) < 3):
            word_list.remove(word)
            for word in word_list:
                if (word in stop_words):
                    word_list.remove(word)
    return word_list


def text_steming(word_list):
    stemmer = FrenchStemmer()
    racine = []
    for word in word_list:
        racine.append(stemmer.stem(word))
    return racine


def text_concat(word_list):
    text = ""
    for word in word_list:
        if text != "":
            text = text + " " + word
        else:
            text = word
    return text


def clean_file(file):
    #with open(file, 'r', encoding='UTF-8') as File:
    with open(file, 'r') as File:
        csvReader = csv.reader(File, delimiter=',')
        with open(os.path.splitext(file)[0]+'Bis.csv', 'w') as FileBis:
            csvWriter = csv.writer(FileBis, delimiter=',')
            #csvWriter.writerow(('id', 'description'))
            for line in csvReader:
                if line!=[]:
                    line2 = [line[0]]
                    desc = line[1]
                    line = text_concat(text_steming(del_stopwords(text_tokenize(text_cleaning(no_accent(no_apostrophe(desc)))))))
                    line2.append(line)
                    csvWriter.writerow(line2)
    return FileBis


def no_accent(text):
    accent = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â']
    zero_accent = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a']
    for i in range(len(accent)):
        text = text.replace(accent[i], zero_accent[i])
    print(text)
    return text


def text_process(text):
    text = text_steming(del_stopwords(text_tokenize(text_cleaning(text))))
    return text


def no_apostrophe(text):
    apostrophe = ['d\'', 'l\'', 'j\'ai', 'n\'', 'des', 'les']
    for i in range(len(apostrophe)):
        text = text.replace(apostrophe[i], '')
    return text


from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()

s1=stemmer.stem('voudrais')

s2=stemmer.stem('animaux')

s3=stemmer.stem('yeux')

s4=stemmer.stem('dors')

s5=stemmer.stem('couvre')
s6=stemmer.stem('avons')

print('lemmes', s1, s2, s3, s4, s5, s6)

'''
import spacy
nlp = spacy.load('fr')

doc = nlp(u"voudrais non animaux yeux dors couvre.")
for token in doc:
    print(token, token.lemma_)
'''

import pprint
import treetaggerwrapper
#build a TreeTagger wrapper:
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')
#tag your text.
tags = tagger.tag_text("ceci est un petit texte qu'il faut comprendre prenais avions")
#use the tags list... (list of string output from TreeTagger).
pprint.pprint(tags)

tags2 = treetaggerwrapper.make_tags(tags)
pprint.pprint(tags2)


'''
s2 = ("Alas, it has not rained today. When, do you think, will it rain again?")
#regexp_tokenize(s2, r'[,\.\?!"]\s*', gaps=False)

tokenizer = nltk.RegexpTokenizer(r'[,\.\?!"]\s*')
tokens = tokenizer.tokenize(s2)
print('tokens', tokens)


test = re.sub(r"(d')", r"  ", "dabdcd'ef")
print(test)


re.sub(r"(ab)", r" \1 ", "abcdef")



clean_file('mantis.csv')
word_list = ['aa','bb']
concat = text_concat(word_list)
print('concat', concat)
'''

'''
##### CLEANING MANTIS.CSV -->> MANTISBIS.CSV #####

with open('mantis.csv', 'r', encoding='UTF-8') as mantisFile:
    csvReaderMantis = csv.reader(mantisFile, delimiter=',')
    with open('mantisBis.csv', 'w', encoding='UTF-8') as mantisFileBis:
        csvWriterMantis = csv.writer(mantisFileBis, delimiter=',')
        csvWriterMantis.writerow(('id_mantis', 'description_mantis'))

        for line in csvReaderMantis:

            if line!=[]:
            #print(line)
                line2 = [line[0]]
                desc = line[1]
            #print(desc)
                line = text_concat(text_steming(del_stopwords(text_tokenize(text_cleaning(desc)))))
                #print('LINE', line)
                line2.append(line)
                csvWriterMantis.writerow(line2)
'''