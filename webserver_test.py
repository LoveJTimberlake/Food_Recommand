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



def Post_Data_Test():
	url = 'http://127.0.0.1:5000/'
	values = {'id':'new_user','num':'123','tags' : ['tian','la','suan'],'food':['酸菜鱼','红皮鸭子']}
	d = json.dumps(values)
	headers =  {'Content-Type':'application/json'}
	req = requests.post(url,headers = headers,data = d)
	#res_data = urllib.urlopen(req)
	#res = res_data.read()
	print(req.text)


if __name__ == '__main__':
	Post_Data_Test()