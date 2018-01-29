# -*-coding:utf-8-*-

import sys

sys.append('../../')
from global_utils import R_OPERATE_QUEUE as r, operate_queue_name
from utils import add_operate2redis

sys.append('../facebook_xnr_operate/')
from utils import get_submit_tweet_fb, get_comment_operate_fb, get_retweet_operate_fb, get_at_operate_fb,\
				get_like_operate_fb,get_private_operate_fb, get_add_friends, get_confirm_friends, \
				get_delete_friend 


sys.append('../twitter_xnr_operate/')
from utils import get_submit_tweet_tw, get_comment_operate_tw, get_retweet_operate_tw, get_at_operate_tw,\
				get_like_operate_tw,get_private_operate_tw, get_follow_operate_tw, get_unfollow_operate_tw

# publish-发帖、retweet-转发、comment-评论、like-点赞、follow-关注、unfollow-取消关注、at-提到、private-私信
    # add-发送添加好友请求、confirm-确认好友请求、delete-删除好友请求

def operate_out_of_redis():

	while True:
		temp = r.rpop(operate_queue_name)
		if not temp:
			break

		queue_dict = json.loads(temp)
		
		channel = queue_dict['channel']
		operate_type = queue_dict['operate_type']

		task_detail = queue_dict['content']

		if channel == 'facebook':
			if operate_type == 'publish':
				try:
				    mark = get_submit_tweet_fb(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'retweet':
				try:
				    mark = get_retweet_operate_fb(task_detail)
				except:
					add_operate2redis(queue_dict)
			elif operate_type == 'comment':
				try:
				    mark = get_comment_operate_fb(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'like':
				try:
				    mark = get_like_operate_fb(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'at':
				try:
				    mark = get_at_operate_fb(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'private':
				try:
				    mark = get_private_operate_fb(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'add':
				try:
				    mark = get_add_friends(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'confirm':
				try:
				    mark = get_confirm_friends(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'delete':
				try:
				    mark = get_delete_friends(task_detail)
				except:
					add_operate2redis(queue_dict)


		elif channel == 'twitter':
			if operate_type == 'publish':
				try:
				    mark = get_submit_tweet_tw(task_detail)
				except:
					add_operate2redis(queue_dict)
			elif operate_type == 'retweet':
				try:
				    mark = get_retweet_operate_tw(task_detail)
				except:
					add_operate2redis(queue_dict)
			elif operate_type == 'comment':
				try:
				    mark = get_comment_operate_tw(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'like':
				try:
				    mark = get_like_operate_tw(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'at':
				try:
				    mark = get_at_operate_tw(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'private':
				try:
				    mark = get_private_operate_tw(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'follow':
				try:
				    mark = get_follow_operate_tw(task_detail)
				except:
					add_operate2redis(queue_dict)

			elif operate_type == 'unfollow':
				try:
				    mark = get_unfollow_operate_tw(task_detail)
				except:
					add_operate2redis(queue_dict)

if __name__ == '__main__':
	
	operate_out_of_redis()			





