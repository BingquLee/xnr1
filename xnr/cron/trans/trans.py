# -*- coding: utf-8 -*-
from google_trans import translate as google_trans
from baidu_trans import translate as baidu_trans
from youdao_trans import translate as youdao_trans
from langconv import *
import time

#q为待翻译的语句组成的列表
def trans(q):
    if isinstance(q, list):
        res = google_trans(q)
        if res:
            return res
        else:
            res = baidu_trans(q)
            if res:
                return res
            else:
                res = youdao_trans(q)
                if res:
                    return res
    return False

#繁体转简体
def traditional2simplified(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence


if __name__ == '__main__':
    # '''
    #q = ['안녕하세요.', 'Hello world','test',"Jason Gao shared Joel Wang's post."]
    #q = ["絕食、減肥、刷存在感，到處都有不作秀就會死的人。不過作秀到最後也是把自己作死。 https://t.co/yVcGdVZ9h7"]
    #q = ["ཁྱེད་གཉིས་ཞལ་འཕྲད་དགོས་。 7ཀརྨ་པ་ཨོ་རྒྱན་འཕྲིན་ལས་རྡོ་རྗེ་མཆོག་དང་་7ཀརྨ་པ་མཐའ་ཡས་རྡོ་རྗེ་མཆོག་གཉིས་ངེས་པར་དུ་ཞལ་མཇལ་འཛོམས་གནང ་ནས་ཞི་བའི་མཛའ་འབྲེལ་བསྐྲུན་དགོས་。ཁྱེད་རྣམ་གཉིས་མི་ལོ་མང་པོ་རིང་ལ་ཕན་ཚུན་ཞལ་འཕྲད་པའི་གསུང་གླེང་གང་ཡང ་མི་འདུགདེ་ནི་སྲིད་ཀྱི་གནོད་ཤུགས་དང་་。སྒེར་གྱི་བྱ་བ་ཞིག་གིས་ཡིན་ནམ་。གཞན་དུ་ན་ཅི་ཞིག་。ཁོ་བོས་འདི ་ནས་འབོད་སྐུལ་དང་་。དྲན་གསོ་ཞིག་བྱ་འདོད་པ་ཞ ིག་ལ་。ད་ལན་ངེད་བོད་རྒྱུད་ནང་བསྟན་གྱི་བླ་ཆེན་གཉིས་འབྲེལ་མེད་སོ་སོར་འཁོད་པའི་གནས་སྟངས་དེས་。འོག་གི་མཆོད་ སྡེ་ཁག་དང་་。དད་ལྡན་པ་རྣམས་ལ་གས་ཆག་ཅིག་མཐོང་སོང་་。ད་ནི་གས་ཆག་དེ་མེད་པར་བཟོ་མཁན་དེ་。སྤྲུལ་ སྐུ་ཁོང་གཉིས་ལ་འགན་འཁྲི་དེ་བབས་ཡོད་。སོང་ཙང་་。ཁྱེད་རྣམ་གཉིས་ངེས་པར་མཇལ་འཕྲད་གནང་ནས་ཕ་མ་གཅིག་གི་སྤུན ་ཟླ་ནང་བཞིན་ཕན་ཚུན་ལ་བརྩེ་བའི་འདུ་ཤེས་བསྟེན་དགོས་。ད ་ལྟར་བྱུང་ན་བོད་བྱིངས་དང་་。ལྷག་པར་བཀའ་རྒྱུད་ཀྱི་བསྟན་པའི་འཕྲིན་ལས་དེ་ཁྱབ་བརྡལ་མུ་མེད་དུ་འགྲོ་ངེས་。དེས་ ན་བཀའ་རྒྱུད་ཀྱི་བླ་ཆེན་དང་་。མཁན་པོ་。དད་ལྡན་པ་གཙོས་བོད་པ་ནང་བསྟན་ཆོས་ལུགས་རིས་མེད་སེམས་ལ་འཁྱིལ་ཚུན ་དེ་ལྟར་རེ་སྐུལ་དང་་。གདོང་གཏུགས་ཀྱི་བྱ་འགུལ་ངེས་པར་སྤེལ་དགོས་。སྤྱི་ལོ་。ཟླ217 10 13ཚེསཉིན་སྟོང་ཐུན་པས་ཚོར་བ ་དྲག་པོ་རླབས་ཀྱི་སྣག་ཚ་བྱས་ནས་ཤར་མར་ས ྲིངས་སོ་。་。"]
    # q = ["RT @nyhopin: 失算的諜戰：郭文貴、劉彥平與川普、FBI （《點點今天事》）https://t.co/TQ97rNa1LH https://t.co/xARoQGmYRB"]
    # m = ["RT @nyhopin: 失算的谍战：郭文贵、刘彦平与川普、FBI （《点点今天事》）https://t.co/TQ97rNa1LH https://t.co/xARoQGmYRB"]
    q = ["Jason Gao shared Joel Wang's post"]
    
    start = time.time()
    print trans(q)[0]
    # print trans(q)[0].encode('utf-8')
    end = time.time()
    print end-start
    # '''

    # li = [u'', u'新聞、時事、中國內幕、香港台灣新聞、世界新聞、財經、名家點評、生活、教育、時尚、幽默、奇聞異事、娛樂、健康養生', u'正體：http://b5.secretchina.com/ 簡體：http://www.secretchina.com/']
    # # traditional_sentence = u'新聞、時事、中國內幕、香港台灣新聞、世界新聞、財經、名家點評、生活、教育、時尚、幽默、奇聞異事、娛樂、健康養生 正體：http://b5.secretchina.com/ 簡體：http://www.secretchina.com/'
    # for l in li:    
    #     simplified_sentence = traditional2simplified(l)
    #     print(simplified_sentence)
    