from channels import Group
import json
from apollo.models import *
from apollo.helpers import *
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http


@channel_session_user_from_http  
def ws_connect(message):
    Group('users').add(message.reply_channel)
    target_word = get_target_word()
    starter_word = get_starter_word()
    word_options = get_word_options(starter_word)
    message.channel_session['word_path'] = []
    message.channel_session['username'] = message.user.username
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
    		'wordOptions': word_options,
    		'leaderboard': leaderboard,
    	})
    })


@channel_session_user
def ws_receive(message):
	data = json.loads(message['text'])
	clicked_word = data['word']
	message.channel_session['word_path'].append(clicked_word)
	
	word_options = get_word_options(clicked_word)
	username = message.channel_session['username']
	# import pdb; pdb.set_trace()
	current_target_word = get_target_word()
	if (clicked_word == current_target_word):
		new_target_word = set_target_word(current_target_word)
		p = Player.objects.get(name=username)
		p.points = p.points + len(Player.objects.filter(is_logged_in=True))
		p.save()
		leaderboard = get_leaderboard()
		Group('users').send({
			'text': json.dumps({
				'targetWord': new_target_word,
				'wordOptions': word_options,
				'leaderboard': leaderboard

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
