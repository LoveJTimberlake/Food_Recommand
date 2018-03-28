#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 14:36:45 2018

@author: justintimberlake
"""

import random 
import math 
from operator import itemgetter

#RMSE均方根误差
def RMSE(records):
	return math.sqrt(sum([(rui - pui) * (rui - pui) for u,i,tui,pui in records]) / float(len(records)))

#准确率与召回率
def PrecisionRecall(test,N):
	hit = 0
	n_recall = 0
	n_precision = 0
	for user, items in test.items():
		rank = Recommend(user, N)
		hit += len(rank & items)
		n_recall += len(items)
		n_precision += N
	return [hit/(1.0 * n_recall), hit/(1.0 * n_precision)]

#基尼系数：评估推荐结果的流行度（覆盖率）
def GiniIndex(p):
	j = 1
	n = len(p)
	G = 0
	for item, weigh in sorted(p.items(), key = itemgetter(1)):
		G += (2*j - n - 1) * weight
	return G/float(n-1)

#将数据集分为训练集与测试集
def SplitData(data,M,k,seed):	#共M份数据，1份为测试集，其余是训练集，共进行M份测试（每次k不同）并取其平均值做最后指标
	test = []
	train = []
	random.seed(seed)
	for user,item in data:
		if random.randint(0,M) == k :
			test.appen([user,item])
		else:
			train.append([user,item]) 
	return train,test

def Jingzhunlv():
	return PrecisionRecall()[0]/PrecisionRecall()[1];

#计算覆盖率
def Coverage(train, test, N):
	recommend_items = set()
	all_items = set()
	for user in train.keys():
		for item in train[user].keys():	#字典train中user对应的所有物品组成的可遍历列表
			all_items.add(item)
		rank = GetRecommendation(user, N)
		for item, pui in rank:
			recommend_items.add(item)
	return len(recommend_items) / (len(all_items) * 1.0)

#UserCF
def UserSimilarity(train):
	#建立物品-用户倒排表
	item_users = dict()
	for u,items in train.items():
		for i in items:	#要将原数据集中变为key:[value]才可
			if i not in item_users:
				item_users[i] = set()
			item_users[i].add(u)
	#计算用户之间相关联的物品
	C = dict()
	N = dict()
	for i, users in item_users.items():
		for u in users:
			N[u] += 1
			for v in users:
				if(u == v): continue 
				C[u][v] += 1

	#计算相似矩阵
	W = dict()
	for u,related_users in C.items():
		for v,cuv in related_users.items():
			W[u][v] = cuv/math.sqrt(N[u]*N[v])
	return W
def Recommend(user,train, W,K):     #推荐算法，为每个用户选出K个兴趣近似的用户并推荐他们感兴趣的物品(K = 80时性能最好)
	rank = dict()
	interacted_items = train[user]	#user有过行为的物品
	for v,wuv in sorted(W[user].items,key = itemgetter(1), reverse = True)[0:K]:	#在相似矩阵中获得user与其他用户的相似系数元组
		for i, rvi in train[v].items:
			if i in interacted_items:
				continue 
			rank[i] += wuv * rvi	#rank[i]是指user对i的感兴趣指数 比如B,D对c有行为，求A对c的兴趣程度即用A与B的相似度 + A与D的相似度
	return rank 	

#改进后的用户相似度推荐算法 User-IIF
def UserSimilarity_new(train):
	#build inverse table 
	item_users = dict()
	for u,items in train.items():
		for i in items.keys():
			if i not in item_users:
				item_users[i] = set()
			item_users[i].add(u)

	#calculate co-rated items between users 
	C = dict()
	N = dict()
	for i , users in item_users.items():
		for u in users :
			N[u] += 1
			for v in users:
				if u == v: continue 
				C[u][v] += 1/math.log(1+len(users))

	#calculate finial similarity matrix W 
	W = dict()
	for u,related_users in C.items():
		for v,cuv in related_users.items():
			W[u][v] += cuv/math.sqrt(N[u] * N[v])
	return W 


#ItemCF 
def ItemSilimlarity(train):
    C = dict()
    N = dict()
	#先建立一个用户-物品倒排表
    for user, items in train.items():
        for item in items:
            N[item] += 1
            for other_item in items :
                if item == ohter_item :
                    continue 
                C[item][other_item] += 1
        
        
	#计算相似矩阵
    W = dict()
    for i, related_items in C.items():
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])   #归一化操作  variable doubts
    return W


def Recommandation(train, user_id, W, K):#提供推荐物品排名名单
    rank = dict()
    ru = train[user_id]         #things user haved behaved to 
    for i, pi in ru.items():    #pi means 兴趣程度
        for j,wj in sorted(W[i].items(), key = itemgetter(1), reverse = True)[0:K]: #wj 为物品之间相似度
            if j in ru: 
                continue
            rank[j] += pi * wj
    return rank

def ItemSimilarityII(train):
    C = dict()
    N = dict()
    for user, items in train.items():
        for i in items :
            N[i] += 1
            for j in items :
                if i == j : 
                    continue 
                C[i][j] += 1/ log(1+ len(items) * 1.0)
                
    W = dict()
    for i, related_items in C.items():
        for j , cij in related_items.items():
            W[i][j] = cij/math.sqrt(N[i] * N[j])
    
    return W

def ItemSimilarity_Norm(tarin):
    Max = 0
    C = dict()
    N = dict()
    for user, items in train.items():
        for i in items :
            N[i] += 1
            for j in items :
                if i == j : 
                    continue 
                C[i][j] += 1/ log(1+ len(items) * 1.0)
                
    W = dict()
    for i, related_items in C.items():
        for j , cij in related_items.items():
            W[i][j] = cij/math.sqrt(N[i] * N[j])
            Max = max(Max,M[i][j])
    for i, related_items in C.items():
        for j , cij in related_items.items():
            W[i][j] /= Max      #归一化
            
    return W




#对每个用户，要保证正负样本的平衡(数目相似)。
#对每个用户采样负样本时，要选取那些很热门，而用户却没有行为的物品。
#采集负样本
def RandomSelectNegativeSamples(items):     #items 是用户喜欢的所有物品的集合
    ret = dict()
    for i in items.keys():
        ret[i] = 1
    n = 0
    items_pool = InitItems_Pool(items)  #items_pool里面的是没有被行为过的物品集合
    for i in range(0,len(items) * 3):
        item = items_pool[random.randint(0,len(items_pool) - 1)]
        if item in ret:
            continue
        ret[item] = 0   #此为负样本
        n += 1
        if n > len(items):
            break;
    return ret

def InitItems_Pool(items):
    Behaved_items = set(items.keys())
    items_pool = list(ItemList - Behaved_items)
    return items_pool

def CreateItemsList(train):
    ItemList = set()
    for user,items in train.items():
        for item in items:
            ItemList.add(item)
    return ItemList
    
def InitModel(user_items, F):   #返回用户与隐类、物品与隐类的矩阵，用于填写其中的关系系数
    P = dict()
    Q = dict()
    for user, items in user_items.items():
        P[user] = dict()
        for f in range(0,F):
            P[user][f] = random.random()
        for item in items():
            if item not in Q:
                Q[item] =dict()
                for f in range(0,F):
                    Q[item][f] = random.random()
    return P,Q
            
def Predict(user,item, P, Q):   #
    rate = 0
    for f, puf in P[user].items():
        qif = Q[item][f]
        rate += qif * puf
    return rate


def LatentfactorModel(train,F,N,alpha, lambda_num):
    #F指的是所有隐类特征数目  N指的是迭代优化次数
    itemlist = CreateItemsList(user,train)
    [P,Q] = InitModel(train, F)    #P是用户与隐类之间的矩阵，Q是物品与隐类之间的矩阵
    for step in range(0,N):
        for user, items in train.items():
            samples = RandomSelectNegativeSamples(items)
            for item,rui in samples.items():
                eui = rui - Predict(user, item, P , Q)
                for f in range(0,F):
                    P[user][f] += alpha * (eui * Q[item][f] - lambda_num * P[user][f])
                    Q[item][f] += alpha * (eui * P[user][f] - lambda_num * Q[item][f])
        alpha *= 0.9 
    return P,Q

def Self_Recommandation(user,train,P,Q):
    rank = dict()
    Behaved_items = train[user]
    for i, other in Q:
        if i in Behaved_items:
            continue 
        rank.setdefault(i,0)
        for f, qif in other.items():
            puf = P[user][f]
            rank += puf * qif
    return rank

def All_Recommandation(train,P,Q):
    result = dict()
    for user, items in train.items():
        rank = Self_Recommandation(user,train,P,Q)
        R = sorted(rank.items(),key = itemgetter(1),reverse = True)
        result[user] = R
    return result

#传统LFM模型很难实时进行推荐，Yahoo有推出新的解决方法：
#class Yahoo_LFM:
    
    
    

    
#基于图的模型
def PersonalRankZ(G, alpha, root):
    rank = dict()
    rank = {x : 0 for x in G.keys()}   # equal to rank[x] = 0
    rank[root] = 1
    for k in range(20):
        tmp = {x : 0 for x in G.keys()}
        for i, ri in G.items():
            for j, wij in ri.items():
                if j not in tmp:
                    tmp[j]= 0
                tmp[j] += 0.6 * rank[i] / (1.0 * len(ri))
                if j == root:
                    tmp[j] += 1 - alpha 
        rank = tmp
    return rank

#改进方法参考论文   Song Li "Fast Algorithms for sprase matrix inverse compuatations"

#冷启动问题

#1.利用用户注册信息为其推荐物品
#(1) 获取用户的注册信息;
#(2) 根据用户的注册信息对用户进行特征分类;
#(3) 给用户推荐他属于的几个特征类中前20共有的物品

#书本82页公式
users_info = set()
NP = {'广东','湖南','湖北','河南','河北','北京','东北'}
AGE = dict()
for i in range(0,101,step = 5):
    AGE[i//5] = set()
def Finish_SignUp_And_Commend(users_info,train):
    C = dict()
    for user,items in train.items():
        C[user] = set()
        for item in items:
            C[item] += 1
    user_info = {'ID':None,'NickName':None,'Native Place':None,'Age':None}
    for key in user_info.keys():
        user_info[key] = input(key + ':')
    age = user_info['Age']
    AGE[age//5].add(user_info['ID'])
    
        

        
        

        
        
        
#利用物品内容信息来计算物品相似度 Page 89
#物品内容过滤适用于 用户行为受物品某一属性影响严重的情况
#def Cal_Similarity_BasedOn_vec(train, entity-items):
    
    

    

#LDA模型  计算物品在话题中的分布，利用KL散度获得物品的相似度
    
    
    
#相对于上面的隐语义模型，给物品打上标签更为方便与高效
    
#1.记录物品上的标签     (假设在用户进行物品互动时都给物品加上了标签)
#2.计算标签的流行度
def Tag_Pop(train):
    Tag_Pop = dict()
    for user, items in train.items():
        for item in items.items():  
            for tag in item['TAG']:
                if tag in Tag_Pop.keys():
                    Tag_Pop[tag] += 1
                else:
                    Tag_Pop[tag] = 1
    return Tag_Pop

#3.根据物品的标签向量计算两个物品的相似度
def CosinSim(train):
    C = dict()
    S = dict()
    ret = 0;
    for user, items in train.items():
        for item1 in items.items():
            for tag in item1['TAG']:
                for item2 in items.items():
                    if iitem1 == item2: 
                        continue
                    else if tag in j['TAG']:
                        C[item1][item2] += 1    #两件物品共有的标签量
                    S[item1][item2] = C[item1][item2] / math.sqrt(len(item1['TAG'])*len(item2['TAG']))
    return S

#还要统计一下多样性和新颖度

#4.给用户推荐标签
def RecommendHybridPopTags(user,item,user_tags,item_tags,alpha,N):  #alpha = 0.8结果较好
    ret = dict()
    max_user_tag_weight = max(user_tags[user].values())
    for tag, weight in user_tags[user].items():
        ret[tag] = (1-alpha) * weight / max_user_tag_weight
    
    max_item_tag_weight = max(item_tags[item].values())
    for tag, weight in item_tags[item].items():
        if tag not in ret:
            ret[tag] = alpha * weight / max_item_tag_weight
        else :
            ret[tag] += alpha * weight/ max_item_tag_weight
    return sorted(ret[user].items(), key = itemgetter(1), reverse = True)[0:N]


#给用户推荐当前最近一段时间内最热门的物品
def RecentPop(record, alpha, T):
    ret = dict()
    for user, item, tm in record.items():
        if tm >= T:
            continue 
        ret[item] = 1 / (1.0 + alpha * (T - tm))
    return sorted(ret.items(),key = itemgetter(1),reverse = True)[0:5]



#基于时间计算物品相似度
def ItemSimilarity(train, alpha):
    C = dict()
    N = dict()
    for user,items in train.items():
        for i,tui in items.items():
            N[i] += 1
            for j,tuj in items.items():
                if i == j:
                    continue
                C[i][j] = 1/(1+ alpha * abs(tui - tuj))
                
    W = dict()
    for i,related_items in C.items():
        for j,cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return W

def Recommendation(train, user_id, W, K,t0):
    rank = dict()
    ru = train[user_id]
    for i,pi in ru.items():
        for j,wj in sorted(W[i].items(),key = itemgetter(1), reverse = True)[0:K]:
            if j,tuj in ru.items():
                continue
            rank[j] += pi*wj/(1+alpha * (t0 - tuj))
    return rank




#基于时间的用户相似度
def UserSimilarity(train):
    item_users = dict()
    for user,items in train.items():
        for i,tui in items.items():
            if i not in item_users.keys():
                item_users[i] = dict()
            item_users[i][user] = tui
    
    C = dict()
    N = dict()
    for i,users in item_users.items():
        for u,tui in users.items():
            N[u] += 1
            for v,tvi in users.items():
                if u == v:
                    continue
                C[u][v] += 1/ ( 1 + alpha * abs(tui - tvi))
            
    W = dict()
    for u,related_users in C.items():
        for v,cuv in related_users.items():
            W[u][v] = cuv/math.sqrt(N[u] * N[v])
    return W

def Recommend(user, T, train, W):
    rank = dict()
    interacted_items = train[user]
    for v,wuv in sorted(W[u].items(),key = itemgetter(1),reverse = True)[0:K]:
        for i, tvi in train[v].items():
            if i in interacted_items:
                continue 
            rank[i] += wuv/(1 + alpha * (T - tvi))
    return rank


#下面开始构建推荐系统
    






























            













































