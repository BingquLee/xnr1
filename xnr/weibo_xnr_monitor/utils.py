# -*- coding:utf-8 -*-

'''
weibo information monitor function about database task
'''
import sys
import json
#import time,datetime
from xnr.time_utils import ts2datetime,datetime2ts
from xnr.global_utils import es_flow_text,flow_text_index_name_pre,flow_text_index_type,\
                             es_xnr,weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type,\
                             es_user_profile,profile_index_name,profile_index_type,\
                             weibo_xnr_corpus_index_name,weibo_xnr_corpus_index_type
from xnr.weibo_publish_func import retweet_tweet_func,comment_tweet_func,like_tweet_func,follow_tweet_func                             
from xnr.parameter import MAX_VALUE,DAY,MID_VALUE

#lookup weibo_xnr concerned users
def lookup_weiboxnr_concernedusers(weiboxnr_id):
    result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=weiboxnr_id)
    followers_list=result['_source']['followers_list']
    return followers_list
    #return result

#lookup keywords_string limit with xnr concerned users and time ranges
#input:from_ts,to_ts,weiboxnr_id
#output:keywords_dict,it's used to create wordcloud
def lookup_weibo_keywordstring(from_ts,to_ts,weiboxnr_id):
    
    #step 1 :adjust the time condition for time
    from_date_ts=datetime2ts(ts2datetime(from_ts))
    to_date_ts=datetime2ts(ts2datetime(to_ts))
    range_time_list=[]
    if from_date_ts != to_date_ts:
        iter_date_ts=from_date_ts
        while iter_date_ts <= to_date_ts:
            iter_next_date_ts=iter_date_ts+DAY
            range_time_list.append({'range':{'timestamp':{'gte':iter_date_ts,'lt':iter_next_date_ts}}})
            iter_date_ts=iter_next_date_ts
        if range_time_list[0]['range']['timestamp']['gte']<from_ts:
            range_time_list[0]['range']['timestamp']['gte']=from_ts
        if range_time_list[-1]['range']['timestamp']['lt']>to_ts:
            range_time_list[-1]['range']['timestamp']['lt']=to_ts

    else:
        # lookup from_ts and to_ts ranges in the same index
        range_time_list=[{'range':{'timestamp':{'gte':from_ts,'lt':to_ts}}}]

    #step 2 :select the range of users
    #lookup xnr concerned userslist
    userslist=lookup_weiboxnr_concernedusers(weiboxnr_id)
    #编码：把一个Python对象编码转换成Json字符串   json.dumps()
    #解码：把Json格式字符串解码转换成Python对象   json.loads()
    userslist = json.loads(userslist)					
    user_condition_list=[{'terms':{'uid':userslist}}]

    #step 3:lookup the content
    flow_text_index_name_list = []
    for range_item in range_time_list:
        iter_condition_list=[item for item in user_condition_list]
        iter_condition_list.append(range_item)

        range_from_ts=range_item['range']['timestamp']['gte']
        range_from_date=ts2datetime(range_from_ts)
        flow_text_index_name=flow_text_index_name_pre+range_from_date
        flow_text_index_name_list.append(flow_text_index_name)
        #print flow_text_index_name
        #print iter_condition_list
        
    query_body={
        'query':{
        	'filtered':{
        		'filter':iter_condition_list
        	}
           
        },
        'aggs':{
            'keywords':{
                'terms':{
                    'field':'keywords_string'
                }
            }
        }
    }

    try:
        #print '123'
        flow_text_exist=es_flow_text.search(index=flow_text_index_name_list,doc_type=flow_text_index_type,\
            body=query_body)['aggregations']['keywords']['buckets']
        #print 'flow_text_exist:',flow_text_exist
        #print '456'
    except:
        flow_text_exist=[]

    return flow_text_exist


