#-*- coding:utf-8 -*-
'''
use to save parameter
'''

#for all
DAY = 24*3600
Fifteen = 60 * 15
HALF_HOUR = 1800
HOUR = 3600
FOUR_HOUR = 3600*4
MAX_VALUE = 999
WEEK = 7
WEEK_TIME = 7*24*3600
MONTH = 30
MONTH_TIME = 30*24*3600
EXPIRE_TIME = 8*24*3600
DAY_HOURS = 24  # 一天24小时
FLOW_TEXT_START_DATE = 1502553600 # 2017-08-13
USER_NUM = 50 #人物行为预警返回用户数量
USER_CONTENT_NUM=50 #人物行为预警每个用户返回的敏感微博数量最大值
REMIND_DAY=15  #今日提醒中，对时间节点的提前天数
WARMING_DAY=15 #时间预警，预警天数
MAX_WARMING_SIZE=100 #最大预警数目
EVENT_COUNT=20 #实时计算事件频率阈值
EVENT_OFFLINE_COUNT=80 #离线计算事件预警数量
FOLLOWER_INFLUENCE_MAX_JUDGE=1.5 #预警中关注者、粉丝权重增加影响力倍数
NOFOLLOWER_INFLUENCE_MIN_JUDGE=1 #预警中非关注者影响力值降低倍数
#xnr
USER_XNR_NUM=50 #用户管理虚拟人数量
# weibo
SPEECH_WARMING_NUM=50 #言论预警数量
HOT_WEIBO_NUM=50 #热门帖子、热门用户数量
INFLUENCE_MIN=1 #影响力阈值

MAX_DETECT_COUNT = 900
MAX_FLOW_TEXT_DAYS = 7 ## 最多查询最近多少天的流数据
TOP_KEYWORDS_NUM = 20  ## 最常用的关键词的数量
MAX_SEARCH_SIZE = 999 ## 从数据库中最大检索返回数量
MAX_HOT_POST_SIZE = 200 #热门帖子未筛选前返回最大数量

#社区发现
MAX_TARGET_USER_NUM=100000 #种子用户最大数量
MAX_CACULATE_USER_NUM=200000 #种子用户计算最大数量

SORT_FIELD = 'timestamp'
TOP_WEIBOS_LIMIT = 20

TOP_WEIBOS_LIMIT_DAILY = 20
TOP_ACTIVE_SOCIAL = 20

ACTIVE_TIME_TOP = 6
DAILY_INTEREST_TOP_USER = 100
NICK_NAME_TOP = 10
USER_LOCATION_TOP = 10
DESCRIPTION_TOP = 10
MONITOR_TOP_USER = 100

DAILY_AT_RECOMMEND_USER_TOP = 10

HOT_EVENT_TOP_USER = 100
HOT_AT_RECOMMEND_USER_TOP = 10

SENSITIVE_TOP_USER = 100
SENSITIVE_AT_RECOMMEND_USER_TOP = 10

BCI_USER_NUMBER = 1000
USER_POETRAIT_NUMBER = 200

## 实例模板：top活跃的时间段
TOP_ACTIVE_TIME = 3

## 随机转发 起止时间 5min- 60min
RETWEET_START_TS = 60*5  # 取决于定时扫描最小间隔
RETWEET_END_TS = 60*60

## 随机转发跟踪uid
TRACE_FOLLOW_LIST = ['5622091306','5650736291','3738565314','5489151972']

# 子观点微博条数限制
SUB_OPINION_WEIBO_LIMIT = 3

# top心理特征
TOP_PSY_FEATURE = 4

## 读取hashtag
UID_TXT_PATH = '/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/weibo_xnr_warming'

## 生成实例模板
EXAMPLE_MODEL_PATH = '/home/ubuntu8/yumingming/xnr1/xnr/example_model/'

# 主动社交，朋友圈推荐，weibo_user库中 friend_list字段
FRIEND_LIST = ['3077463611','3925294372','1666458704','1663088660','3605949192','3700715461','5664244064','5764699905','2567277481']

FOLLOWERS_LIST = ['5664244064','3925294372','2702763965','3077463611']

