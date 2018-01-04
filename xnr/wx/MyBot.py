#-*- coding: utf-8 -*-
from wxpy import *
import os
import json
import random
import time
import hashlib
import datetime
import socket
import threading
import subprocess
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from xnr.global_utils import es_xnr, wx_xnr_index_name, wx_xnr_index_type, wx_xnr_history_count_index_name, \
                        wx_xnr_history_count_index_type, wx_group_message_index_name_pre, wx_group_message_index_type, \
                        r_wx as r, wx_xnr_data_path, wx_xnr_qrcode_path, wx_sent_group_message_index_name_pre
from xnr.global_config import qiniu_access_key, qiniu_secret_key, qiniu_bucket_name, qiniu_bucket_domain, WX_IMAGE_ABS_PATH, WX_VOICE_ABS_PATH
from xnr.parameter import LOCALHOST_IP, DAY
from xnr.utils import user_no2wxbot_id, wxbot_id2user_no
from xnr.time_utils import ts2datetime, datetime2ts
from xnr.wx_xnr_groupmessage_mappings import wx_group_message_mappings
from sensitive_compute import sensitive_check

class MyBot(Bot):
    #继承Bot()，以便加入更多属性
    def __init__(self, wxbot_id, wxbot_port,  init_groups_list=None, if_enable_puid=True, if_cache_path=False, if_console_qr=False, if_login_callback=None, if_logout_callback=True):
        self.wxbot_id = wxbot_id
        self.wxbot_port = wxbot_port
        self.init_groups_list = init_groups_list
        self.if_enable_puid = if_enable_puid
        self.if_cache_path = if_cache_path
        self.if_console_qr = if_console_qr
        self.if_login_callback = if_login_callback
        self.if_logout_callback = if_logout_callback
        self.puid_path = None
        self.qr_path = None
        self.console_qr =False
        self.cache_path = None
        self.qr_callback = None
        self.login_callback = None
        self.data_path = os.path.join(os.getcwd(), wx_xnr_data_path)
        self.logger = None  #负责将相关信息log等发送到微信监管群中, 有bug
        self.qiniu = Auth(qiniu_access_key, qiniu_secret_key)
        self.groups_list = []  #需要监听的群组的puid
        self.status = None  #记录wxbot的登陆、listen状态等

        #开启缓存登录
        if self.if_cache_path:
            self.cache_path = os.path.join(self.data_path, self.wxbot_id + '.pkl')
        #登录方式
        if self.if_console_qr:  
            #使用控制台二维码登陆
            self.console_qr = True
        else:   
            #使用二维码图片登陆
            self.qr_path = os.path.join(os.path.join(os.getcwd(), wx_xnr_qrcode_path), self.wxbot_id + '_' + hashlib.md5(str(int(time.time()))).hexdigest() + '_qrcode.png')
            if os.path.isfile(self.qr_path):    #确保上次登录使用的二维码图片被清除掉
                os.remove(self.qr_path)
            self.change_wxxnr_redis_data({'qr_path':self.qr_path})
            self.qr_callback = self.my_qr_callback
        if self.if_login_callback:
            self.login_callback = self.my_login_callback
        if self.if_logout_callback:
            self.if_logout_callback = self.my_logout_callback
        #初始化需要监听的群组
        if self.init_groups_list:
            for group_puid in self.init_groups_list.split(','):
                self.groups_list.append(group_puid)
        
        #登陆
        print 'starting %s ...' % self.wxbot_id
        print 'before login'
        print self.cache_path
        print self.console_qr
        print self.qr_path
        Bot.__init__(self, self.cache_path, self.console_qr, self.qr_path, self.qr_callback, self.login_callback, self.if_logout_callback)
        print 'after login' #如果此条没有打印出来，多半是该账号网页版被封了……
        #还可能是因为certifi==2015.04.28被替换掉了

        #启用puid
        if self.if_enable_puid:
            self.puid_path = os.path.join(self.data_path,self.wxbot_id + '_puid.pkl')
            print 'self.puid_path: ', self.puid_path
            self.enable_puid(self.puid_path)
        #注册群消息处理函数
        @self.register(Group)
        def proc_group_msg(msg):
            self.proc_msg(msg)
        #登陆成功后更改存放在redis中的wxbot数据
        self.change_status('logined')
        self.change_wxxnr_redis_data({'puid':self.self.puid, 'nickname':self.self.name, 'groups_list':self.groups_list})
        #如果已经登陆成功了，但是二维码图片不存在，说明使用了缓存登陆。但是这样的话，正常扫描二维码登陆后也会是这种情况，不过结果没啥影响。
        if not os.path.isfile(self.qr_path):
            print 'loginedwithcache：file not exist'
            self.change_wxxnr_redis_data({'qr_path':'loginedwithcache'})
        else:
            size = os.path.getsize(self.qr_path)
            if not size :
                print 'loginedwithcache: file size is zero'
                self.change_wxxnr_redis_data({'qr_path':'loginedwithcache'})
        #保存bot基本信息到es中
        self.save_bot_info()
        #创建时默认设置监听所有的群组
        self.set_default_groups()

    def my_qr_callback(self, **kwargs):
        print 'trying to save qrcode picture'
        with open(self.qr_path, 'wb') as fp:
            fp.write(kwargs['qrcode'])
        #可以将二维码图片发送到邮箱之类的, 但是登陆也可能会使用缓存登陆，不一定会产生新的二维码图片
        print 'save qrcode picture'
    
    def my_login_callback(self, **kwargs):
        d = r.get(self.wxbot_id)
        if d:
            data = eval(d)
            data['status'] = 'logined'
            r.set(self.wxbot_id, data)
        else:
            r.set(self.wxbot_id, {'status': 'logined'})

    def my_logout_callback(self, **kwargs):
        self.change_status('logout')    #设置self.status字段，以便别处自动判断是否应该关闭socket端口
        #send mail to admin ?
        
    def enable_logger(self, group_name):
        try:
            group_receiver = ensure_one(self.groups(update=True).search(group_name))
            self.logger = get_wechat_logger(group_receiver)
        except Exception,e:
            print e

    def change_wxxnr_redis_data(self, xnr_data={}):
        d = r.get(self.wxbot_id)
        data = {}
        if d:
            data = eval(d)
        for key,value in xnr_data.items():
            data[key] = value   #如果存在key则更改数据为value,不存在key则增加数据value
        return r.set(self.wxbot_id, data)

    def change_status(self, status):
        self.status = status
        return self.change_wxxnr_redis_data({'status': status}) #更改redis里面wxbot的status信息

    def save_bot_info(self):
        while True:
            d = r.get(self.wxbot_id)
            if d:
                try:
                    wx_id = eval(d)['wx_id']
                    wxbot_port = eval(d)['wxbot_port']
                    submitter = eval(d)['submitter']
                    mail = eval(d)['mail']
                    access_id = eval(d)['access_id']
                    remark = eval(d)['remark']
                    break
                except Exception,e:
                    print e
        #check if already exist
        query_body_wx_exist={'query':{'term':{'wx_id':wx_id}}}
        search_result = es_xnr.search(index=wx_xnr_index_name,doc_type=wx_xnr_index_type, body=query_body_wx_exist)['hits']['hits']
        if search_result:
            #更改xnr信息并保存到es中
            pass
        else:
            print 'save_bot_info'
            wxxnr_data = {
                'wx_id': wx_id,
                'puid': self.self.puid,
                'user_no': wxbot_id2user_no(self.wxbot_id),
                'xnr_user_no': self.wxbot_id,
                'wxbot_port': wxbot_port,
                'create_ts': int(time.time()),
                'nickname': self.self.name,
                'remark': remark,
                'submitter': submitter,
                'mail': mail,
                'access_id': access_id
            }
            es_xnr.index(index=wx_xnr_index_name, doc_type=wx_xnr_index_type, id=self.wxbot_id, body=wxxnr_data)

    def set_default_groups(self):
        try:
            d = r.get(self.wxbot_id)
            if d:
                data = eval(d)
                create_flag = data['create_flag']
                if create_flag:
                    group_list = []
                    groups = self.groups(update=True)
                    for group in groups:
                        #load members details
                        group.update_group(members_details=True)
                        group_list.append(group.puid)
                    if self.set_groups(group_list):
                        if self.change_wxxnr_redis_data({'create_flag': 0}):
                            return 1
                else:
                    return 1
        except Exception,e:
            print e
        return 0

    def save_sent_msg(self, m, to_puid, to_name):
        data = {
            'msg_type': m.type,
            'text': m.text,
            'timestamp': int(time.mktime(m.create_time.timetuple())),
            'xnr_id': self.self.puid, 
            'xnr_name': self.self.name, 
            'group_id': to_puid, 
            'group_name': to_name,
            'speaker_id': self.self.puid, 
            'speaker_name': self.self.name
        }
        nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
        #虚拟人发送的消息在wx_sent_group_message中存一份
        sent_index_name = wx_sent_group_message_index_name_pre + str(nowDate)
        if not es_xnr.indices.exists(index=sent_index_name):
            print 'get mapping'
            print wx_group_message_mappings(sent_index_name)
        print es_xnr.index(index=sent_index_name, doc_type=wx_group_message_index_type, body=data)
        #虚拟人发送的消息在wx_group_message中再存一份
        index_name = wx_group_message_index_name_pre + str(nowDate)
        if not es_xnr.indices.exists(index=index_name):
            print 'get mapping'
            print wx_group_message_mappings(index_name)
        print es_xnr.index(index=index_name, doc_type=wx_group_message_index_type, body=data)
        

    def proc_msg(self, msg):
        group_puid = msg.sender.puid
        if group_puid in self.groups_list:
            msg_type = msg.type
            save_flag = 0
            data = {}
            if msg_type in ['Text','Picture', 'Recording']:
                save_flag = 1
                data = {
                    'xnr_id': self.self.puid, 
                    'xnr_name': self.self.name, 
                    'group_id': group_puid, 
                    'group_name': msg.sender.name,
                    'timestamp': msg.raw['CreateTime'],
                    'speaker_id': msg.member.puid,
                    'speaker_name': msg.member.name,
                    'msg_type': msg_type
                }
                nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
                index_name = wx_group_message_index_name_pre + str(nowDate)
            if msg_type == 'Text':
                text = msg.text
                data['text'] = text
                try:
                    sen_value, sen_words = sensitive_check(text.encode('utf8')) 
                    if sen_value !=0:
                        sen_flag = 1    #该条信息是敏感信息
                    else:
                        sen_flag = 0
                    if msg.is_at:
                        at_flag = 1     #被@到
                    else:
                        at_flag = 0
                    data['at_flag'] = at_flag
                    data['sensitive_flag'] = sen_flag
                    data['sensitive_value'] = sen_value
                    data['sensitive_words_string'] = sen_words['sensitive_words_string']
                except Exception,e:
                    print e
            elif msg_type == 'Picture':
                '''
                #保存到七牛（已弃用，2018-1-2，hanmc）
                try:
                    #save picture
                    filename = str(msg.id) + '.png'
                    filepath = os.path.join(self.data_path, filename)
                    msg.get_file(filepath)
                    #upload picture to qiniu.com
                    token = self.qiniu.upload_token(qiniu_bucket_name, filename, 3600)
                    ret, info = put_file(token, filename, filepath,)
                    data['text'] = qiniu_bucket_domain + '/' + filename 
                    os.remove(filepath)
                except Exception,e:
                    print e
                '''
                #保存到本地
                filename = str(msg.id) + '.png'
                filepath = os.path.join(WX_IMAGE_ABS_PATH, ts2datetime(time.time()))
                if not os.path.isdir(filepath):
                    os.mkdir(filepath)
                    remove_wx_media_old_files(WX_IMAGE_ABS_PATH, period=30)
                msg.get_file(save_path = os.path.join(filepath, filename))
                data['text'] = os.path.join(filepath, filename)
            elif msg_type == 'Recording':
                filename = str(msg.id) + '.mp3'
                filepath = os.path.join(WX_VOICE_ABS_PATH, ts2datetime(time.time()))
                if not os.path.isdir(filepath):
                    os.mkdir(filepath)
                remove_wx_media_old_files(WX_VOICE_ABS_PATH, period=30)
                print msg.get_file(save_path = os.path.join(filepath, filename))
                data['text'] = os.path.join(filepath, filename)
            #存储msg到es中
            if save_flag : 
                if not es_xnr.indices.exists(index=index_name):
                    print 'get mapping'
                    print wx_group_message_mappings(index_name)
                print es_xnr.index(index=index_name, doc_type=wx_group_message_index_type, body=data)
            #自动回复监听的群组中@自己的消息
            if msg.is_at:
                time.sleep(random.random())
                m = msg.reply(u'知道啦~')
                self.save_sent_msg(m=m, to_puid=msg.sender.puid, to_name=msg.sender.name)

    def load_all_groups(self):
        groups = self.groups(update=True)
        data = []
        for group in groups:
            data.append((group.puid, group.name))
        return data

    def set_groups(self, group_list):        
        #注册监听群消息的函数, group_list是需要监听消息的群组的puid列表
        if group_list:  #['']也是True
            #判断下传过来的groups_list是否有误
            try:
                groups_nickname = []
                if group_list == ['']:
                    group_list = []
                else:
                    for group_puid in group_list:
                        gs = self.groups(update=True).search(puid=group_puid)
                        if not gs:
                            return 0
                        groups_nickname.append(gs[0].name)
                self.groups_list = group_list
                print 'MyBot: set_groups: self.groups_list: ', self.groups_list
                groups_data = {
                    'wx_groups_num': len(groups_nickname),
                    'wx_groups_nickname': groups_nickname,
                    'wx_groups_puid': self.groups_list
                }
                self.change_wxxnr_redis_data({'groups_list': ','.join(self.groups_list)})
                es_xnr.update(index=wx_xnr_index_name,doc_type=wx_xnr_index_type,id=self.wxbot_id, body={'doc':groups_data})
            except Exception,e:
                print e
                return 0
        return 1

    def bot_logout(self):
        try:
            if self.alive:
                self.logout()
            return 1
        except Exception,e:
            print e
            return 0

    def load_group_members(self, puid):
        data = []
        for member in ensure_one(self.search(puid=puid)).members:
            data.append((member.puid, member.name))
        return data

    def send_msg_by_puid(self, puids, msg):
        for puid in puids:
            if not self.send_single_msg_by_puid(puid=puid, msg=msg):
                return 0
        return 1

    def send_single_msg_by_puid(self, puid, msg):
        try:
            u = ensure_one(self.search(puid=puid))
            m = u.send(msg)
            self.save_sent_msg(m=m, to_puid=u.puid, to_name=u.name) #save sent msg
            return 1
        except Exception,e:
            print e
            return 0

    def tcplink(self, conn, addr):
        print 'Accept new connection from %s:%s...'  % addr
        data = conn.recv(8192)
        result = None
        if data:
            data = json.loads(data)
            opt = data['opt']
            if opt == 'loadallgroups':
                result = self.load_all_groups()
            elif opt == 'setgroups':
                result = self.set_groups(group_list=data['group_list']) 
            elif opt == 'sendmsgbypuid':
                result = self.send_msg_by_puid(puids=data['puids'], msg=data['msg'])
            #发送结果给客户端
            conn.send(json.dumps(result))
            #logout时会关闭socket所以，不用server端回传。checkstatus也不需要回传
            if opt == 'logout':
                self.bot_logout()
            elif opt == 'checkstatus':
                pass
        conn.close()  
        print 'Connection from %s:%s closed.' % addr
    
    def listen(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((LOCALHOST_IP, self.wxbot_port))
        server.listen(5)    #等待连接的最大数量为5
        #更改状态为listening
        self.change_status('listening')
        #添加wxbot_port属性到redis
        self.change_wxxnr_redis_data({'wxbot_port':self.wxbot_port})
        while True:
            if self.status == 'logout':
                server.close()
                break
            conn, addr = server.accept()
            t = threading.Thread(target=self.tcplink, args=(conn, addr))
            t.start()


def remove_wx_media_old_files(filepath_pre, period=30):
    #遍历filepath_pre下的文件夹，如果不在最近30天内，则删除
    #1、得到合法的（在period内）文件夹名
    legal_filepath_suf_list = []
    for i in range(1, (period + 1)):
        date_range_start_ts = time.time() - i*DAY
        date_range_start_datetime = ts2datetime(date_range_start_ts)
        legal_filepath_suf_list.append(date_range_start_datetime)
    filepath_suf_list = os.listdir(filepath_pre) #得到文件夹下的所有文件名称 
    '''
    ['2018-01-02', '2018-01-01', '2017-12-31', '2017-12-30', '2017-12-29', '2017-12-28', 
    '2017-12-27', '2017-12-26', '2017-12-25', '2017-12-24', '2017-12-23', '2017-12-22', 
    '2017-12-21', '2017-12-20', '2017-12-19', '2017-12-18', '2017-12-17', '2017-12-16', 
    '2017-12-15', '2017-12-14', '2017-12-13', '2017-12-12', '2017-12-11', '2017-12-10', 
    '2017-12-09', '2017-12-08', '2017-12-07', '2017-12-06', '2017-12-05', '2017-12-04']
    '''
    print filepath_suf_list 
    for filepath_suf in filepath_suf_list: #遍历文件夹  
        filepath = os.path.join(filepath_pre, filepath_suf)
        if os.path.isdir(filepath):
            print filepath_suf
            if not filepath_suf in legal_filepath_suf_list:
                os.remove(filepath)