#lookup hot posts
#input:from_ts,to_ts,weiboxnr_id,classify_id,search_content,order_id
#output:weibo hot_posts content
def lookup_hot_posts(from_ts,to_ts,weiboxnr_id,classify_id,order_id):
    #step 1 :adjust the time condition for time
    from_date_ts=datetime2ts(ts2datetime(from_ts))
    to_date_ts=datetime2ts(ts2datetime(to_ts))
    range_time_list=[]
    if from_date_ts != to_date_ts:
        iter_date_ts=from_date_ts
        while iter_date_ts <= to_date_ts:
            iter_next_date_ts=iter_date_ts+DAY
            range_time_list.append({'range':{'timestamp':{'gte':iter_date_ts,'lt':iter_next_date_ts}}})
            iter_date_ts=iter_next_date_ts
        if range_time_list[0]['range']['timestamp']['gte']<from_ts:
            range_time_list[0]['range']['timestamp']['gte']=from_ts
        if range_time_list[-1]['range']['timestamp']['lt']>to_ts:
            range_time_list[-1]['range']['timestamp']['lt']=to_ts

    else:
        # lookup from_ts and to_ts ranges in the same index
        range_time_list=[{'range':{'timestamp':{'gte':from_ts,'lt':to_ts}}}]

    #step2: users condition
    #make sure the users range by classify choice
    userslist=lookup_weiboxnr_concernedusers(weiboxnr_id)
    userslist = json.loads(userslist)
    user_condition_list=[{'terms':{'uid':userslist}}]

    #step 3:keyword condition,delete
    #if search_content:
    #    keyword_condition_list=[{'match':{'text':{'query':search_content}}}]
    #else:
    #    keyword_condition_list=[]

    #step 4:sort order condition set
    if order_id==1:         #按时间排序
        sort_condition_list=[{'timestamp':{'order':'desc'}}]         
    elif order_id==2:       #按热度排序
        sort_condition_list=[{'hot':{'order':'desc'}}]
    elif order_id==3:       #按敏感度排序
        sort_condition_list=[{'mingan':{'order':'desc'}}]
    else:                   #默认设为按时间排序
        sort_condition_list=[{'timestamp':{'order':'desc'}}]

    #step 5:lookup the content
    flow_text_index_name_list=[]
    for range_item in range_time_list:
    	iter_condition_list=[]
        if classify_id==1:             #当类别选择为所关注用户时
            iter_condition_list=[item for item in user_condition_list]
 		#当类别选择为全部用户时，不设置用户这一限制条件
        #if keyword_condition_list:
        #    iter_condition_list.append(keyword_condition_list)
        iter_condition_list.append(range_item)

        range_from_ts=range_item['range']['timestamp']['gte']
        range_from_date=ts2datetime(range_from_ts)
        flow_text_index_name=flow_text_index_name_pre+range_from_date
        flow_text_index_name_list.append(flow_text_index_name)
        #print flow_text_index_name
        #print iter_condition_list
        print sort_condition_list
    print flow_text_index_name_list
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':iter_condition_list
                        }
                    }
                }
            },
        'size':MAX_VALUE,		
        'sort':sort_condition_list
        }
    try:
        flow_text_exist=es_flow_text.search(index=flow_text_index_name_list,doc_type=flow_text_index_type,\
            body=query_body)['hits']['hits']
        #print 'folw_text_exit:',flow_text_exist
    except:
        flow_text_exist=[]
        #scan the flow_text_exist content and change the from to hot posts

    #organize the result content and use the public function
    ###############################################################
    weibo_content=flow_text_exist['_source']['text']
    for content in weibo_content:
        print content
        #use the function 
    return flow_text_exist

#################微博操作##########
#转发微博
def get_weibohistory_retweet(task_detail):
    text=task_detail['text']
    r_mid=task_detail['r_mid']

    xnr_user_no=task_detail['xnr_user_no']
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

    #调用转发微博函数
    mark=retweet_tweet_func(account_name,password,text,r_mid)
    
    # 保存微博，将转发微博保存至flow_text_表
    ###########################################
    return mark

#评论
def get_weibohistory_comment(task_detail):
    text=task_detail['text']
    r_mid=task_detail['r_mid']

    xnr_user_no=task_detail['xnr_user_no']
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

    #调用评论微博函数
    mark=comment_tweet_func(account_name,password,text,r_mid)
    
    # 保存评论，将评论内容保存至表
    ###########################################
    return mark

#赞
def get_weibohistory_like(task_detail):
    r_mid=task_detail['r_mid']

    xnr_user_no=task_detail['xnr_user_no']
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

    #调用点赞函数
    mark=like_tweet_func(account_name,password,r_mid)

    #保存点赞信息至weibo_feedback_like表
    ###########################################
    return mark

#直接关注
def attach_fans_follow(task_detail):
    xnr_user_no=task_detail['xnr_user_no']
    xnr_es_result=es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
    account_name=xnr_es_result['weibo_mail_account']
    password=xnr_es_result['password']

    uid=task_detail['uid','']

    #调用关注函数
    mark=follow_tweet_func(account_name,password,uid)
    #if mark:
        #保存至关注列表
    #######################
    return mark

###加入语料库


###############################################################



#lookup acitve_user
#input:classify_id,weiboxnr_id
#output:active weibo_user info list
def lookup_active_weibouser(classify_id,weiboxnr_id):
    #step1: users condition
    #make sure the users range by classify choice
    userlist = lookup_weiboxnr_concernedusers(weiboxnr_id)
    userlist = json.loads(userlist)
    if classify_id==1:		#concrenedusers
    	condition_list=[{'bool':{'must':{'terms':{'uid':userlist}}}}]
        #print 'aaaa'
    elif classify_id==2:	#unconcrenedusers
    	condition_list=[{'bool':{'must_not':{'terms':{'uid':userlist}}}}] 
    else:
    	condition_list=[{'match_all':{}}]
    print userlist,classify_id,condition_list

    #step 2:lookup users and ranked by infuluence
    for item in condition_list:
        print item
        query_body={
            '_source':{
                'include':[
                    'id',            #用户ID
                    'nick_name',     #昵称
                    'user_location', #注册地
                    #'fansum',        #粉丝数
                    #'weibosum',      #微博数，该字段暂未创建
                    #'infulence'     #影响力，该字段需创建然后计算
                ]
            },
            'query':item,
            'size':MID_VALUE,		#查询影响力排名前500的用户即可
            #'sort':{'infuluence':{'order':'desc'}}    #根据影响力排名
            }
    try:
        flow_text_exist=es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,body=query_body)['hits']['hits']
    except:
        flow_text_exist=[]

    return flow_text_exist

#weibo_user_detail
def weibo_user_detail(user_id):
	result=es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=user_id)
	return result
            

###############code test###################
def weibo_user_test():
    query_body={
        '_source':{
            'include':['id']
        },
        'query':{
            'match_all':{}
        },
        'size':999
    }
    result=es_flow_text.search(index='weibo_user',doc_type='user',body=query_body)['hits']['hits']
    return result
