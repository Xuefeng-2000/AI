# -*- coding: utf-8 -*-
import sys
import numpy as np
import  os
import pickle
import  math
import pypinyin

import xpinyin

selec_matrix = {}
first_matrix = {}
trans_matrix = {}
triple_matrix = {} # 三元语法        {'我爱中' => 0.8}  P(我爱中)/P(我爱)
quad_matrxi = {}

def load_dict(name):
    of = os.path.dirname(os.path.abspath(__file__)) + '/../train_dict/' + name + '.pkl'
    with open(of, 'rb') as f:
        return pickle.load(f)

def Graph_Construction(py_list):
    node = [["初"]]
    global selec_matrix
    for py in py_list:
        if py not in selec_matrix:
            node.append(['得'])
            continue
        word_list = selec_matrix[py]  #获取拼音为py 的word列表
        tmp_word_list = []
        for word_set in word_list:  # 读取word
            tmp_word_list.append(word_set[0])
        node.append(tmp_word_list)
    node.append(["末"])
    return node

def Vertebi(graph):
    lmd = 0.99999

    fst = 1.0

    global first_matrix;
    dp = [[0]]  #记录dp值
    prev = [[-1]]  #记录上一个字索引

    dp_tmp = [] #临时dp数组
    prev_tmp = []
    word_list = graph[1] #初始化概率

    cnt = 0
    for word in word_list:
        tmp_val = 0;
        py = pypinyin.pinyin(word, style=pypinyin.NORMAL)[0][0]
        list_tmp = selec_matrix[py]
        for k, v in list_tmp:
            if k == word:
                tmp_val = v
                break
        if(cnt == 0 and (word in first_matrix)):
            dp_tmp.append(  -math.log(fst*first_matrix[word] + (1.0-fst)*tmp_val)  )   #----------
        else:
            dp_tmp.append(  -math.log(tmp_val) )
        prev_tmp.append(0)

    dp.append(dp_tmp)
    prev.append(prev_tmp)

    gra_len = len(graph)
    for i in range(1,gra_len-1):
        word_list1 = graph[i]
        word_list2 = graph[i+1]
        len1 = len(word_list1)
        len2 = len(word_list2)

        dp_tmp = [99999 for j in range(len2)]  # 临时dp数组
        prev_tmp = [0 for j in range(len2)]
        dp.append(dp_tmp)
        prev.append(prev_tmp)

        for j in range(len1):  #第一个字
            now_dp = dp[i][j]
            for k in range(len2): #第二个字
                ci = word_list1[j] + word_list2[k]
                tmp_val = 0
                if(ci not in trans_matrix):
                    #print(ci)
                    py = pypinyin.pinyin(word_list2[k], style=pypinyin.NORMAL)[0][0]
                    list_tmp = selec_matrix[py]
                    for ke, v in list_tmp:
                        if ke == word_list2[k]:
                            tmp_val = v
                            break
                    new_dp = now_dp + ( -math.log( (1.0-lmd)*tmp_val) )  # <-------------
                else:
                    new_dp = now_dp + ( -math.log(lmd * trans_matrix[ci]  + (1.0-lmd)*tmp_val) )#//* 0.9 + 0.1 * selec_matrix[""]
                if i==gra_len-2:
                    new_dp = now_dp
                if new_dp < dp[i+1][k]:  #取  负log  之后要改为最小
                    dp[i+1][k] = new_dp
                    prev[i+1][k] = j
    return dp,prev

