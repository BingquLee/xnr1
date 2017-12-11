#-*- coding: utf-8 -*-
'''
facebook warming function
'''
import os
import json
import time
import sys
reload(sys)
sys.path.append('../../')
from timed_python_files.system_log_create import get_user_account_list
from parameter import DAY,MAX_VALUE,WARMING_DAY,USER_XNR_NUM
from global_config import S_TYPE,FACEBOOK_FLOW_START_DATE
from time_utils import ts2datetime,datetime2ts,get_day_flow_text_index_list,ts2yeartime,get_timets_set_indexset_list
from global_utils import es_xnr,fb_xnr_index_name,fb_xnr_index_type,weibo_date_remind_index_name,weibo_date_remind_index_type,\
                         fb_xnr_fans_followers_index_name,fb_xnr_fans_followers_index_type,\
                         facebook_flow_text_index_name_pre,facebook_flow_text_index_type,\
                         facebook_speech_warning_index_name_pre,facebook_speech_warning_index_type,\
                         facebook_feedback_friends_index_name,facebook_feedback_friends_index_type,\
                         facebook_user_warning_index_name_pre,facebook_user_warning_index_type,\
                         facebook_timing_warning_index_name_pre,facebook_timing_warning_index_type

 
#虚拟人列表
def get_user_xnr_list(user_account):
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{
                        'must':[
                        {'term':{'submitter':user_account}},
                        {'term':{'create_status':2}}
                        ]
                    }
                }
            }
        },
        'size':USER_XNR_NUM
    }
    try:
        user_result=es_xnr.search(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no_list=[]
        for item in user_result:
            xnr_user_no_list.append(item['_source']['xnr_user_no'])
    except:
        xnr_user_no_list=[]
    return xnr_user_no_list                         

#查询虚拟人uid
def lookup_xnr_uid(xnr_user_no):
    try:
        xnr_result=es_xnr.get(index=fb_xnr_index_name,doc_type=fb_xnr_index_type,id=xnr_user_no)['_source']
        xnr_uid=xnr_result['uid']
    except:
        xnr_uid=''
    return xnr_uid


#查询好友列表
def lookup_xnr_friends(xnr_user_no):
    try:
        xnr_result=es_xnr.get(index=fb_xnr_fans_followers_index_name,doc_type=fb_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
        lookup_list=xnr_result['fans_list']
    except:
        lookup_list=[]
    return lookup_list



#言论内容预警
def create_speech_warning(xnr_user_no,today_datetime):
    #查询好友列表
    friends_list=lookup_xnr_friends(xnr_user_no)
    
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'bool':{'must':{'range':{'sensitive':{'gte':1}}}}
                }
            }
        },
        'size':MAX_VALUE,
        'sort':{'sensitive':{'order':'desc'}}
    }
    facebook_flow_text_index_name=get_timets_set_indexset_list(facebook_flow_text_index_name_pre,today_datetime,today_datetime)
    #print facebook_flow_text_index_name
    results=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
    #print results
    result=[]
    for item in results:
        if item['_source']['uid'] in friends_list:
            item['_source']['content_type']='friends'
        else:
            item['_source']['content_type']='unfriends'

        item['_source']['validity']=0
        item['_source']['xnr_user_no']=xnr_user_no

        task_id=xnr_user_no+'_'+item['_source']['fid']

        #写入数据库
        today_date=ts2datetime(today_datetime)
        facebook_speech_warning_index_name=facebook_speech_warning_index_name_pre+today_date
        #facebook_speech_warning_index_name=facebook_speech_warning_index_name_pre+FACEBOOK_FLOW_START_DATE
        # try:
        es_xnr.index(index=facebook_speech_warning_index_name,doc_type=facebook_speech_warning_index_type,body=item['_source'],id=task_id)
        mark=True
        # except:
        #     mark=False

        result.append(mark)
    return result


