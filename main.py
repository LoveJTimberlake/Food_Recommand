# coding=utf-8

#1.先在mysql中获得数据
#2.将获得的数据进行清洗筛选形成各自表格
#3.利用各自表格生成必要的特征向量
#4.利用特征向量计算相似度（Item,User)
#5.利用相似度分别推荐排名靠前的物品



import pymysql
import math 
import 

def CreateTable():
	database = pymysql.Connect(
		host = 'service_ip',
		user = 'root',
		db = 'demo',
		password = ' ',
		port = '',	#服务器端口号
		)
	#大表格1：<user_id, food_id, bussiness_id, tags(list), score>
	#大表格2：<user_id, food_id, behavior>
	#大表格3: <user_id, bussiness_id, behavior>

	#目标表格：1.食物 标签 占比   2.用户 食物 分数  2.用户，商家，分数  3.用户，标签，（0,1）

	#1.先抽取food_tag向量，获取food_tag的标签向量
	food_tags,food_tag_num = Food_Tags(table_1)
	Final_Food_Tag = dict()
	for food, tag_num in food_tags.items():
		Final_Food_Tag[food] = dict()
		for tag,num in tag_num.items():
			Final_Food_Tag[food][tag] = food_tags[food][tag] / food_tag_num[food][num]

	#2.抽取User_Food的向量






def Food_Tags(database):
	sql = "Select food_id,tag from table_1"
	cursor = database.cursor()
	cursor.execute(sql)

	Food_Tags = dict()	#记录一个食物各个标签被打数量
	Food_Tags_Num = dict()
	for food, tag in "select food_id, tag from Table_1":
		Food_Tags[food] = dict()
		if tag not in Food_Tags[food].keys():
			Food_Tags[food][tag] = 0
		Food_Tags[food][tag] += 1 
		if food not in Food_Tags_Num.keys():
			Food_Tags_Num[food] = 0
		Food_Tags_Num[food] += 1
	cursor.close()
	return Food_Tags,Food_Tags_Num


def Person_Food(database):
	person_food = dict()
	cursor = database.cursor()
	sql = "select user_id,food_id, score from Table_1"
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		User_ID = row[0]
		Food_ID = row[1]
		Score = row[2]
		if User_ID not in person_food.keys():
			person_food[user_id] = dict()
		person_food[User_ID][Food_ID] = Score 
	cursor.close()


	sql = "select * from Table_2"
	cursor = database.cursor()
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		User_ID = row[0]
		Food_ID = row[1]
		Shoucang = row[2]
		Share = row[3]
		person_food[User_ID][Food_ID] += 3 * Shoucang + 2 * Share 
	cursor.close()
	return person_food


def Person_Bussiness(database):
	person_store = dict()
	cursor = database.cursor()
	sql = "select * from Table_3"
	cursor.execute(sql)
	results = cursor.fetchall(sql)
	for row in results:
		User_ID = row[0]
		Buss_ID = row[1]
		Score = row[2]
		person_store[User_ID] = dict()
		person_store[User_ID][Buss_ID] = Score
	cursor.close()
	return Person_Bussiness



def Person_Tags(database):
	person_tags = doct() 
	cursor = database.cursor()
	sql = "select"

























