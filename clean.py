import nltk
import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer

def text_cleaning(text):
    text = text.lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '',  text)
    regex = re.compile(r'[\n\r\t0-9]')
    #regex1 = re.compile(r'[0-9]')
    text = regex.sub(" ", text)
    #text = regex1.sub(" ", text)
    return text

def text_tokenize(text):
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    return tokens


def del_stopwords(word_list):
    stop_words = set(stopwords.words('french'))
    for word in word_list:
        if (len(word) <= 3):
            word_list.remove(word)
            for word in word_list:
                if (word in stop_words):
                    word_list.remove(word)
    return word_list

def text_concat (word_list):
    text = ""
    for word in word_list:
        if text != "":
            text = text + " " + word
        else:
            text = word
    return text


def text_steming(word_list):
    stemmer = FrenchStemmer()
    racine = []
    for word in word_list:
        racine.append(stemmer.stem(word))
    return racine


def clean_file(file):
    with open(file, 'r', encoding='UTF-8') as File:
        csvReader = csv.reader(File, delimiter=',')
        print(file, type(file))
        print('fileExtension', fileExtension[0])
        with open(os.path.splitext(file)[0]+'Bis.csv', 'w', encoding='UTF-8') as FileBis:
            csvWriter = csv.writer(FileBis, delimiter=',')
            csvWriter.writerow(('id', 'description'))
            for line in csvReader:
                if line!=[]:
                    line2 = [line[0]]
                    desc = line[1]
                    line = text_concat(text_steming(del_stopwords(text_tokenize(text_cleaning(desc)))))
                    line2.append(line)
                    csvWriter.writerow(line2)

def


clean_test('mantis.csv')

test = "Texte à nettoyer  : \n tokeniser   le 78797  et supprimer les mots  la fréquents "

print(test)
clean_test = text_cleaning(test)
print('clean_test : ', clean_test)

tokenized_test = text_tokenize(clean_test)

print('tokenized_test : ', tokenized_test)

stop_test = del_stopwords(tokenized_test)

print('test without stopwords : ', stop_test)

stem_test = text_steming(stop_test)
print('stem_test', stem_test)
concat_test = text_concat(stem_test)
#print('concat_test', concat_test)