#人物行为预警
def create_personal_warning(xnr_user_no,today_datetime):
    #查询好友列表
    friends_list=lookup_xnr_friends(xnr_user_no)

    #查询虚拟人uid
    xnr_uid=lookup_xnr_uid(xnr_user_no)

    #计算敏感度排名靠前的用户
    query_body={
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'uid':friends_list}
                }
            }
        },
        'aggs':{
            'friends_sensitive_num':{
                'terms':{'field':'uid'},
                'aggs':{
                    'sensitive_num':{
                        'sum':{'field':'sensitive'}
                    }
                }                        
            }
            },
        'size':MAX_VALUE
    }

    facebook_flow_text_index_name=get_timets_set_indexset_list(facebook_flow_text_index_name_pre,today_datetime,today_datetime)
    
    try:   
        first_sum_result=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,\
        body=query_body)['aggregations']['friends_sensitive_num']['buckets']
    except:
        first_sum_result=[]

    print 'first_sum_result',first_sum_result
    top_userlist=[]
    for i in xrange(0,len(first_sum_result)):
        user_sensitive=first_sum_result[i]['sensitive_num']['value']
        if user_sensitive > 0:
            user_dict=dict()
            user_dict['uid']=first_sum_result[i]['key']
            user_dict['sensitive']=user_sensitive
            top_userlist.append(user_dict)
        else:
            pass

    #查询敏感用户的敏感内容
    results=[]
    for user in top_userlist:
        #print user
        user_detail=dict()
        user_detail['uid']=user['uid']
        user_detail['user_sensitive']=user['sensitive']
        user_lookup_id=user['uid']
        print user_lookup_id
        try:
            user_result=es_xnr.get(index=facebook_feedback_friends_index_name,doc_type=facebook_feedback_friends_index_type,id=user_lookup_id)['_source']
            #user_result=es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=user['uid'])['_source']
            user_detail['user_name']=user_result['nick_name']
        except:
            user_detail['user_name']=''

        query_body={
            'query':{
                'filtered':{
                    'filter':{
                        'bool':{
                            'must':[
                                {'term':{'uid':user['uid']}},
                                {'range':{'sensitive':{'gte':1}}}
                            ]
                        }
                    }
                }
            },
            'size':MAX_VALUE,
            'sort':{'sensitive':{'order':'desc'}}
        }

        try:
            second_result=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
        except:
            second_result=[]

        s_result=[]
        for item in second_result:
            s_result.append(item['_source'])

        s_result.sort(key=lambda k:(k.get('sensitive',0)),reverse=True)
        user_detail['content']=json.dumps(s_result)

        user_detail['xnr_user_no']=xnr_user_no
        user_detail['validity']=0
        user_detail['timestamp']=today_datetime

        #写入数据库
        today_date=ts2datetime(today_datetime)
        facebook_user_warning_index_name=facebook_user_warning_index_name_pre+today_date

        task_id=xnr_user_no+'_'+user_detail['uid']
        try:
            es_xnr.index(index=facebook_user_warning_index_name,doc_type=facebook_user_warning_index_type,body=user_detail,id=task_id)
            mark=True
        except:
            mark=False

        results.append(mark)

    return results



#时间预警
def create_date_warning(today_datetime):
    query_body={
        'query':{
            'match_all':{}
        },
        'size':MAX_VALUE,
        'sort':{'date_time':{'order':'asc'}}
    }
    try:
        result=es_xnr.search(index=weibo_date_remind_index_name,doc_type=weibo_date_remind_index_type,body=query_body)['hits']['hits']
        date_result=[]
        for item in result:
            #计算距离日期
            date_time=item['_source']['date_time']
            year=ts2yeartime(today_datetime)
            warming_date=year+'-'+date_time
            today_date=ts2datetime(today_datetime)
            countdown_num=(datetime2ts(warming_date)-datetime2ts(today_date))/DAY
        
            if abs(countdown_num) < WARMING_DAY:
                #根据给定的关键词查询预警微博
                keywords=item['_source']['keywords']
                date_warming=lookup_facebook_date_warming(keywords,today_datetime)
                item['_source']['facebook_date_warming_content']=json.dumps(date_warming)
                item['_source']['validity']=0
                item['_source']['timestamp']=today_datetime

                task_id=str(item['_source']['create_time'])+'_'+str(today_datetime)    
                #print 'task_id',task_id
                #写入数据库
                
                facebook_timing_warning_index_name=facebook_timing_warning_index_name_pre+warming_date
                
                if date_warming:
                    print facebook_timing_warning_index_name
                    try:

                        es_xnr.index(index=facebook_timing_warning_index_name,doc_type=facebook_timing_warning_index_name,body=item['_source'],id=task_id)
                        mark=True
                    except:
                        mark=False
                else:
                    pass

                date_result.append(mark)
        else:
            pass

    except:
        date_result=[]
    return date_result