## 行为评估
PORTRAIT_UID_LIST = ['2964470873','1885229780','1628587977','2575596064','5313413396']
PORTRAI_UID = '5078684428'

# 安全性评估 -- 今日关注人群
FOLLOWERS_TODAY = ['1885229780','5313413396','3210602114']

## 渗透力和安全性（活跃程度）评估 top 依据
TOP_ASSESSMENT_NUM = 500

## 2016-11-19 用户
ACTIVE_UID = '2919766227'

## 影响力评估参数设置
#MAX_FANS = 100
#MAX_LIKE = 50000
#MAX_PRIVATE = 100
#MAX_AT = 1000

WHITE_UID_PATH = '/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/'

WHITE_UID_FILE_NAME = 'white_uid.txt'

IMAGE_PATH = '/home/ubuntu8/yumingming/xnr1/xnr/weibo_images/'

DOMAIN_ABS_PATH = '/home/ubuntu8/huxiaoqian/user_portrait_151220/user_portrait/user_portrait/cron/model_file/domain'

CH_ABS_PATH = '/home/ubuntu8/huxiaoqian/user_portrait_151220/user_portrait/user_portrait/cron/model_file/character'

TOPIC_ABS_PATH = "/home/ubuntu8/huxiaoqian/user_portrait_151220/user_portrait/user_portrait/cron/model_file/topic"

PSY_ABS_PATH = "/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/cron/model_file/psy"

POLICY_ABS_PATH = '/home/ubuntu8/yuanhuiru/xnr/xnr1/xnr/cron/knowledge_base_management/political'

#FB & TW 属性计算
FB_DOMAIN_ABS_PATH = '/home/ubuntu8/hanmc/666/xnr1/xnr/cron/topic_domain_facebook_twitter_v1/domain_facebook'
TW_DOMAIN_ABS_PATH = '/home/ubuntu8/hanmc/666/xnr1/xnr/cron/topic_domain_facebook_twitter_v1/domain_twitter'
FB_TW_TOPIC_ABS_PATH = '/home/ubuntu8/hanmc/666/xnr1/xnr/cron/topic_domain_facebook_twitter_v1/topic'

MID_VALUE = 500      #查询活跃用户数量

MAX_VALUE = 9999

SENTIMENT_DICT_NEW = {'0':u'中性', '1':u'积极', '2':u'生气', '3':'焦虑', \
         '4':u'悲伤', '5':u'厌恶', '6':u'消极其他', '7':u'消极'}

daily_ch2en = {u'旅游':'travel',u'美食':'food',u'汽车':'cars',u'游戏':'games',\
            u'星座':'constellation',u'音乐':'music',u'影视':'movie',\
            u'健身':'fitness',u'养生':'health',u'体育':'sports',\
            u'萌宠':'pets',u'动漫':'cartoon',u'时尚':'fashion',\
            u'鸡汤':'soul'}

topic_value_dict = {"art": 1, "computer":2, "economic":7, "education":7.5, "environment":8.7, "medicine":7.8,"military":7.4, "politics":10, "sports":4, "traffic":6.9, "life":1.8, "anti-corruption":9.5, "employment":6, "fear-of-violence":9.3, "house":6.4, "law":8.6, "peace":5.5, "religion":7.6, "social-security":8.6}

topic_en2ch_dict = {'art':u'文体类_娱乐','computer':u'科技类','economic':u'经济类', \
                    'education':u'教育类','environment':u'民生类_环保', 'medicine':u'民生类_健康',\
                    'military':u'军事类','politics':u'政治类_外交','sports':u'文体类_体育',\
                    'traffic':u'民生类_交通','life':u'其他类','anti-corruption':u'政治类_反腐',\
                    'employment':u'民生类_就业','fear-of-violence':u'政治类_暴恐',\
                    'house':u'民生类_住房','law':u'民生类_法律','peace':u'政治类_地区和平',\
                    'religion':u'政治类_宗教','social-security':u'民生类_社会保障'}
