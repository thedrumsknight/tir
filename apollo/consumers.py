from channels import Group
import json
from apollo.models import *
from apollo.helpers import *
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http


@channel_session_user_from_http  
def ws_connect(message):
	Group('users').add(message.reply_channel)
	message.channel_session['word_path'] = []
	message.channel_session['word_path_compound'] = []
	message.channel_session['username'] = message.user.username
	message.channel_session['current_target_word'] = get_target_word()
	target_word = get_target_word()
	starter_words = get_starter_words()
	previous_target_word, completed_from, completed_in = get_previous_target_word_details()
	p = Player.objects.get(name=message.channel_session['username'])
	p.is_logged_in = True
	p.save()
	active_users = len(Player.objects.filter(is_logged_in=True))
	Group('users').send({
		'text': json.dumps({
			'activeUsers': active_users,
		})
	})
	leaderboard = get_leaderboard()
	print(leaderboard)
	message.reply_channel.send({
		'text': json.dumps({
			'targetWord': target_word,
			'completedIn': completed_in,
			'completedFrom': completed_from,
			'wordOptions': starter_words,
			'leaderboard': leaderboard,
			'previousTargetWord': previous_target_word,
		})
	})


@channel_session_user
def ws_receive(message):
	data = json.loads(message['text'])
	clicked_word = data['word']
	message.channel_session['word_path'].append(clicked_word)
	message.channel_session['word_path_compound'].append(clicked_word)
	username = message.channel_session['username']
	# import pdb; pdb.set_trace()
	current_target_word = get_target_word() 
	if message.channel_session['current_target_word'] != current_target_word:
		message.channel_session['word_path'] = [clicked_word] 
	word_options = get_word_options(clicked_word, message.channel_session['word_path'])
	message.channel_session['current_target_word'] = current_target_word
	if (clicked_word == current_target_word):
		p = Player.objects.get(name=username)
		p.points = p.points + len(Player.objects.filter(is_logged_in=True))
		p.save()
		completed_in = len(message.channel_session['word_path_compound'])
		completed_from = message.channel_session['word_path_compound'][0]
		w = TargetWord.objects.latest('datetime')
		w.completed_in = completed_in
		w.completed_from = completed_from
		previous_target_word = w.word
		w.save()
		message.channel_session['word_path_compound'] = []
		message.channel_session['word_path'] = []
		new_target_word = set_target_word(current_target_word)
		leaderboard = get_leaderboard()
		Group('users').send({
			'text': json.dumps({
				'targetWord': new_target_word,
				'leaderboard': leaderboard,
				'completedFrom': completed_from,
				'completedIn': completed_in,
				'previousTargetWord': previous_target_word,
			})
		})
	message.reply_channel.send({
		'text': json.dumps({
			'wordOptions': word_options,
		})
	})



@channel_session_user
def ws_disconnect(message):
	Group('users').discard(message.reply_channel)
	p = Player.objects.get(name=message.channel_session['username'])
	p.is_logged_in = False
	p.save()
	active_users = len(Player.objects.filter(is_logged_in=True))
	Group('users').send({
		'text': json.dumps({
			'activeUsers': active_users,
		})
	})