def lookup_facebook_date_warming(keywords,today_datetime):
    keyword_query_list=[]
    for keyword in keywords:
        keyword_query_list.append({'wildcard':{'text':'*'+keyword.encode('utf-8')+'*'}})

    facebook_flow_text_index_name=get_timets_set_indexset_list(facebook_flow_text_index_name_pre,today_datetime,today_datetime)

    query_body={
        'query':{
            'bool':
            {
                'should':keyword_query_list,
                'must':{'range':{'sensitive':{'gte':1}}}
            }
        },
        'size':MAX_WARMING_SIZE,
        'sort':{'sensitive':{'order':'desc'}}
    }
    try:
        temp_result=es_xnr.search(index=facebook_flow_text_index_name,doc_type=facebook_flow_text_index_type,body=query_body)['hits']['hits']
        date_result=[]
        for item in temp_result:
            date_result.append(item['_source'])
    except:
            date_result=[]
    return date_result





# #事件预警
# #事件涌现思路：
# #（1）根据get_hashtag获取事件名称
# #（2）在流数据中查询与事件名相关的微博数据，
# #（3）根据虚拟人编号查找粉丝和关注人的uid，统计事件名称相关的微博数据中粉丝、关注人出现的频次，如果既是关注人又是粉丝则频次相加。取频次前三用户
# #（4）计算微博数据的转发数、评论数、敏感等级，得到微博影响力的初始值,
# #计算微博影响力的值=初始影响力值X（粉丝值（是1.2，否0.8）+关注值（是1.2，否0.8）
# def get_hashtag(now_time):

#     uid_list = []
#     hashtag_list = {}

#     with open(UID_TXT_PATH+'/uid_sensitive.txt','rb') as f:
#         for line in f:
#             uid = line.strip()
#             uid_list.append(uid)

#     for uid in uid_list:
#         if S_TYPE == 'test':
#             hashtag = r_cluster.hget('hashtag_' + str(datetime2ts(S_DATE_WARMING)-DAY),uid)
#             #hashtag = r_cluster.hget('hashtag_'+str(datetime2ts(S_DATE)+7*DAY),uid)
#         else:
#             hashtag = r_cluster.hget('hashtag_' + str(now_time),uid)
#             #hashtag = r_cluster.hget('hashtag_'+str((time.time()-DAY)),uid)

#         if hashtag != None:
#             hashtag = hashtag.encode('utf8')
#             hashtag = json.loads(hashtag)

#             for k,v in hashtag.iteritems():
#                 try:
#                     hashtag_list[k] += v
#                 except:
#                     hashtag_list[k] = v
#         #r_cluster.hget('hashtag_'+str(a))

#     hashtag_list = sorted(hashtag_list.items(),key=lambda x:x[1],reverse=True)[:200]

#     return hashtag_list



# def create_event_warning(xnr_user_no,today_datetime,write_mark):
#     #获取事件名称
#     hashtag_list = get_hashtag(today_datetime)
#     print 'hashtag_list::',hashtag_list

#     flow_text_index_name = get_day_flow_text_index_list(today_datetime)

#     #虚拟人的粉丝列表和关注列表
#     try:
#         es_xnr_result=es_xnr.get(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,id=xnr_user_no)['_source']
#         followers_list=es_xnr_result['followers_list']
#         fans_list=es_xnr_result['fans_list']
#     except:
#         followers_list=[]
#         fans_list=[]

