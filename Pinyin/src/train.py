# -*- coding: utf-8 -*-
import pickle
import os
import math
import  pypinyin


def save_dict(obj, name):
    #outputfile = os.path.join('./train_dict/', name)
    of  = os.path.dirname(os.path.abspath(__file__)) + '/../train_dict/' + name + '.pkl'
    #print(of)
    f =  open(of, 'wb+')
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)




def is_chinese(ch):
    if u'\u4e00' <= ch <= u'\u9fff' :
        return True
    else:
        return False

#print(is_chinese("我爱崔江燕"));
#print(is_chinese("I love jiangyan cui"));
trans_matrix = {} # 二元概率         {'我爱' => 0.8 , '中国' => 1.0}
first_matrix = {} # 在句首概率       ('哎'=>0.7) 、 ('爱'=>0.3)
selec_matrix = {} # 被选择概率       'ai' => [('哎',0.7),('爱',0.3)]
triple_matrix = {} # 三元语法        {'我爱中' => 0.8}  P(我爱中)/P(我爱)
quad_matrxi = {}

first_count = {}
pinyin_first_count = {}

word_list = {}

tri_count = {}
quad_count= {}
trans_count = {}
ch_count = {}
pinyin_count = {}

def dict_insert(dict , ch):
    if (ch not in dict):
        dict.setdefault(ch, 1)
    else:
        dict[ch] = dict[ch] + 1

def get_matrix_info(sentence):
    #print(sentence)
    global  trans_count
    sub_len = len(sentence)
    #p = xpinyin.Pinyin()


    if sentence[0] in word_list:
        dict_insert(first_count, sentence[0])  # 句首
        py = (pypinyin.pinyin(sentence[0], style=pypinyin.NORMAL))[0][0]#p.get_pinyin(sentence[0])
        #print(sentence[0] + py)
        dict_insert(pinyin_first_count , py)

    for i in range(sub_len-2):
        word = sentence[i] + sentence[i+1] + sentence[i+2]

        if (sentence[i] in word_list) and (sentence[i+1]  in word_list)  and (sentence[i+2]  in word_list):
            dict_insert(tri_count,word);

    for i in range(sub_len-3):
        word = sentence[i] + sentence[i+1] + sentence[i+2] + sentence[i+3]

        if (sentence[i] in word_list) and (sentence[i+1]  in word_list)  and (sentence[i+2]  in word_list)  and (sentence[i+3]  in word_list):
            dict_insert(quad_count,word);

    for i in range(sub_len-1):
        word = sentence[i] + sentence[i+1]

        if (sentence[i] in word_list) and (sentence[i+1]  in word_list):
            dict_insert(trans_count,word);
        '''
        if(word not in trans_count):
            trans_count.setdefault(word,1)
        else:
            trans_count[word] = trans_count[word] + 1
'''

        ch = sentence[i]   #统计字符出现次数
        py = pypinyin.pinyin(ch, style=pypinyin.NORMAL)[0][0]#py = p.get_pinyin(ch)
        #print(ch + py)

        if ch in word_list:
            dict_insert(ch_count,ch)
            dict_insert(pinyin_count, py)

    if(sub_len!=1):
        ch = sentence[sub_len-1]  #最后一个字符
        if ch in word_list:
            dict_insert(ch_count, ch)
            py = pypinyin.pinyin(ch, style=pypinyin.NORMAL)[0][0]  # py = p.get_pinyin(ch)
            #print(ch + py)
            dict_insert(pinyin_count, py)


def deal_with_sentence(sentence):
    #print(sentence)
    sub_sentence = ''
    cnt = 0
    for ch in sentence:   #先把所有的完整汉字串提取出来
        if(is_chinese(ch)):
            cnt = 1
            sub_sentence = sub_sentence + ch
        elif(cnt != 0):
            cnt = 0
            get_matrix_info(sub_sentence)
            #print(sub_sentence+"*******")
            sub_sentence = ''
    if(cnt):
        get_matrix_info(sub_sentence)
       #print(sub_sentence + "*******")

def culculation_probability():
    #p = xpinyin.Pinyin()
    for k,v in first_count.items():
        #py = p.get_pinyin(k)
        py = pypinyin.pinyin(k, style=pypinyin.NORMAL)[0][0]
        prob = float(v) / pinyin_first_count[py]  # P(我)/P(wo) first
        if(k not in first_matrix):
            first_matrix.setdefault(k,0)
        first_matrix[k]=prob

    for k,v in trans_count.items():         # P(我爱)/P(我)
        trans_matrix.setdefault(k,0.0);
        trans_matrix[k] = float(v)/ch_count[k[0]]


    for k,v in tri_count.items():           # P(我爱中)/P(我爱)
        triple_matrix.setdefault(k,0.0);
        word = k[0] + k[1]
        triple_matrix[k] = float(v) / trans_count[word]

    for k,v in tri_count.items():           # P(我爱中国)/P(我爱中)
        quad_matrxi.setdefault(k,0.0);
        word = k[0] + k[1] + k[2]
        quad_matrxi[k] = float(v) / tri_count[word]

    for k,v in ch_count.items():
        #py = p.get_pinyin(k)
        py = pypinyin.pinyin(k, style=pypinyin.NORMAL)[0][0]
        prob = float(v)/pinyin_count[py]  # P(我)/P(wo)

        if(py not in selec_matrix):
            selec_matrix.setdefault(py,[])
        selec_matrix[py].append( (k,prob) )

if __name__ == '__main__':
    word_bank = open('../train_data/word.txt' ,'r' ,encoding='gbk')
    words = word_bank.readlines()
    for line in words:
        for word in line:
            word_list.setdefault(word,1)
    #print(word_list)

    file_list = os.listdir("../train_data/sina_news_gbk");
    #print(file_list)
    for str in file_list:
        #text = open('../data/std_output.txt','r' ,encoding='utf-8')
        text = open('../train_data/sina_news_gbk/'+str, 'r', encoding='gbk')
        sentence = text.readlines()
        cnt = 0
        print(len(sentence))
        for line in sentence:  # 按行读取
            #print(cnt)
            deal_with_sentence(line)
            #print(ch_count)
            #break
            cnt = cnt+1

            '''
            if cnt == 1:
                break
            '''


    culculation_probability()

    #print(trans_count)
    #print(ch_count)

    #print(first_matrix)
    #print(trans_matrix)
    #print(selec_matrix)

    save_dict(selec_matrix,"selec_matrix_sina_ex")
    save_dict(first_matrix,"first_matrix_sina_ex")
    save_dict(trans_matrix,"trans_matrix_sina_ex")
    save_dict(triple_matrix,"triple_matrix_sina_ex")
    save_dict(quad_matrxi, "quad_matrix_sina_ex")
    text.close()  # 关闭