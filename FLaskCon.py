# coding=utf-8

import json 
from flask import Flask 
from flask import request 
from flask import redirect 
from flask import jsonify
#from flask.ext.sqlalchemy import SQLAlchemy
import pymysql
import gzip
import msgpack
import urllib
import tarfile
import requests
import Init_SQL as ISQL 
import Recommand_System 
import thulac 
import snownlp
import jieba
import jieba.analyse as jae
from snownlp import sentiment 
from snownlp import SnowNLP
import synonyms
import math 

RS = Recommand_System()

# web server的搭建
# web server面对各个请求的回应
# 与数据库推荐结果列表的连接
# 


		#web server

class WebServer():
	app = Flask(__name__)

	def __init__(self):
		app = Flask(__name__)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/add',methods = ['POST'])
	def Receive_new_User(self):			#获得新注册的用户的信息并添加
		a = request.get_data() 
		dict1 = json.loads(a)
		
		#进行对数据库增加一行的操作
		user_id= dict1['id']
		DB_conn = pymysql.connect(host = 'localhost',user = 'user',password = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		cursor = DB_conn.cursor() 
		sql = "Insert INTO UTs(User_ID) values(%s)" %user_id
		cursor.execute(sql)
		DB_conn.commit() 
		cursor.close()
		DB_conn.close() 

		json_data = {'error':0}

		RS.User_ID_List.append(user_id)
		RS.User_Fav_Food_List[user_id] = set()
		return jsonify(json_data)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/edit-tag',methods = ['POST'])
	def Edit_Tag(self):	#将用户新增加的标签加入到数据库中
		a = request.get_data()
		dict2 = json.loads(a)
		user_id = dict2['id']
		tags_list = dict2['tags']
		DB_conn = pymysql.connect(host = 'localhost',user = 'user',password = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		#将用户有所行动的标签添加进其向量中
		for tag in tags_list :
			cursor_2 = DB_conn.cursor() 
			sql = """
					update UTs set %s = 1 where User_ID = %s
					"""%(tag,user_id)
			cursor_2.execute(sql)
			DB_conn.commit()
			cursor_2.close()
		DB_conn.close()
		json_data = {'error':0}
		return jsonify(json_data)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/add-favorite',methods = ['POST'])
	def Favourite_Food(self):	#将用户新增加的喜爱食物加入到数据库中
		a = request.get_data()
		dict3 = json.loads(a)
		user_id = dict3['id']
		Fav_Food = dict3['food']
	
		#用户喜欢的食物可用来增加其标签的权重
		RS.Up_Tags_Weight(Fav_Food)
		RS.User_Fav_Food_List[user_id].add(Fav_Food)
		json_data = {'error':'0'}
		return jsonify(json_data)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/delelte-favorite',methods = ['POST'])
	def Delete_Fav_Food(self):
		a = request.get_data()
		dict4 = json.loads(a)
		User_ID = dict4['id']
		Fav_Food = dict4['food']

		#删除其增加的权重
		RS.DOWN_Tags_Weight(Fav_Food)
		RS.User_Fav_Food_List[user_id].remove(Fav_Food)

		json_data = {'error':0}
		return jsonify(json_data)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/add-comment',methods = ['POST'])
	def Added_Comment_Annalysic(self):
		
		#add the func to change the table user_id---Comment_Time(+1)  
		
		DB_conn = pymysql.connect(host = 'localhost',user = 'user',password = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		a = requests.get_data()
		dict5 = json.loads(a)
		User_ID = dict5['id']
		Comment_Food = dict5['food']
		Score = dict5['rate']
		Comment = dict5['detail']
		Comment_ID = dict7['CommentId']
		Return_Tags_List = list()

		#提取文本中的标签并加入到数据库里用户的标签向量与食物的标签向量中（标签向量增量要根据其给分而定）
		tag_words = jae.extract_tags(Comment,topK = 10, withWeight = True, allowPOS = ())
		Predict_Score = SnowNLP(Comment).sentiments

		#将获得的标签与原标签表中的作对比，选出相近的作为对应的标签，相近度也要放进标签权重计算中
		Change_FTs_Cursor = DB_conn.cursor()
		Change_UTs_Cursor = DB_conn.cursor()
		for test_word, weight in tag_words:
			Rank_Dict = dict()
			for origin_tag in ISQL.Tags_List:
				Rank_Dict[origin_tag] = synonyms.compare(test_word,origin_tag,seg = True)
			Sorted_Rank_Dict = sorted(Rank_Dict.items(),key = lambda d:d[1],reverse = True)
			Most_Similiar_Tag = Sorted_Rank_Dict[0][0]
			Return_Tags_List.append(Most_Similiar_Tag)
			Similiar_Point = Sorted_Rank_Dict[0][1]

			Final_Set_Weight = math.log(Score/5 * Predict_Score*Similiar_Point * weight)
			Change_FTs_Cursor.execute("select %s from FTs where Food_ID = %s" %(Most_Similiar_Tag,Comment_Food))
			Pre_FWeight_Dict = Change_FTs_Cursor.fetchone()
			Pre_FWeight = Pre_FWeight_Dict[Most_Similiar_Tag]
			Change_FTs_Cursor.execute("Update FTs set %s = %s where Food_ID = %s" %(Most_Similiar_Tag,Pre_FWeight + Final_Set_Weight,Comment_Food))
			DB_conn.commit() 
			Change_UTs_Cursor.execute("select %s from UTs where User_ID = %s" %(Most_Similiar_Tag,User_ID))
			Pre_UWeight_Dict = Change_UTs_Cursor.fetchone() 
			Pre_UWeight = Pre_UWeight_Dict[Most_Similiar_Tag]
			Change_UTs_Cursor.execute("Update UTs set %s = %s where User_ID = %s" %(Most_Similiar_Tag,Pre_UWeight + Final_Set_Weight, User_ID))
			DB_conn.commit()

		#修改食物平均分表
		Get_Info_cursor = DB_conn.cursor() 
		Change_F_AveS_cursor = DB_conn.cursor()
		Get_Info_cursor.execute("Select * from F_AveS where Food_ID = %s"%Comment_Food)
		Food_Info_Row = Get_Info_cursor.fetchone()
		Pre_Score = Food_Info_Row['Ave_Score'] * Food_Info_Row['times']
		New_Score = Pre_Score + Score 
		New_Times = Food_Info_Row['times'] + 1
		New_Ave_Score = New_Score / New_Times
		Change_F_AveS_cursor.execute("Update F_AveS set Ave_Score = %s , times = %s where Food_ID = %s" %(New_Ave_Score,New_Times,Comment_Food))
		DB_conn.commit()
		Get_Info_cursor.close() 
		Change_F_AveS_cursor.close()
		DB_conn.close()
		json_data = {'error':0,'tag':Return_Tags_List}
		return jsonify(json_data)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/delete-comment',methods = ['POST'])
	def Delete_Comment(self):
		DB_conn = pymysql.connect(host = 'localhost',user = 'user',password = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		a = requests.get_data()
		dict7 = jason.loads(a)
		User_ID = dict7['id']
		Comment_Food = dict7['food']
		Score = dict7['rate']
		Comment = dict7['detail']
		Comment_ID = dict7['CommentId']
		#先提取其中的标签，再在UTs上去除这些标签(-1)，且在FTs上也去除
		tag_words = jae.extract_tags(Comment,topK = 10, withWeight = True, allowPOS = ())
		Predict_Score = SnowNLP(Comment).sentiments
		#最后减去该评论导致的食品评分变化
		Change_FTs_Cursor = DB_conn.cursor()
		Change_UTs_Cursor = DB_conn.cursor()
		for test_word, weight in tag_words:
			Rank_Dict = dict()
			for origin_tag in ISQL.Tags_List:
				Rank_Dict[origin_tag] = synonyms.compare(test_word,origin_tag,seg = True)
			Sorted_Rank_Dict = sorted(Rank_Dict.items(),key = lambda d:d[1],reverse = True)
			Most_Similiar_Tag = Sorted_Rank_Dict[0][0]
			Return_Tags_List.append(Most_Similiar_Tag)
			Similiar_Point = Sorted_Rank_Dict[0][1]

			Final_Set_Weight = math.log(Score/5 * Predict_Score*Similiar_Point * weight)
			Change_FTs_Cursor.execute("select %s from FTs where Food_ID = %s" %(Most_Similiar_Tag,Comment_Food))
			Pre_FWeight_Dict = Change_FTs_Cursor.fetchone()
			Pre_FWeight = Pre_FWeight_Dict[Most_Similiar_Tag]
			Change_FTs_Cursor.execute("Update FTs set %s = %s where Food_ID = %s" %(Most_Similiar_Tag,Pre_FWeight - Final_Set_Weight,Comment_Food))
			DB_conn.commit() 
			Change_UTs_Cursor.execute("select %s from UTs where User_ID = %s" %(Most_Similiar_Tag,User_ID))
			Pre_UWeight_Dict = Change_UTs_Cursor.fetchone() 
			Pre_UWeight = Pre_UWeight_Dict[Most_Similiar_Tag]
			Change_UTs_Cursor.execute("Update UTs set %s = %s where User_ID = %s" %(Most_Similiar_Tag,Pre_UWeight - Final_Set_Weight, User_ID))
			DB_conn.commit()
		
		#食物平均分表的撤销
		Get_Info_cursor = DB_conn.cursor() 
		Change_F_AveS_cursor = DB_conn.cursor()
		Get_Info_cursor.execute("Select * from F_AveS where Food_ID = %s"%Comment_Food)
		Food_Info_Row = Get_Info_cursor.fetchone()
		Pre_Score = Food_Info_Row[1] * Food_Info_Row[2]
		New_Score = Pre_Score - Score 
		New_Times = Food_Info_Row[2] - 1
		New_Ave_Score = New_Score / New_Times
		Change_F_AveS_cursor.execute("Update F_AveS set Ave_Score = %s , times = %s where Food_ID = %s" %(New_Ave_Score,New_Times,Comment_Food))
		DB_conn.commit()
		Get_Info_cursor.close() 
		Change_F_AveS_cursor.close()
		DB_conn.close()
		json_data = {'error':0}
		return jsonify(json_data)

	@app.route('/',methods = ['POST'])
	def Return_Recommand_Foods(self):
		a = request.get_data()
		dict6 = json.loads(a)
		user_id = dict6['id']


		#根据与其相似的用户及与其有过行为的物品相似度高的物品计算推荐物品列表并返回结果列表	result_list
		result_list = RS.Recommand(user_id)
		json_data = {'foods':result_list}
		return jsonify(json_data)

if __name__ == '__main__':
	web = WebServer()
	web.app.run()
	#运行时要用gunicorn运行才会有多线程
