#-*-coding:utf-8-*-

from global_utils import es_user_profile,profile_index_name,profile_index_type,\
                        es_xnr,weibo_xnr_index_name,weibo_xnr_index_type
from parameter import MAX_SEARCH_SIZE

def nickname2uid(nickname_list):
    uids_list = set()
    query_body = {
        'query':{
            'filtered':{
                'filter':{
                    'terms':{'nick_name':nickname_list}
                }
            }
        },
        'size':MAX_SEARCH_SIZE
    }

    es_results = es_user_profile.search(index=profile_index_name,doc_type=profile_index_type,\
                    body=query_body)['hits']['hits']
    print 'es_results:::',es_results
    if es_results:
        for result in es_results:
            result = result['_source']
            uid = result['uid']
            uids_list.add(uid)
    uids_list = list(uids_list)
    print 'uids_list::',uids_list
    return uids_list

def uid2nick_name_photo(uid):
    uname_photo_dict = {}
    try:
        user = es_user_profile.get(index=profile_index_name,doc_type=profile_index_type,id=uid)['_source']
        nick_name = user['nick_name']
        photo_url = user['photo_url']
    except:
        nick_name = ''
        photo_url = ''
        
    return nick_name,photo_url


def user_no2_id(user_no):
    task_id = 'WXNR'+str('%04d'%user_no)  #五位数 WXNR0001
    return task_id

def _id2user_no(task_id):
    user_no_string = filter(str.isdigit,task_id)
    print 'user_no_string::',user_no_string
    user_no = int(user_no_string)
    print 'user_no::',user_no
    return user_no

def xnr_user_no2uid(xnr_user_no):
    try:
        result = es_xnr.get(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,id=xnr_user_no)['_source']
        uid = result['uid']
    except:
        uid = ''

    return uid

def uid2xnr_user_no(uid):
    try:
        query_body = {
            'query':{
                'term':{'uid':uid}
            }
        }
        result = es_xnr.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']
        xnr_user_no = result[0]['xnr_user_no']
    except:
        xnr_user_no = ''

    return xnr_user_no