#     event_warming_list=[]
#     for event_item in hashtag_list:
#         event_sensitive_count=0
#         event_warming_content=dict()     #事件名称、主要参与用户、典型微博、事件影响力、事件平均时间
#         event_warming_content['event_name']=event_item[0]
#         print 'event_name:',event_item[0]
#         event_influence_sum=0
#         event_time_sum=0       
#         query_body={
#             'query':{
#                 'bool':{
#                     'should':{'wildcard':{'text':'*'+event_item[0]+'*'}}
#                 }
#             }
#         }
#         try:         
#             event_results=es_flow_text.search(index=flow_text_index_name,doc_type=flow_text_index_type,body=query_body)['hits']['hits']
#             weibo_result=[]
#             fans_num_dict=dict()
#             followers_num_dict=dict()
#             alluser_num_dict=dict()
#             for item in event_results:
#                 if item['_source']['sensitive'] >0:
#                     event_sensitive_count=event_sensitive_count+1
#                     #统计用户信息
#                     if alluser_num_dict.has_key(str(item['_source']['uid'])):
#                         alluser_num_dict[str(item['_source']['uid'])]=alluser_num_dict[str(item['_source']['uid'])]+1
#                     else:
#                         alluser_num_dict[str(item['_source']['uid'])]=1
                        
#                     for fans_uid in fans_list:                    
#                         if fans_uid==item['_source']['uid']:
#                             if fans_num_dict.has_key(str(fans_uid)):
#                                 fans_num_dict[str(fans_uid)]=fans_num_dict[str(fans_uid)]+1
#                             else:
#                                 fans_num_dict[str(fans_uid)]=1
#                         else:
#                             pass
                        
#                     for followers_uid in followers_list:
#                         if followers_uid==item['_source']['uid']:
#                             if followers_num_dict.has_key(str(followers_uid)):
#                                 fans_num_dict[str(followers_uid)]=fans_num_dict[str(followers_uid)]+1
#                             else:
#                                 fans_num_dict[str(followers_uid)]=1
#                         else:
#                             pass

#                     #计算影响力
#                     origin_influence_value=(item['_source']['comment']+item['_source']['retweeted'])*(1+item['_source']['sensitive'])
#                     fans_value=judge_user_type(item['_source']['uid'],fans_list)
#                     followers_value=judge_user_type(item['_source']['uid'],followers_list)
#                     item['_source']['weibo_influence_value']=origin_influence_value*(fans_value+followers_value)
#                     weibo_result.append(item['_source'])

#                     #统计影响力、时间
#                     event_influence_sum=event_influence_sum+item['_source']['weibo_influence_value']
#                     event_time_sum=item['_source']['timestamp']            

#             #典型微博信息
#             weibo_result.sort(key=lambda k:(k.get('weibo_influence_value',0)),reverse=True)
#             event_warming_content['main_weibo_info']=json.dumps(weibo_result)

#             #事件影响力和事件时间
#             number=len(event_results)
#             event_warming_content['event_influence']=event_influence_sum/number
#             event_warming_content['event_time']=event_time_sum/number

#         except:
#             event_warming_content['main_weibo_info']=[]
#             event_warming_content['event_influence']=0
#             event_warming_content['event_time']=0
        
#         try:
#             if event_sensitive_count > 0:
#             #对用户进行排序
#                 temp_userid_dict=union_dict(fans_num_dict,followers_num_dict)
#                 main_userid_dict=union_dict(temp_userid_dict,alluser_num_dict)
#                 main_userid_dict=sorted(main_userid_dict.items(),key=lambda d:d[1],reverse=True)
#                 main_userid_list=[]
#                 for i in xrange(0,len(main_userid_dict)):
#                     main_userid_list.append(main_userid_dict[i][0])

#                 #主要参与用户信息
#                 main_user_info=[]
#                 user_es_result=es_user_profile.mget(index=profile_index_name,doc_type=profile_index_type,body={'ids':main_userid_list})['docs']
#                 for item in user_es_result:
 
