# Helper functions and settings
from apollo.models import *
import random
from nltk.stem import WordNetLemmatizer
from gensim.models import KeyedVectors
from tir.settings import MODEL_PATH

wordnet_lemmatizer = WordNetLemmatizer()

STARTER_WORDS = ['cat', 'man', 'building', 'helicopter', 'plane', 'dog']
TARGET_WORDS = ['house', 'Obama',  'garden', 'garbage', 'light', 'Frost']

model = KeyedVectors.load_word2vec_format(MODEL_PATH, unicode_errors = 'replace', binary = 'True', limit=10000)

def get_target_word():	
	return str(TargetWord.objects.latest('datetime').word)

def get_previous_target_word_details():
	return TargetWord.objects.order_by('-datetime')[1].word, TargetWord.objects.order_by('-datetime')[1].completed_from, TargetWord.objects.order_by('-datetime')[1].completed_in

def get_starter_words():
	random.shuffle(STARTER_WORDS)
	return STARTER_WORDS[:4]

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (wordnet_lemmatizer.lemmatize(x.lower()) in seen or seen_add(wordnet_lemmatizer.lemmatize(x.lower())))]

def get_word_options(word, pre_used_words):
	# Use word2vec to send 4 closest words to 'word'
    w = [i[0] for i in model.most_similar(word,topn=40) if "_" not in i[0]]
    w = [i for i in w if (i.lower() not in pre_used_words and wordnet_lemmatizer.lemmatize(i) not in pre_used_words)]
    w = f7(w)
    return w[:4]
	#return [random.choice(STARTER_WORDS), random.choice(STARTER_WORDS), random.choice(STARTER_WORDS), random.choice(STARTER_WORDS)]

def get_leaderboard():
	leaderboard = []
	top_players = Player.objects.order_by('-points')[:20]
	for player in top_players:
		leaderboard.append({
			'name': player.name,
			'points': player.points
		})
	return leaderboard

def set_target_word(previous_target):
	word = random.choice(TARGET_WORDS)
	while (word == previous_target):
		word = random.choice(TARGET_WORDS)
	TargetWord.objects.create(word=word)
	return word
