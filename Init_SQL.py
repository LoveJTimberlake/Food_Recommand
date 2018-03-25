# coding=utf-8

from flask import Flask 
import PyMySQL

#初始化三个表格且值均为0：1.用户标签表   2.食物标签表    3.用户食物评分表    


#1.用户标签表

#先构建好整个表格
Tags_List = set()	#存储标签列表

db = PM.connect("localhost","数据库管理员ID","管理员password","数据库名称")	#doubts


cursor_1 = db.cursor()	#cursor作为数据库操作单位

DataL_Init_1 = """Create Table UTs(		
	User_ID  varChar[20]  NOT NULL,
	%s    varChar[20]  NOT NULL,	
	Primary Key('User_ID') 
	)"""%(Tags_List[0])		#创建表格关于用户及其标签。
cursor_1.execute(DataL_Init_1)
cursor_1.commit()
cursor_1.close()

for i in range(1,len(Tags_List)):
	cursor_2 = db.cursor()
	Action_1 = """
				alter table UTs add %s int
				"""%(Tags_List[i])
	cursor_2.execute(Action_1)
	cursor_2.commit()
	cursor_2.close()

#再将所有的值变为0
cursor_SelectAll = db.cursor() 
cursor_SelectAll.execute(" select * from UTs ")
rows = cursor_SelectAll.fetchall() 

for row in rows:
	for i in range(1,len(row)):
		cursor_InitSet = db.cursor()
		cursor_InitSet.execute("update UTs set %s = 0" %Tags_List[i-1])
		cursor_InitSet.commit() 
		cursor_InitSet.close()

#2.食物标签表

#先构建好整个表格
cursor_3 = db.cursor()

DataL_Init_2 = """Create Table FTs(
				Food_ID  varChar[20]  NOT NULL,
				%s  	 varChar[20]  Not NULL,
				Primary Key('Food_ID')
				)"""	%(Tags_List[0])
cursor_3.execute(DataL_Init_2)
cursor_3.commit()
cursor_3.close()

for i in range(1,len(Tags_List)):
	cursor_4 = db.cursor()
	Action_2 = """
				alter table FTs add %s int 
				"""	%Tags_List[i]

	cursor_4.execute(Action_2)
	cursor_4.commit()
	cursor_4.close() 	

#再将所有的值变为0
cursor_SelectAll = db.cursor() 
cursor_SelectAll.execute(" select * from FTs ")
rows = cursor_SelectAll.fetchall() 

for row in rows:
	for i in range(1,len(row)):
		cursor_InitSet = db.cursor() 
		cursor_InitSet.execute("update FTs set %s = 0 " % Tags_List[i-1])	
		cursor_InitSet.commit() 
		cursor_InitSet.close() 



#3.用户食物分数表
cursor_5 = db.cursor() 
DataL_Init_3 = """Create Table UFS_0(
				  User_ID	varChar[20]  NOT NULL,
				  Food_ID   varChar[20]  NOT NULL,
				  Score		varChar[20]	 NULL,
				 )"""

cursor_5.execute(DataL_Init_3)
cursor_5.commit()
cursor_5.close()


