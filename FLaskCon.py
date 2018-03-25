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
import Recommand_System as RS 


# web server的搭建
# web server面对各个请求的回应
# 与数据库推荐结果列表的连接
# 


		#web server
app = Flask(__name__)

class WebServer():
	app = Flask(__name__)

	def __init__(self):
		app = Flask(__name__)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/add',methods = ['POST'])
	def Receive_new_User(self):			#获得新注册的用户的信息并添加
		a = request.get_data() 
		dict1 = json.loads(a)
		
		#此处要进行对数据库增加一行的操作
		user_id= dict1['id']

		#对参数的检查控制
		DB_conn = pymysql.connect(host = 'localhost',user = 'user','password' = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		cursor = DB_conn.cursor() 
		sql = "Insert INTO 'UTs' ('User_ID') Values ( user_id )"
		cursor.execute(sql)
		DB_conn.commit() 
		cursor.close()
		DB_conn.close() 

		json_data = {'error':'0'}
		return jsonify(json_data)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/edit-tag',methods = ['POST'])
	def Edit_Tag(self):	#将用户新增加的标签加入到数据库中
		a = request.get_data()
		dict2 = json.loads(a)
		user_id = dict2['id']
		tags_list = dict2['tags']
		DB_conn = pymysql.connect(host = 'localhost',user = 'user','password' = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		#将用户有所行动的标签添加进其向量中
		for tag in Tags_List :
			cursor_2 = DB_conn.cursor() 
			sql = """
					update UTs set %s = 1 where User_ID = user_id
					"""
			cursor_2.execute(sql)
			DB_conn.commit()
			cursor_2.close()
		DB_conn.close()

		json_data = {'error':'0'}
		return jsonify(json_data)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/add-favorite',methods = ['POST'])
	def Favourite_Food(self):	#将用户新增加的喜爱食物加入到数据库中
		a = request.get_data()
		dict3 = json.loads(a)
		user_id = dict3['id']
		Fav_Food = dict3['food']
		DB_conn = pymysql.connect(host = 'localhost',user = 'user','password' = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		#用户喜欢的食物可用来增加其标签的权重
		RS.Up_Tags_Weight(Fav_Food)

		json_data = {'error':'0'}
		return jsonify(json_data)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/delelte-favorite',methods = ['POST'])
	def Delete_Fav_Food(self):
		a = request.get_data()
		dict4 = json.loads(a)
		User_ID = dict4['id']
		Fav_Food = dict4['food']

		#删除其增加的权重
		DB_conn = pymysql.connect(host = 'localhost',user = 'user','password' = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		RS.DOWN_Tags_Weight(Fav_Food)
		

		json_data = {'error':'0'}
		return jsonify(json_data)

	@app.route('/http://lcoalhost:8080/v1/backend/food/sync/user/add-comment',methods = ['POST'])
	def Comment_Annalysic(self):
		a = requests.get_data()
		dict5 = json.loads(a)
		User_ID = dict5['id']
		Comment_Food = dict5[food]
		Score = dict5['rate']
		Comment = dict5['detail']

		#提取文本中的标签并加入到数据库里用户的标签向量中


		json_data = {'error':'0'}
		return jsonify(json_data)

	@app.route('/',methods = ['POST'])
	def Return_Recommand_Foods(self):
		a = request.get_data()
		dict6 = json.loads(a)
		user_id = dict6['id']

		#根据与其相似的用户及与其有过行为的物品相似度高的物品计算推荐物品列表并返回结果列表	result_list
		result_list = RS.Recommand_List(user_id)

		return jsonify(result_list)

if __name__ == '__main__':
	web = WebServer()
	web.app.run()
