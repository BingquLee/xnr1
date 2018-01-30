#!/usr/bin/env python
# encoding: utf-8

import time
from launcher import Launcher
from Elasticsearch_fb import Es_fb
from feedback_comment import Comment
from feedback_friends import Friend
from feedback_like import Like
from feedback_mention import Mention
from feedback_message import Message
from feedback_online import Online
from feedback_share import Share

def execute(username, password):
	#launcher = Launcher(username, password)
	#driver = launcher.login()
	#es = Es_fb()

	comment = Comment(username, password)
	list = comment.get_comment()
	comment.save('facebook_feedback_comment_2017-11-13','text',list)

	friend = Friend(username, password)
	list = friend.get_friend()
	friend.save('facebook_feedback_friends','text',list)

	like = Like(username, password)
	list = like.get_like()
	like.save('facebook_feedback_like_2017-11-13','text',list)

	mention = Mention(username, password)
	list = mention.get_mention()
	mention.save('facebook_feedback_at_2017-11-13','text',list)

	message = Message(username, password)
	list = message.get_message()
	message.save('facebook_feedback_private_2017-11-13','text',list)

	online = Online(username, password)

	share = Share(username, password)
	list = share.get_share()
	share.save('facebook_feedback_retweet_2017-11-13','text',list)
	
if __name__ == '__main__':
	execute('8617078448226','xnr123456')