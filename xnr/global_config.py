# -*- coding: utf-8 -*-
'''
use to save database information
'''
import os
import time

#use to mark type:  run or test
S_TYPE = 'test'   #test/run
S_DATE = '2016-11-20' #when type=test, now_date=S_DATE
S_UID = '1910774981' #'3986246393'
S_DATE_BCI = '2016-11-27'
S_DATE_EVENT_WARMING = '2016-11-28'

QQ_S_DATE = '2017-07-12'
QQ_S_DATE_NEW = '2017-08-25'
QQ_S_DATE_ASSESSMENT = '2017-09-28'
QQ_GROUP_MESSAGE_START_DATE = '2017-08-23'
QQ_GROUP_MESSAGE_START_DATE_ASSESSMENT = '2017-09-28'


XNR_CENTER_DATE_TIME=int(time.time())      #当前时间


PATH_ROOT = os.path.dirname(os.path.abspath(__file__)) 

#config es
#config xnr user info
ES_CLUSTER_HOST = ['219.224.134.213:9205', '219.224.134.214:9205',\
                   '219.224.134.215:9205']
ES_CLUSTER_PORT = '9205'
#config flow text info
ES_FLOW_TEXT_HOST = ['219.224.134.216:9201', '219.224.134.217:9201',\
                          '219.224.134.218:9201']
ES_FLOW_TEXT_PORT = '9201'

# need three ES identification 
USER_PROFILE_ES_HOST = ['10.128.55.81','10.128.55.82','10.128.55.83']
USER_PROFILE_ES_PORT = 9200

#config user portrat
ES_USER_PORTRAIT_HOST = ['219.224.134.216:9201', '219.224.134.217:9201',\
                     '219.224.134.218:9201']
ES_USER_PORTRAIT_PORT = '9201'

#es_path
ES_PATH = '/home/ubuntu8/huxiaoqian/elasticsearch-1.6.0/'

#config redis
REDIS_HOST = '219.224.134.212'
REDIS_PORT = '7392'

REDIS_CLUSTER_HOST_FLOW2 = '219.224.134.213'
REDIS_CLUSTER_PORT_FLOW2 = '6666'

#redis_path
REDIS_PATH = '/home/ubuntu7/huxiaoqian/redis-3.0.5/7392/'

# use to identify the db number of redis-97
R_BEGIN_TIME = '2016-03-21'

##　 weibo敏感词redis
REDIS_CLUSTER_HOST_FLOW3 = '219.224.134.214' #'10.128.55.71'
REDIS_CLUSTER_PORT_FLOW3 = '6379'

REDIS_HOST_SENSITIVE = '219.224.134.212' #'10.128.55.68'
REDIS_PORT_SENSITIVE = '6381' #'6379'

#wx redis
REDIS_WX_PORT = 6660
REDIS_WX_HOST = '219.224.134.213'

#使用七牛来存储捕获到的图片
qiniu_access_key = "2QHQTgGYH8Ow3dy1jpuSKLAlTo-ZkRav1ty2Nok8"
qiniu_secret_key = "Q91z6hnj5H0LaRkbAN8IPdc8dypdAQ_n21S8tEcu"
qiniu_bucket_name = "publicbucket"
qiniu_bucket_domain = "ovorc2c4c.bkt.clouddn.com"

#wx
WX_S_DATE = '2017-10-25'
WX_S_DATE_NEW = '2017-10-25'
WX_S_DATE_ASSESSMENT = '2017-10-25'
WX_GROUP_MESSAGE_START_DATE = '2017-10-25'
WX_GROUP_MESSAGE_START_DATE_ASSESSMENT = '2017-10-25'