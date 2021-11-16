文件目录结构:
./Pinyin/train_data 语料库 2016.[2-11]Sina news

./Pinyin/src   源文件 train.py为预处理程序  pinyin.py为可执行程序

./Pinyin/train_dict 预处理结果文件

./Pinyin/data  输入/输出文件  

Input : input.txt       sub_in_sina.txt    分别为样例输入和自己爬取的2021.10sina news
Output: output.txt      sub_out_sina.txt   分别对应输出
Stdout: std_output.txt  sub_std_sina.txt   分别对应标准输出

----------------------------------------------------------------------
cd ./Pinyin/src
Python3 pinyin.py ../data/输入文件  ../data/输出文件