topic_ch2en_dict = {u'文体类_娱乐': 'art', u'科技类':'computer', u'经济类':'economic', \
                    u'教育类':'education', u'民生类_环保': 'environment', u'民生类_健康':'medicine',\
                    u'军事类': 'military', u'政治类_外交':'politics', u'文体类_体育':'sports',\
                    u'民生类_交通':'traffic', u'其他类':'life', u'政治类_反腐':'anti-corruption',\
                    u'民生类_就业':'employment', u'政治类_暴恐':'fear-of-violence',\
                    u'民生类_住房': 'house', u'民生类_法律':'law', u'政治类_地区和平':'peace',\
                    u'政治类_宗教':'religion', u'民生类_社会保障':'social-security'}
                    
domain_ch2en_dict = {u'高校': 'university', u'境内机构':'homeadmin', u'境外机构':'abroadadmin' ,\
                     u'媒体': 'homemedia', u'境外媒体': 'abroadmedia', u'民间组织': 'folkorg', \
                     u'法律机构及人士': 'lawyer', u'政府机构及人士':'politician', u'媒体人士':'mediaworker',\
                     u'活跃人士': 'activer', u'草根': 'grassroot', u'其他':'other', u'商业人士':'business'}                    

domain_en2ch_dict = {'university':u'高校', 'homeadmin':u'境内机构', 'abroadadmin':u'境外机构', \
                     'homemedia':u'媒体', 'abroadmedia':u'境外媒体', 'folkorg':u'民间组织',\
                     'lawyer':u'法律机构及人士', 'politician':u'政府机构及人士', 'mediaworker':u'媒体人士',\
                     'activer':u'活跃人士', 'grassroot':u'草根', 'other':u'其他', 'business':u'商业人士'}   

task_source_ch2en = {u'日常发帖':'daily_post',u'热门发帖':'hot_post',u'业务发帖':'business_post',\
                    u'跟随转发':'trace_post',u'智能发帖':'intel_post'}

#facebook
fb_domain_ch2en_dict = {u'高校':'university',u'机构':'admin',u'媒体':'media',u'民间组织':'folkorg',\
                        u'法律机构及人士':'lawyer',u'政府机构及人士':'politician',u'媒体人士':'mediaworker',\
                        u'活跃人士':'activer',u'其他':'other',u'商业人士':'business'}
                        
fb_domain_en2ch_dict = {'university':u'高校','admin':u'机构','media':u'媒体',\
                        'folkorg':u'民间组织','lawyer':u'法律机构及人士','politician':u'政府机构及人士',\
                        'mediaworker':u'媒体人士','activer':u'活跃人士','other':u'其他','business':u'商业人士'}               

#facebook&twitter
fb_tw_topic_en2ch_dict = {'life':u'其他类','law':u'民生类_法律','computer':u'科技类','house':u'民生类_住房',\
                        'peace':u'政治类_地区和平','politics':u'政治类_民主','fear-of-violence':u'政治类_暴恐',\
                        'sports':u'文体类_体育','environment':u'民生类_环保','religion':u'政治类_宗教',\
                        'economic':u'经济类','traffic':u'民生类_交通','anti-corruption':u'政治类_反腐',\
                        'military':u'军事类','medicine':u'民生类_健康','art':u'文体类_娱乐',\
                        'education':u'教育类','employment':u'民生类_就业','social-security':u'民生类_社会保障'}

fb_tw_topic_ch2en_dict={'其他类':u'life','民生类_法律':u'law','科技类':u'computer','民生类_住房':u'house',\
                        '政治类_地区和平':u'peace','政治类_民主':u'politics','政治类_暴恐':u'fear-of-violence',\
                        '文体类_体育':u'sports','民生类_环保':u'environment','政治类_宗教':u'religion',\
                        '经济类':u'economic','民生类_交通':u'traffic','政治类_反腐':u'anti-corruption',\
                        '军事类':u'military','民生类_健康':u'medicine','文体类_娱乐':u'art',\
                        '教育类':u'education','民生类_就业':u'employment','民生类_社会保障':u'social-security',}
# 敏感词等级评分, string类型
sensitive_score_dict = {
    "1": 1,
    "2": 5,
    "3": 10
}                 
                   
# qq
group_message_windowsize = 30          # 群历史消息查询范围30天
LOCALHOST_IP = '127.0.0.1'