#                     user_dict=dict()
#                     if item['found']:
#                         user_dict['photo_url']=item['_source']['photo_url']
#                         user_dict['uid']=item['_id']
#                         user_dict['nick_name']=item['_source']['nick_name']
#                         user_dict['favoritesnum']=item['_source']['favoritesnum']
#                         user_dict['fansnum']=item['_source']['fansnum']
#                     else:
#                         user_dict['photo_url']=''
#                         user_dict['uid']=item['_id']
#                         user_dict['nick_name']=''
#                         user_dict['favoritesnum']=0
#                         user_dict['fansnum']=0
#                     main_user_info.append(user_dict)
#                 event_warming_content['main_user_info']=json.dumps(main_user_info)

#             else:
#                 event_warming_content['main_user_info']=[]
#         except:
#             event_warming_content['main_user_info']=[]

#         event_warming_content['xnr_user_no']=xnr_user_no
#         event_warming_content['validity']=0
#         event_warming_content['timestamp']=today_datetime
#         now_time=int(time.time())
#         task_id=xnr_user_no+'_'+str(now_time) 
        
#         if event_sensitive_count > 0:
#             #写入数据库           
#             if write_mark:
#                 mark=write_envent_warming(today_datetime,event_warming_content,task_id)
#                 event_warming_list.append(mark)
#             else:
#                 event_warming_list.append(event_warming_content)
#         else:
#             pass
#     return event_warming_list


# def write_envent_warming(today_datetime,event_warming_content,task_id):
#     weibo_event_warning_index_name=weibo_event_warning_index_name_pre+ts2datetime(today_datetime)
#     print 'weibo_event_warning_index_name:',weibo_event_warning_index_name
#     #try:
#     es_xnr.index(index=weibo_event_warning_index_name,doc_type=weibo_event_warning_index_type,body=event_warming_content,id=task_id)
#     mark=True
#     #except:
#     #    mark=False
#     return mark

# #粉丝或关注用户判断
# def judge_user_type(uid,user_list):
#     if uid in user_list:
#         mark=1.2
#     else:
#         mark=0.8
#     return mark

# def union_dict(*objs):
#     #print 'objs:', objs[0]
#     _keys=set(sum([obj.keys() for obj in objs],[]))
#     _total={}

#     for _key in _keys:
#         _total[_key]=sum([int(obj.get(_key,0)) for obj in objs])

#     return _total





#facebook预警内容组织
def create_facebook_warning():
    #时间设置
    if S_TYPE == 'test':
        test_day_date=FACEBOOK_FLOW_START_DATE
        today_datetime=datetime2ts(test_day_date) - DAY
        start_time=today_datetime
        end_time=today_datetime
        operate_date=ts2datetime(start_time) 
    else:
        now_time=int(time.time())
        today_datetime=datetime2ts(ts2datetime(now_time)) - DAY 
        start_time=today_datetime    #前一天0点
        end_time=today_datetime          #定时文件启动的0点
        operate_date=ts2datetime(start_time)

    account_list=get_user_account_list()
    for account in account_list:
        #xnr_list=get_user_xnr_list(account)
        #print xnr_list
        xnr_list=['FXNR0001']
        for xnr_user_no in xnr_list:
            #人物行为预警
            personal_mark=create_personal_warning(xnr_user_no,today_datetime)
            #言论内容预警
            speech_mark=create_speech_warning(xnr_user_no,today_datetime)
            speech_mark=True
            #事件涌现预警
            #create_event_warning(xnr_user_no,today_datetime,write_mark=True)

    #时间预警
    date_mark=create_date_warning(today_datetime)

    return True


if __name__ == '__main__':
    create_facebook_warning()



# if __name__ == '__main__':
#     xnr_user_no='FXNR0001'
#     today_datetime=datetime2ts(FACEBOOK_FLOW_START_DATE)
#     print today_datetime
#     for i in range(0,30):
#         datetime=today_datetime+i*DAY
#         create_speech_warning(xnr_user_no,datetime)