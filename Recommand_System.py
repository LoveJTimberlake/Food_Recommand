# coding=utf-8

#推荐系统主要后台代码

import Init_SQL as ISQL 
import math 

#功能：1.从数据库中生成User_Tags与Food_Tags的字典	2.计算User与Food的两个相似矩阵   3.针对用户喜爱的食物来调整其拥有的标签的权重   4.根据用户ID来返回推荐列表

RS_Tags_List = ISQL.Tags_List
Food_ID_Set = set()
User_ID_Set = set()
UserCF_Matrix = dict() 
ItemCF_Matrix = dict()	
Food_AveScore = dict() 


class Recommand_System():

	def __Init__(self):
		U_T = dict()	#用户标签字典	{"user1": {"tag1": 1/0, "tag2" : 1/0} ,"user2": {"tag1": 1/0, "tag2" : 1/0} }
		F_T = dict()	#食物标签字典
		Food_ID_List  = set()	#在使用前在此处初始化
		User_ID_List = set()	
		UserCF_Matrix = dict() 
		ItemCF_Matrix = dict()	
		Food_AveScore = dict() 
		for food_id in Food_ID_List:
			Food_AveScore[food_id][0] = 0	#avescore
			Food_AveScore[food_id][1] = 0	#times

		DB_conn =  pymysql.connect(host = 'localhost',user = 'user',password = '',db = 'db', charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
		Get_F_AveS = DB_conn.cursor()
		Get_F_AveS.execute("select * from F_AveS")
		rows = Get_F_AveS.fetchall()

		for row in rows:
			Food_AveScore[row['User_ID']] = row[1]
		Get_F_AveS.close()
		DB_conn.close()


		User_Fav_Food_List = dict() 
		for user_id in User_ID_List:
			User_Fav_Food_List[user_id] = set()


	def Up_Tags_Weight(self,user_id,Fav_Food_ID):	#将特定用户喜欢的食物所具有的标签在UT表格中进行权重增加
		#权重增加百分比依据该用户对其有过行为的食物的数量，当该用户吃过更多食物的时候（评分行为越多），该行为对其的影响越小
        DB_conn = pymysql.connect(host = 'localhost', user = 'mozart', password = '', db ='db', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        get_food_tags_cursor = DB_conn.cursor()
        get_food_tags_cursor.execute('select * from FTs where Food_ID = %s' %Fav_Food_ID)


        row = get_food_tags_cursor.fetchone()		#这里需要修改 使得其可以提出该食品对应的所有标签向量


        for i in range(1,len(row))
            if(row[i] != 0 ):
            	{
                fav_tag_list.add(i)
                Fav_Tags_Num += 1
        	}
        get_food_tags_cursor.close()

		for up_tag_index in fav_tag_list:
    		Up_User_Tags_Weight = DB_conn.cursor()
    		Up_User_Tags_Weight.execute('select  %s from UTs  where User_ID = %s' %(RS_Tags_List[up_tag_index-1],user_id))		#此处应为update语句 要修改
    		DB_conn.commit()
    		Up_User_Tags_Weight.close()

    	User_Fav_Food_List[user_id].add(Fav_Food_ID)
    
    
    def DOWN_Tags_Weight(self,user_id,Dislike_Food):
        DB_conn = pymysql.connect(host = 'localhost', user = 'user', password = ' ', db ='db', charset = 'utf8mb4', cursorclass = pymysql.cursors.DictCursor)
        get_food_tags_cursor = DB_conn.cursor()
        
        Unlike_tag_list = set()
        get_food_tags = 'select * from FTs where Food_ID = %s'  %(Dislike_Food)
        get_food_tags_cursor.execute(get_food_tags)
        Dislike_Tags_row = get_food_tags_cursor.fetchone()
        
        for i in range(0,len(RS_Tags_List)):
            Unlike_tag_list.add(i+1)
    
        get_food_tags_cursor.close()
        
        for down_tag_index in Unlike_tag_list:
            Down_User_Tags_Weight = DB_conn.cursor()
            Down_User_Tags_Weight.execute(' update UTs set %s *= 0.8 where User_ID = %s' %(RS_Tags_List[down_tag_index],user_id))
            Down_User_Tags_Weight.commit()
            Down_User_Tags_Weight.close()

         User_Fav_Food_List[user_id].remove(Dislike_Food)


	def Cal_ItemCF(self):    #计算物品相似度
    #Point: 如何给向量字典顺序加入物品各个标签的行为点数
    	Item_Tags = dict()
    	DB_conn = pymsql.connect(host = 'localhost', user = 'user', password = ' ', db = 'db', charset = 'utf8mb4',cursorclass = pymsql.cursors.DictCursor)
    	#生成各食物的标签向量
    	#（后面可以增加用标签占比来计算物品标签向量提高准确度）
    	for i in range(0,len(Food_ID_List)):
    		Item_Tags[Food_ID_List[i]] = dict() 
    		get_food_tags_cursor = DB_conn.cursor()

    		get_food_tags = " select * from FTs where Food_ID = %s" %Food_ID_List[i]
    		get_food_tags_cursor.execute(get_food_tags)
    		Food_Tags_row = get_food_tags_cursor.fetchone()
    		
    		for j in range(0,len(RS_Tags_List)):
    			Item_Tags[Food_ID_List[i]][RS_Tags_List[j]] = Food_Tags_row[RS_Tags_List[j]]
    		get_food_tags_cursor.close()

    	#计算相似矩阵
    	for food_i in Food_ID_List:
    		ItemCF_Matrix[food_i] = dict()
    		vector_i = Item_Tags[food_i].items()
    		for food_j in Food_ID_List:
    			if (food_i == food_j):
    				continue		#后面要改
    			else:
    				vector_j = Item_Tags[food_j].items()
    				part_result = 0
    				for i in range(0,len(vector_i)):
    					part_result += Item_Tags[food_i][i] * Item_Tags[food_j][i]
    				ItemCF_Matrix[food_i][food_j] = part_result/(sqrt(len(RS_Tags_List) * len(RS_Tags_List)))		#向量长度的计算有误
    	DB_conn.close()

    		


    def Cal_UserCF(self):    #计算用户相似度
    	#后期可采用皮尔逊相似度
    	DB_conn = pymsql.connect(host = 'localhost', user = 'user', password = ' ', db = 'db', charset = 'utf8mb4',cursorclass = pymsql.cursors.DictCursor)
    	User_Tags = dict() 

    	for i in range(0,len(User_ID_List)):
    		User_Tags[User_ID_List[i]] = dict() 
    		get_User_tags_cursor = DB_conn.cursor() 

    		get_user_tags = " select * from UTs where User_ID = %s" %User_ID_List[i]
    		get_User_tags_cursor.execute(get_user_tags)
    		User_Tags_row = get_User_tags_cursor.fetchone() 

    		for j in range(0,len(RS_Tags_List)):
    			User_Tags[User_ID_List[i]][RS_Tags_List[j]] = User_Tags_row[RS_Tags_List[j]]
    		get_User_tags_cursor.close() 

    	#计算相似矩阵
    	for user_i in User_ID_List:
    		UserCF_Matrix[user_i] = dict() 
    		vector_i = User_Tags[user_i].items() 
    		for user_j in User_ID_List:
    			if(user_i == user_j):
    				UserCF_Matrix[user_i][user_j] = 0 
    			else :
    				vector_j = User_Tags[user_j].items()
    				part_result = 0
    				for i in range(0,len(vector_i)):
    					part_result += User_Tags[user_i][i] * User_Tags[user_j][i]
    				UserCF_Matrix[user_i][user_j] = part_result/(sqrt(len(RS_Tags_List) * len(RS_Tags_List)))	#向量长度的计算有误
    	DB_conn.close()
    
    #推荐算法中用USerCF来线下计算并定时提供好推荐列表，再用ItemCF来进行当用户收藏了食物之后的实时计算

    def Recommand(self,user_id):    #根据用户ID返回其推荐列表
        #先根据用户相似度抽取相似度高的用户收藏的食物用于推荐
        UserCF_Recommand_List = list() 
        UserCF_Recommand_Set= set()
        Top_Sim_User_List = sorted(UserCF_Matrix[user_id],key = lambda item:item[1],reverse = True)
        for i in range(0,len(User_ID_List)):		#由于前期数据量不足则使用全遍历，后期数据量增大后再加入学习因子
        	if(! Top_Sim_User_List[i][1] ):
        		continue 
        	else:
        		for food in range(0,len(User_Fav_Food_List[Top_Sim_User_List[i][0]])):
        			UserCF_Recommand_Set.add(food)
        			if food in UserCF_Recommand_Set:
        				continue 
        			else:
        				UserCF_Recommand_List.append(food)

        #再根据物品相似度进行实时推荐
        Sim_Items_List = list() 
        Sim_Items_Set = set()
        for Fav_Food_ID in User_Fav_Food_List:
			part_Sim_Items_List = sorted(ItemCF_Matrix[Fav_Food_ID],key = lambda item: item[1], reverse = True)
			Sim_Items_List.extend(part_Sim_Items_List)

		Sim_Items_Recommand_List = list(set(Sim_Items_List))
		Sim_Items_List.sort(key = Sim_Items_List.index)


        #下一步先融合二表再进行根据平均分数排列
        All_Item_Recommend_List = Sim_Items_List + UserCF_Recommand_List
        Final_Item_Recommend_List = [item for item in self.Food_AveScore if item in All_Item_Recommend_List]
        return Final_Item_Recommend_List
       
    def Renew_Food_Rank_List(self):
        temp = sorted(RS.Food_AveScore,key = lambda item : item[0], reverse = True)
        RS.Food_AveScore = temp

