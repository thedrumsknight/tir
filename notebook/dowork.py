from nltk.stem.snowball import SnowballStemmer
from gensim.models import KeyedVectors
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
import re
stopwords_list = stopwords.words('english')

stemmer = SnowballStemmer("english")
wordnet_lemmatizer = WordNetLemmatizer()

from multiprocessing import Pool
def doWork(complete_list, start_index, end_index):
    remove_local = []
    for index, word in enumerate(complete_list[start_index:end_index]):
        if(index%1000==0):
            print(index)
        if word in stopwords_list:
            remove_local.append(word)
            continue
        if re.sub('[^A-Za-z0-9 ]+', '', word) != word:
            remove_local.append(word)
            continue
        if (word.lower()!=word) & (word.lower() in complete_list):
            remove_local.append(word)
            continue
        if (wordnet_lemmatizer.lemmatize(word)!=word) & (wordnet_lemmatizer.lemmatize(word) in complete_list):
            remove_local.append(word)
            continue 
    return remove_local