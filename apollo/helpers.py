# Helper functions and settings
from apollo.models import *
import random

STARTER_WORDS = ['cat', 'man', 'pillow', 'building', 'helicopter', 'plane']


def get_target_word():	
	return str(TargetWord.objects.latest('datetime').word)

def get_starter_word():
	return random.choice(STARTER_WORDS)

def get_word_options(word):
	# Use word2vec to send 4 closest words to 'word'
	return [random.choice(STARTER_WORDS), random.choice(STARTER_WORDS), random.choice(STARTER_WORDS), random.choice(STARTER_WORDS)]

def get_leaderboard():
	leaderboard = []
	top_players = Player.objects.order_by('-points')[:20]
	for player in top_players:
		leaderboard.append({
			'name': player.name,
			'points': player.points
		})
	return leaderboard