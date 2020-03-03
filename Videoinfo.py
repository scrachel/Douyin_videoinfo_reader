# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 10:30:12 2020

@author: Scrachel
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import randn, chisquare

    
def read_Douyin_videoinfo(file_name):
    file1 = open(file_name, 'r') 
    Lines = file1.readlines() 
    file1.close()
    enter_count=0  #无用变量
    #video_count=0
    biaoti=[]
    release_time=[]
    bofang=[]
    dianzan=[]
    fenxiang=[]
    pinglun=[]
    
    #所有可能字符内容
    probable_lines=['查看评论\n', '投放DOU+\n', '我的视频\n']
    
    for i in range(len(Lines)):
        if Lines[i] == '\n':
            enter_count = enter_count + 1
    #        if enter_count == 2:
    #            video_count = video_count + 1
    #            enter_count = 0
        elif Lines[i].find(':') > -1:
    #        print(i)
            colon_pos = Lines[i].find(':')
            line = Lines[i][colon_pos+2:]
            if Lines[i].find('题') > -1:
                biaoti.append(line)
    #            print(i,line)
            elif Lines[i].find('时间') > -1:
                release_time.append(pd.to_datetime(line))
            elif Lines[i].find('播放') > -1:
                bofang.append(int(line))
            elif Lines[i].find('赞数') > -1:
                dianzan.append(int(line.split('/')[0]))
            elif Lines[i].find('享数') > -1:
                fenxiang.append(int(line.split('/')[0]))
            elif Lines[i].find('论数') > -1:
                pinglun.append(int(line.split('/')[0]))
            else:
                print('Error.')
            enter_count=0
        elif Lines[i] in probable_lines:
            pass
        elif int(Lines[i]):
            #这句尽可能放后面 也可以把这个elif分支注释掉
            pass
        else:
            print('Error.')
            print(Lines[i])
            
    bofang_ = np.array(bofang)
    dianzan_ = np.array(dianzan)
    fenxiang_ = np.array(fenxiang)
    pinglun_ = np.array(pinglun)
    return bofang_, dianzan_, fenxiang_, pinglun_, biaoti, release_time


file_name = r'C:\\Users\Scrachel\.spyder\Video_info.txt'
bofang, dianzan, fenxiang, pinglun, biaoti, release_time = \
    read_Douyin_videoinfo(file_name=file_name)
    
#####处理数据重复问题  假设不存在更复杂的重复性，即同一播放量只对应同一视频
bofang_0 = np.unique(bofang)
index_list = []
for i in bofang_0:
    index_list.append(np.argwhere(bofang==i)[0][0])
    
bofang = bofang[index_list]
dianzan = dianzan[index_list]
pinglun = pinglun[index_list]
fenxiang = fenxiang[index_list]


# =============================================================================
# #####发布时间
# fig, ax = plt.subplots(figsize=(8,5))
# ax.set_xlabel('Release time', fontsize=15)
# ax.set_ylabel('Hits', fontsize=15)
# plt.yscale('log', nonposy='clip')
# ax.set_ylim(1e+4,1e+7)
# time_spread = max(release_time)-min(release_time)
# ax.set_xlim(min(release_time)-0.1*time_spread, 
#             max(release_time)+0.1*time_spread)
# ax.scatter(release_time, bofang)
# fig.tight_layout()
# =============================================================================

# =============================================================================
# #####评论量
# fig, ax = plt.subplots(figsize=(8,5))
# ax.set_ylabel('Comments', fontsize=15)
# ax.set_xlabel('Hits', fontsize=15)
# plt.yscale('log', nonposy='clip')
# plt.xscale('log')
# ax.set_xlim(1e+4,1e+7)
# ax.set_ylim(10,3500)
# ax.scatter(bofang, pinglun)
# fig.tight_layout()
# #plt.show()
# fig.savefig('pinglun_bofang.png', dpi=500)
# =============================================================================

######点赞量
#fig, ax = plt.subplots(figsize=(8,5))
#ax.set_ylabel('DianZan', fontsize=15)
#ax.set_xlabel('Hits', fontsize=15)
#plt.yscale('log', nonposy='clip')
#plt.xscale('log')
#ax.set_xlim(1e+4,1e+7)
#ax.set_ylim(500,1.5e5)
#ax.scatter(bofang, dianzan)
#fig.tight_layout()
##plt.show()
#fig.savefig('dianzan_bofang.png', dpi=500)
#
######点赞率
#condi=np.where(bofang>1e+4)
##plt.yscale('log', nonposy='clip')
#plt.xscale('log')
#ax.set_xlim(1e+4,1e+7)
#ax.set_ylim(0,0.05)
#ax.scatter(bofang[condi], dianzan[condi]*1.0/bofang[condi])
#fig.tight_layout()
#plt.show()

# =============================================================================
# #####分享量
# fig, ax = plt.subplots(figsize=(8,5))
# ax.set_ylabel('Sharing', fontsize=15)
# ax.set_xlabel('Hits', fontsize=15)
# plt.yscale('log', nonposy='clip')
# plt.xscale('log')
# ax.set_xlim(1e+4,1e+7)
# ax.set_ylim(10,2500)
# ax.scatter(bofang, fenxiang)
# fig.tight_layout()
# #plt.show()
# fig.savefig('fenxiang_bofang.png', dpi=500)
# =============================================================================


#desensitization
def random_modi(size):
    x = randn(size)
    range_y = np.exp2(0.3 * x**3 + np.sqrt(abs(x)))
    range_y[np.where(range_y>1.3)] = 0.23 * \
                                chisquare(13,np.where(range_y>1.3)[0].size)
    factor_y = range_y / 3.0 * randn(size) * 0.1
    return(factor_y)
    
y = (random_modi(np.size(bofang)) * dianzan + dianzan) // 1
x = (random_modi(np.size(bofang)) * bofang + bofang) // 1


fig, ax = plt.subplots(figsize=(8,5))
ax.set_ylabel('DianZan', fontsize=15)
ax.set_xlabel('Hits', fontsize=15)
plt.yscale('log', nonposy='clip')
plt.xscale('log')
ax.set_xlim(1e+4,1e+7)
#ax.set_ylim(5,1.5e5)
ax.set_ylim(500,1.5e5)
ax.scatter(x, y)
fig.tight_layout()
#plt.show()
fig.savefig('dianzan_bofang_0.png', dpi=100)