def Vertebi_3(graph):
    lmd = 0.99999

    fst = 1.0

    global first_matrix;
    dp = [[0]]  #记录dp值
    prev = [[-1]]  #记录上一个字索引

    dp_tmp = [] #临时dp数组
    prev_tmp = []
    word_list = graph[1] #初始化概率

    cnt = 0
    for word in word_list:
        tmp_val = 0;
        py = pypinyin.pinyin(word, style=pypinyin.NORMAL)[0][0]
        list_tmp = selec_matrix[py]
        for k, v in list_tmp:
            if k == word:
                tmp_val = v
                break
        if(cnt == 0 and (word in first_matrix)):
            dp_tmp.append(  -math.log(fst*first_matrix[word] + (1.0-fst)*tmp_val)  )   #----------
        else:
            dp_tmp.append(  -math.log(tmp_val) )
        prev_tmp.append(0)

    dp.append(dp_tmp)
    prev.append(prev_tmp)
    #print(len(dp))

    gra_len = len(graph)



    for i in range(0,gra_len-2):
        word_list1 = graph[i]
        word_list2 = graph[i+1]
        word_list3 = graph[i+2]
        len1 = len(word_list1)
        len2 = len(word_list2)
        len3 = len(word_list3)

        dp_tmp = [99999 for j in range(len3)]  # 临时dp数组
        prev_tmp = [0 for j in range(len3)]
        dp.append(dp_tmp)
        prev.append(prev_tmp)

        for j in range(len1):  #第一个字
            for k in range(len2): #第二个字
                now_dp = dp[i+1][k]
                for l in range(len3):
                    ci2 = word_list2[k] + word_list3[l]
                    ci = word_list1[j] + word_list2[k] + word_list3[l]
                    tmp_val = 99999
                    if(ci not in triple_matrix):
                        if (ci2 not in trans_matrix):
                            py = pypinyin.pinyin(word_list2[k], style=pypinyin.NORMAL)[0][0]
                            list_tmp = selec_matrix[py]
                            for ke, v in list_tmp:
                                if ke == word_list2[k]:
                                    tmp_val = v
                                    break
                        else:
                            tmp_val = trans_matrix[ci2]
                        new_dp = now_dp + ( -math.log( 0.7*tmp_val ) )  # <-------------
                    else:
                        new_dp = now_dp + ( -math.log(lmd * triple_matrix[ci]  + (1.0-lmd)*tmp_val) )#//* 0.9 + 0.1 * selec_matrix[""]
                    if i==gra_len-3:
                        new_dp = now_dp
                    #print(len(dp),i+2)
                    if new_dp < dp[i+2][l]:  #取  负log  之后要改为最小
                        dp[i+2][l] = new_dp
                        prev[i+2][l] = k
    return dp,prev


def dfs(n,idx,graph,prev):
    if(n == 1):
        return ''
    prev_idx = prev[n][idx]
    return  dfs(n-1,prev_idx,graph,prev) +graph[n-1][prev_idx] #上一个字

def pinyin(py_list):
    graph = Graph_Construction(py_list)
    #print(graph)
    dp , prev = Vertebi(graph) #二元模型
    #dp, prev = Vertebi_3(graph) #三元 翻车模型
    #print(dp)
    len_g = len(graph)
    return dfs(len_g-1,0,graph,prev)

def Merge(dict1, dict2):
    return(dict2.update(dict1))

def get_accuracy(a,b):
    ac = 0
    len_t = len(a)
    for i in range(len_t):
        if a[i] == b[i]:
            ac = ac+1
    return 1.0*ac / len_t

if __name__ == '__main__':
    inputfile = open(sys.argv[1],"r")
    output = open(sys.argv[2],"w")

    output_std = open("../data/sub_std_sina.txt", "r")
    list_std = output_std.readlines()

    selec_matrix = load_dict("selec_matrix_sina")
    first_matrix = load_dict("first_matrix_sina")
    trans_matrix = load_dict("trans_matrix_sina")

    len_count = [0 for j in range(25)]
    len_acc_sum = [0.0 for j in range(25)]


    lines = inputfile.readlines()
    out_list = []
    for line in lines:
        line_tmp = line.rstrip()
        tmp = pinyin(line_tmp.split(' '))
        out_list.append(tmp)
        output.write(tmp+'\n');
        #print(tmp)
   

    '''
    len_all = len(lines)
    ac = 0.0
    cnt = 0
    for i in range(len_all):
        acc = get_accuracy(list_std[i].strip(),out_list[i])
        ac = ac + acc
        len_s = len(out_list[i])
        idx = len_s//4
        #if(acc == 1.0 and len_s > 20):   #正确 长 句子
        #    print('std_out : ' + list_std[i].strip())
        #    print('output  : ' + out_list[i])
        
        #if list_std[i].strip() != out_list[i]: #表现不好的句子
        #if get_accuracy(list_std[i].strip(),out_list[i]) < 0.3 :
        #    print('std_out : '+ list_std[i].strip())
        #    print('output  : '+out_list[i])
        #    print(acc)
    #print( str(round(ac /len_all *100,5)) + '%' )
    '''

    '''
    print("--")
    while True:
        line = input()
        print(pinyin(line.split(' ')))
    '''


    inputfile.close()
    output.close()
    output_std.close()