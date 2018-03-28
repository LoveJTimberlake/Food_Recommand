# coding=utf-8

#推荐系统主要后台代码

import Init_SQL as ISQL 

#功能：1.从数据库中生成User_Tags与Food_Tags的字典	2.计算User与Food的两个相似矩阵   3.针对用户喜爱的食物来调整其拥有的标签的权重   4.根据用户ID来返回推荐列表

RS_Tags_List = ISQL.Tags_List
Food_ID_List  = set()
User_ID_List = set()

class Recommand_System():
	U_T = dict()	#用户标签字典
	F_T = dict()	#食物标签字典
	US = dict() 	#用户相似度矩阵
	FS = dict()		#食物相似度矩阵

	def __Init__(self):
		U_T = None	
		F_T = None	
		US = None 	
		FS = None
		U_T = dict()	#用户标签字典	{"user1": {"tag1": 1/0, "tag2" : 1/0} ,"user2": {"tag1": 1/0, "tag2" : 1/0} }
		F_T = dict()	#食物标签字典
		US = dict() 	#用户相似度矩阵
		FS = dict()		#食物相似度矩阵

	def Init_UT_Matrix(self):
		DB_conn =  pymysql.connect(host = 'localhost',user = 'user','password' = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		cursor = DB_conn.cursor() 

		cursor.execute(" Select * From UTs")

		rows = cursor.fetchall() 
		for row in rows:
			self.U_T[row[0]] = dict() 
			for i in range(1,len(row)):
				cursor_UserGetTag = DB_conn.cursor() 
				cursor_UserGetTag.execute("select %s from UTs where User_ID = %s" %(RS_Tags_List[i],row[0]))
				tag_weight = cursor_UserGetTag.fetchone() 
				self.U_T[row[0]][RS_Tags_List[i]] = tag_weight 
				cursor_UserGetTag.close() 

		cursor.close() 
		DB_conn.close() 

	def Init_FT_Matrix(self):
		DB_conn =  pymysql.connect(host = 'localhost',user = 'user','password' = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		cursor = DB_conn.cursor() 

		cursor.execute(" select * From FTs ")

		rows = cursor.fetchall() 

		for row in rows:
			self.F_T[row[0]] = dict() 
			for i in range(1,len(row)):
				cursor_FoodGetTag = DB_conn.cursor() 
				cursor_FoodGetTag,execute(" select %s from FTs where Food_ID = %s" %(row[i],row[0]))
				tag_weight = cursor_FoodGetTag.fetchone() 
				self.F_T[row[0]][RS_Tags_List[i]] = tag_weight
				cursor_FoodGetTag.close() 

		cursor.close() 
		DB_conn.close() 

	def Up_Tags_Weight(self,user_id,Fav_Food_ID):	#将特定用户喜欢的食物所具有的标签在UT表格中进行权重增加
		#权重增加百分比依据该用户对其有过行为的食物的数量，当该用户吃过更多食物的时候（评分行为越多），该行为对其的影响越小
        	DB_conn = pymysql.connect(host = 'localhost', user = 'user', password = ' ', db ='db', charser = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        	get_food_tags_cursor = DB_conn.cursor()
            	if(row[i+1] != 0 ):
                {
                	fav_tag_list.add(i+1)
                	Fav_Tags_Num += 1
        	}
        	get_food_tags_cursor.close()

		for up_tag_index in fav_tag_list:
    			Up_User_Tags_Weight = DB_conn.cursor()
    			Up_User_Tags_Weight.execute('update UTs set %s *= 1.5 where User_ID = user_id' %RS_Tags_List[up_tag_index])
    			Up_User_Tags_Weight.commit()
    			Up_User_Tags_Weight.close()
    
    
    	def DOWN_Tags_Weight(self,user_id,Dislike_Food):
        	DB_conn = pymysql.connect(host = 'localhost', user = 'user', password = ' ', db ='db', charser = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        	get_food_tags_cursor = DB_conn.cursor()
        
        	Unlike_tag_list = set()
        	get_food_tags = 'select * from FTs where Food_ID = %s'  %(Dislike_Food)
       		Dislike_Tags_row = get_food_tags.fetchone()
        
        	for i in range(0,len(RS_Tags_List)):
            	Unlike_tag_list.add(i+1)
    
        	get_food_tags.close()
        
        	for down_tag_index in Unlike_tag_list:
            		Down_User_Tags_Weight = DB_conn.cursor()
            		Down_User_Tags_Weight.execute(' update UTs set %s *= 0.8 where User_ID = user_id' %RS_Tags_List[down_tag_index])
           	 	Down_User_Tags_Weight.commit()
            		Down_User_Tags_Weight.close()


	def Cal_ItemCF(self):    #计算物品相似度
    	#Point: 如何给向量字典顺序加入物品各个标签的行为点数
    		ItemCF_Matrix = dict()
    		for i in range(0,len(User_ID_List)):
    
    
    	def Cal_UserCF(self):    #计算用户相似度
    
    
    	def Recommand(self,user_id):    #根据用户ID返回其推荐列表
        

        	fav_tag_list = set()
        
        	get_food_tags = ' select * from FTs where Food_ID = %s' %(Fav_Food_ID)
        	get_food_tags_cursor.execute(get_food_tags)
        	Fav_Tags_row = get_food_tags_cursor.fetchone()
        
        	Fav_Tags_Num = 0        #下次迭代中加强该过程学习function
        
        	for i in range(0,len(RS_Tags_List)):

