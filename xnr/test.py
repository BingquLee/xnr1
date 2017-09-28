#-*- coding:utf-8 -*-
import os
import time
import random
import json
import sys
import base64
from global_utils import es_xnr as es,r
from global_utils import es_user_portrait,portrait_index_name,portrait_index_type
from global_utils import weibo_xnr_index_name,weibo_xnr_index_type,\
                        weibo_xnr_fans_followers_index_name,weibo_xnr_fans_followers_index_type
from textrank4zh import TextRank4Keyword, TextRank4Sentence

# icon = open('./weibo_images/zhengyidang.png','rb')
# iconData = icon.read()
# iconData = base64.b64encode(iconData)
# print 'icondata:::',iconData

# imgData = base64.b64decode(iconData)
# time_name = time.strftime('%Y%m%d%H%M%S')
# random_name = time_name + '_%d' % random.randint(0,100)
# leniyimg = open('./'+random_name+'.jpg','wb')
# leniyimg.write(imgData)
# leniyimg.close()
#     

# query_body = {
#     'query':{
#         'match_all':{}
#     },
#     'size':20,
#     'sort':{'sensitive':{'order':'desc'}}
# }
# results = es_user_portrait.search(index=portrait_index_name,doc_type=portrait_index_type,body=query_body)['hits']['hits']


# for result in results:
    
#     print result['_source']['sensitive']

# query_body= {
#     'query':{
#         'term':{'xnr_user_no':'WXNR0004'}
#     }
# }

# query_body= {
#     'query':{
#         'match_all':{}
#     }
# }


# result = es.search(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
#     body=query_body)['hits']['hits']
# print 'result::',result

# with open("./fans_followers.json","w") as dump_f:
#     for item in result:
#         json.dump(item,dump_f)
#         print '@'

# follow_list = result[0]['_source']['followers_list']

# follow_list = list(set(follow_list))

# es.update(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
#     id='WXNR0004',body={'doc':{'trace_follow_list':follow_list,'followers_list':follow_list}})

# with open("./fans_followers.json","r") as load_f:
#     #print 'load_f::',load_f
#     load_dict = json.load(load_f)
#     print load_dict
#     es.index(index=weibo_xnr_fans_followers_index_name,doc_type=weibo_xnr_fans_followers_index_type,\
#         id='WXNR0004',body=load_dict['_source'])

# # query_body = {
# #     'query':{
# #         'term':{'xnr_user_no':['WXNR00004']}
# #     }
# # }

# results = es.search(index=weibo_xnr_index_name,doc_type=weibo_xnr_index_type,body=query_body)['hits']['hits']

# print 'results::',results

#es.delete(index='recommend_subopinion_keywords_task',doc_type='keywords_task',id='WXNR0004_4043525244676524')
# es.delete(index='weibo_domain',doc_type='group',id='AV6396lYQIwrAS0usE0H')
# es.delete(index='weibo_domain',doc_type='group',id='AV64pqMhS8CBAF2ZGzdS')
# es.delete(index='weibo_domain',doc_type='group',id='AV63955tS8CBAF2ZGzdO')
# es.delete(index='weibo_domain',doc_type='group',id='wei_quan_qun_ti')

#es.delete(index='weibo_xnr',doc_type='user',id='WXNR0014')
# print r.sadd('qq_group_set_01',['121567','5674567'])
# m = r.smembers('qq_group_set_01')
# if "123123123" in m:
# 	print '1111'

es.delete(index='weibo_example_model',doc_type='model',id='min_yun_ren_shi_grassroot')
es.delete(index='weibo_example_model',doc_type='model',id='null_min_yun_ren_shi_grassroot')
es.delete(index='weibo_example_model',doc_type='model',id='WXNR0004_min_yun_ren_shi_grassroot')
# es.delete(index='recommend_subopinion_keywords_task',doc_type='keywords_task',id='WXNR0004_4043525622087918')
# es.delete(index='recommend_subopinion_keywords_task',doc_type='keywords_task',id='WXNR0004_4043433776005723')
# es.delete(index='recommend_subopinion_keywords_task',doc_type='keywords_task',id='WXNR0004_4043274014747152')
# es.delete(index='qq_xnr',doc_type='user',id='QXNR0003')
# es.delete(index='qq_xnr',doc_type='user',id='QXNR0005')
# es.delete(index='qq_xnr',doc_type='user',id='QXNR0006')
#es.update(index='weibo_domain',doc_type='group',id='wei_quan_qun_ti',body={'doc':{'xnr_user_no':'WXNR0004'}})

# def main(w_text):

#     tr4w = TextRank4Keyword()
#     tr4w.analyze(text=w_text, lower=True, window=4)
#     k_dict = tr4w.get_keywords(5, word_min_len=2)
#     for item in k_dict:
#         print item.weight,item.word.encode('utf-8')

#     return k_dict

# if __name__ == '__main__':

#     m = main('李钟硕&帅&发型&心&天网&画报&5959&眼神&VEDI&截图&花絮&初吻&代言&七次&VERO&c&少女&说话&相思&rabbit&镜头&对视&期间&cosmopolitankorea&中旬&钟硕&出新&感动&天际&应该&感觉&style&代表&身体&难解&刘海&光日&cosmopolitan&加油&性感&暖暖&发布会&以来&抱抱&还好&期待&无敌&好帅&以前&d')
#     print m[0].word.encode('utf-8')


