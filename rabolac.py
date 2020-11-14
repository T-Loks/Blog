from bottle import run, route, request, response,  jinja2_template, static_file, error, redirect

import sqlite3

import mysql.connector
from mysql.connector import Error

import itertools
import statistics 
from statistics import mode

import time
import random
import os
import csv

from functions.ext import *

per_page = 8
connection = mysql.connector.connect(host='abrex.mysql.pythonanywhere-services.com', database='abrex$rabolac', user='abrex', password="zxcvb")
#connection = mysql.connector.connect(host='localhost', database='rabolac', user='root', password="zxcvb")

db_Info = connection.get_server_info()

cursor = connection.cursor(buffered=True)

cursor.execute('SELECT COUNT(*) FROM posts')
total = cursor.fetchone()

def popular():
	cursor.execute("SELECT p_id FROM comments")
	c_id_tuple = cursor.fetchall()
	
	c_id_list = [item for t in c_id_tuple for item in t]
	
	first, second, third = Nmaxelements(c_id_list, 3)
	
	return (first, second, third)
	
@route('/login')
def login():
	return jinja2_template('login')
	
@route("/cookie", method='POST')
def cookie():
	user = request.forms.get('username')
	password = request.forms.get('password')
	
	if user == 'Rabolac' and password == 'pass':
		response.set_cookie("account", 'login', secret='some-secret-key', max_age = 3600 * 24 * 5)
		redirect('http://localhost:8080/')
	else:
		return('Login failed')
	
@route("/")
@route("/<page:int>")
def home(page=0):
	#response.set_cookie("account", 'login', secret='some-secret-key', max_age = 3600 * 24 * 5)
	per = int(request.query.per or per_page)
	print('****')
	print(request.get_cookie("account", secret='some-secret-key'))
	print('****')
	
	cursor.execute('SELECT * FROM popular')
	pop_posts = cursor.fetchall()
	
	popular_posts = []
	
	for i in range(len(pop_posts)):
		cursor.execute('SELECT * FROM posts WHERE p_id = %s', (pop_posts[i][0],))
		g = cursor.fetchone()
		popular_posts.append(g)
		
	cursor.execute('SELECT COUNT(*) FROM posts ')
	total = cursor.fetchone()
	
	cursor.execute('DROP TABLE IF EXISTS search;')
	connection.commit()
	
	first, second, third = popular()
	
	cursor.execute('SELECT * FROM popular_tags ORDER BY id DESC')
	popular_tags = cursor.fetchall()
	
	start, end = (page*8), (page+1)*8
	cursor.execute('SELECT * FROM posts WHERE status = %s  ORDER BY p_id DESC LIMIT %s, 8',('post', start))
	posts = cursor.fetchall()
	
#	if total[0] <= 8:
#		start, end = (page*8), (page+1)*8
#		print (start,end)
#		cursor.execute('SELECT * FROM posts WHERE p_id >= %s AND p_id < %s ORDER BY p_id DESC',(start, end))
#		posts = cursor.fetchall()
#		
#	elif total [0] > 8:
#		start, end = total [0]-(page*8), total [0]-((page+1)*8)
#		print (start,end)
#		cursor.execute('SELECT * FROM posts WHERE p_id <= %s AND p_id > %s ORDER BY p_id DESC',(start, end))
#		posts = cursor.fetchall()
	
	home = "http://localhost:8080"
			
	parameters = {
			'popular_tags': popular_tags,
			'popular_posts': popular_posts, 
			'home': home, 
			'page': page,
			'posts': posts, 
			'has_next': end < total[0],  
			'query_string': '?'+request.query_string,
            }
		
	return jinja2_template("blog",**parameters)



@route("/editor")
def home():
	if request.get_cookie("account", secret='some-secret-key'):
		parameters = {
			'x': '',
			'all': '',
			'home': 'http://localhost:8080'
		}
		return jinja2_template("editor", **parameters)
	else:
		return('denied')
	
	
@route("/editor/<id>/<file>/<status>")
def home(id, file, status):
	if request.get_cookie("account", secret='some-secret-key'):
		cursor.execute('SELECT * FROM posts WHERE p_id = %s AND fle = %s',(id, file))
		all = cursor.fetchone()
	
		cursor.execute('SELECT * FROM tags WHERE p_id = %s',(id, ))
		tx = cursor.fetchall()
	
		tag = ""
		for b in range(len(tx)):
			y = tx[b]
			tag= tag+y[1]+" "
	
		file1 = open('./'+status+'/'+file+'.txt',"r")#read mode 
		x = file1.read()
		file1.close()
		
		return jinja2_template("editor",x=x, tag=tag, all = all, home = 'http://localhost:8080')



@route('/editor', method='POST')
def do_save():
	if request.get_cookie("account", secret='some-secret-key'):
		title = request.forms.get('title')
		author = request.forms.get('author')
		header = request.files.get('header')
		catch = request.forms.get('summary')
		text = request.forms.get('txt_save')
		tags = request.forms.get('tags')
	
		header_img = str(header)
		file =title.replace(" ","-")
		fle = file
		file = file+'.txt'
	
		cursor.execute("SELECT * FROM posts WHERE file = %s", (file, ))
		mij = cursor.fetchone()
		if os.path.isfile('./draft/'+file) == True:
			os.remove('./draft/images/'+mij[9])
			os.remove('./draft/'+file)
			cursor.execute('DELETE FROM posts WHERE p_id = %s AND file = %s', (mij[0], file))
			connection.commit()
		
		if os.path.isfile('./post/'+file) == True:
			os.remove('./post/images/'+mij[9])
			os.remove('./post/'+file)
			cursor.execute('DELETE FROM posts WHERE p_id = %s AND file = %s', (mij[0], file))
			connection.commit()
	
	
	
		hour = time.strftime("%H")
		minute = time.strftime("%M")
		month = time.strftime("%B")
		day = time.strftime("%d")
		year = time.strftime("%Y")
	
	
		file1 = open('./post/'+file,"w")#write mode 
		file1.write(str(text))
		file1.close()
	
		size = int(round(os.path.getsize('./post/'+file)/1024))
	
		cursor.execute('INSERT INTO posts (author, title, file, hour, minute, month, day, year, header_img_url, catch, fle, status, size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (author, title, file, hour, minute, month, day, year, header.filename, catch, fle, 'post', size))
		connection.commit()
	
		j = '0'
		cursor.execute("SELECT p_id FROM posts ORDER BY p_id DESC")
		p_id = cursor.fetchone()
		for i in p_id:
			j = i
		
		tags = list(tags.split(" "))
		for t in tags:
			cursor.execute('INSERT INTO tags (p_id, tags) VALUES (%s, %s)', (j, t))
			connection.commit()
	
	
		name, ext = os.path.splitext(header.filename)
		if ext not in ('.png','.jpg','.jpeg'):
			return 'File extension not allowed.'
	
		#save_path = (category)
		header.save('./post/images', overwrite=True) # appends upload.filename automatically
		redirect('http://localhost:8080')


@route('/editor/draft', method="POST")
def do_save_draft():
	title = request.forms.get('title')
	author = request.forms.get('author')
	header = request.files.get('header')
	catch = request.forms.get('summary')
	text = request.forms.get('txt_save')
	tags = request.forms.get('tags')
	
	h = header.filename
	
	header_img = str(header)
	file =title.replace(" ","-")
	fle = file
	file = file+'.txt'
	
	if os.path.isfile('./draft/'+file) == True:
		cursor.execute("SELECT * FROM posts WHERE p_id = %s", (id, ))
		mij = cursor.fetchone()
		os.remove('./draft/images/'+mij[9])
		os.remove('./draft/'+mij[3])
	
		cursor.execute('DELETE FROM posts WHERE p_id = %s AND file = %s', (id, file))
		connection.commit()
	
	
	file1 = open('./draft/'+file,"w")#write mode 
	file1.write(str(text))
	file1.close()
  
	name, ext = os.path.splitext(header.filename)
	if ext not in ('.png','.jpg','.jpeg'):
		return 'File extension not allowed.'
		
	header.save('./draft/images', overwrite=True)
	
	hour = time.strftime("%H")
	minute = time.strftime("%M")
	month = time.strftime("%B")
	day = time.strftime("%d")
	year = time.strftime("%Y")
	
	size = int(os.path.getsize('./draft/'+file)/1024)
	
	cursor.execute('INSERT INTO posts (author, title, file, hour, minute, month, day, year, header_img_url, catch, fle, status, size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (author, title, file, hour, minute, month, day, year, header.filename, catch, fle, 'draft', size))
	connection.commit()
	
	j = '0'
	cursor.execute("SELECT p_id FROM posts ORDER BY p_id DESC")
	p_id = cursor.fetchone()
	for i in p_id:
		j = i
		
	tags = list(tags.split(" "))
	for t in tags:
		cursor.execute('INSERT INTO tags (p_id, tags) VALUES (%s, %s)', (j, t))
		connection.commit()
	
	redirect('http://localhost:8080')


@route("/<post>")
def post(post):
	cursor.execute('SELECT * FROM popular')
	pop_posts = cursor.fetchall()
	
	popular_posts = []
	
	for i in range(len(pop_posts)):
		cursor.execute('SELECT * FROM posts WHERE p_id = %s', (pop_posts[i][0],))
		g = cursor.fetchone()
		popular_posts.append(g)
	
	tt = post
	post_name = tt+'.txt'
	
	fiu = open('./post/'+tt+'.txt', "r+")
	xx = fiu.read()
	
	cursor.execute('SELECT * FROM posts WHERE file = %s',(post_name,))
	pst = cursor.fetchall()
	id = pst[0]
	
	cursor.execute('SELECT * FROM comments WHERE p_id = %s',(id[0], ))
	comments = cursor.fetchall()
	
	cursor.execute('SELECT * FROM tags WHERE p_id = %s',(id[0],))
	tags = cursor.fetchall()
	
	
	
	parameters = {
			'home': 'http://localhost:8080',
			'popular_posts': popular_posts, 
			'tt': tt,
			'id': id, 
			'xx': xx, 
			
			'pst': pst, 
			'comments': comments,
			'tags': tags
	}
	
	return jinja2_template("post", **parameters)


@route('/<post>', method='POST')
def comment(post):
	p_id =  request.forms.get('p_id')
	content = request.forms.get('comment')
	author = request.forms.get('author')
	tt = post
	
	
	hour = time.strftime("%H")
	minute = time.strftime("%M")
	month = time.strftime("%B")
	day = time.strftime("%d")
	year = time.strftime("%Y")
	
	cursor.execute('INSERT INTO comments (p_id, author, content, hour, minute, month, day, year) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s);', (p_id, author, content, hour, minute, month, day, year))
	
	connection.commit()
	
	
	cursor.execute('SELECT * FROM posts WHERE p_id = %s',(p_id,))
	pst = cursor.fetchone()
	
	
	cursor.execute('SELECT * FROM comments WHERE p_id = %s',(p_id, ))
	comments = cursor.fetchall()
	
	cursor.execute('SELECT * FROM tags WHERE p_id = %s',(p_id,))
	tags = cursor.fetchall()
	
	parameters = {
			'home': 'http://localhost:8080',
			'id': p_id, 
			'tt': tt,
			'pst': pst, 
			'comments': comments,
			'tags': tags
	}
	
	redirect('../'+tt)
	

@route("/search/handler", method='POST')
def search_handler():
	query = str(request.forms.get("query"))
	url = '../query/'+query
	redirect(url)
	
@route("/query/<query>")
@route("/query/<query>/<page:int>")
def search(query, page=0):
	cursor.execute('DROP TABLE IF EXISTS search;')
	se = '%'+query+'%'
	per = int(request.query.per or per_page)
	
	cursor.execute("CREATE TABLE IF NOT EXISTS search (p_id INT AUTO_INCREMENT PRIMARY KEY, author VARCHAR(255) NOT NULL, title VARCHAR(255) NOT NULL, file VARCHAR(255) NOT NULL, hour VARCHAR(255) NOT NULL, minute VARCHAR(255) NOT NULL, month VARCHAR(255) NOT NULL, day VARCHAR(255) NOT NULL, year VARCHAR(255) NOT NULL, header_img_url VARCHAR(255) NOT NULL, catch VARCHAR(255) NOT NULL, fle VARCHAR(255) NOT NULL);")

	connection.commit()
	
	cursor.execute("SELECT * FROM posts WHERE  title LIKE %s ORDER BY p_id DESC",(se, ))
	posts = cursor.fetchall()
	
	for p in posts:
		cursor.execute('INSERT INTO search ( author, title, file, hour, minute, month, day, year, header_img_url, catch, fle) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]))
		connection.commit()
	
	cursor.execute('SELECT COUNT(*) FROM search WHERE title LIKE %s ORDER BY p_id DESC',(se, ))
	cnt = cursor.fetchone()
	
	cursor.execute('SELECT * FROM popular')
	pop_posts = cursor.fetchall()
	
	popular_posts = []
	for i in range(len(pop_posts)):
		cursor.execute('SELECT * FROM posts WHERE p_id = %s', (pop_posts[i][0],))
		g = cursor.fetchone()
		popular_posts.append(g)
	
	start, end = page*8, (page+1)*8
	
	cursor.execute('SELECT * FROM search WHERE p_id >= %s AND p_id < %s AND title LIKE %s ORDER BY p_id ASC',(start, end, se))
	posts = cursor.fetchall()
	
	#keys = ('id', 'name') 
	#posts = (dict(zip(keys, post)) for post in posts)
	
	home = "http://localhost:8080"
			
	parameters = {
			'home': 'http://localhost:8080',
			'popular_posts': popular_posts, 
			'query': query, 
			'cnt': cnt, 
			'home': home, 
			'page': page,
			'posts': posts, 
			'has_next': end <= cnt[0],  
			'query_string': '?'+request.query_string,
            }
	return jinja2_template("query", **parameters)


@error(404)
@error(500)
def error404(error):
	cursor.execute('DROP TABLE IF EXISTS search;')
	connection.commit()
	cursor.execute('SELECT * FROM popular')
	pop_posts = cursor.fetchall()
	
	popular_posts = []
	
	for i in range(len(pop_posts)):
		cursor.execute('SELECT * FROM posts WHERE p_id = %s', (pop_posts[i][0],))
		g = cursor.fetchone()
		popular_posts.append(g)
	
	return jinja2_template("404", popular_posts=popular_posts, home
	 = 'http://localhost:8080')


@route("/dashboard")
@route("/dashboard/<page:int>")
def dashboard (page=0):
	if request.get_cookie("account", secret='some-secret-key'):
		home = "http://localhost:8080"
	
		start, end = page * 2, (page+1)*2
		cursor.execute('SELECT * FROM posts ORDER BY p_id DESC LIMIT %s, 2', (start,))
		posts = cursor.fetchall()
	
		cursor.execute('SELECT COUNT(*) FROM posts')
		count = cursor.fetchone()
	
		cursor.execute('SELECT * FROM popular ORDER BY id DESC')
		popular_posts = cursor.fetchall()
	
		cursor.execute('SELECT * FROM popular_tags ORDER BY id DESC')
		popular_tags = cursor.fetchall()
	
		cursor.execute('SELECT COUNT(*) FROM popular_tags ORDER BY id DESC')
		popular_tags_count = cursor.fetchone()
	
		cursor.execute('SELECT COUNT(*) FROM popular ORDER BY id DESC')
		popular_post_count = cursor.fetchone()
	
	
	
		parameters={
			'home': home,
			'page': page,
			'posts': posts,
			'popular_tags': popular_tags,
			'popular_posts': popular_posts,
			'count': popular_post_count,
			'addable': popular_post_count[0] <=3,
			'tag_addable': popular_tags_count[0] <= 23,
			'has_next': end < count[0]
		}
	
		return jinja2_template("dashboard", **parameters)

@route("/delete/<file>/<id>")
def delete (id, file):
	if request.get_cookie("account", secret='some-secret-key'):
		data = request.forms.get('title')
		cursor.execute('SELECT * FROM posts WHERE p_id = %s',(id,))
		delete = cursor.fetchone()
	
		if os.path.isfile('./'+delete [12]+'/images'+delete[9]) == True and os.path.isfile('./'+delete [12]+'/'+delete[3]) == True:
			os.remove('./'+delete[12]+'/images/'+delete[9])
			os.remove('./'+delete[12]+'/'+delete[3])
	
		cursor.execute('DELETE FROM posts WHERE p_id = %s AND title = %s', (id, file))
		connection.commit()
		redirect ('../../dashboard')
	else:
		return('ACCESS DENIED')



@route("/add-popular", method="POST")
def add_popular():
	if request.get_cookie("account", secret='some-secret-key'):
		id = str(request.forms.get('id'))
		cursor.execute("SELECT * FROM posts WHERE p_id = %s",(id,))
		y = cursor.fetchone()
	
		cursor.execute("INSERT INTO popular (id, title) VALUES (%s, %s)",(id, y[2]))
		redirect("../dashboard")
	else:
		redirect('../')


@route("/<id>/del-popular")
def del_popular(id):
	if request.get_cookie("account", secret='some-secret-key'):
		cursor.execute("DELETE FROM popular WHERE id = %s",(id,))
		connection.commit()
	
		redirect("../dashboard")
	else:
		redirect('../../')


@route("/add-popular-tag", method="POST")
def add_popular():
	id = str(request.forms.get('id'))
	
	cursor.execute("INSERT INTO popular_tags ( tag) VALUES (%s)",(id,))
	redirect("../dashboard")


@route("/<tag>/del-popular-tag")
def del_popular(tag):
	if request.get_cookie("account", secret='some-secret-key'):
		cursor.execute("DELETE FROM popular_tags WHERE tag = %s",(tag,))
		connection.commit()
	
		redirect("../dashboard")
	

@route('/generate')
def generate():
	if request.get_cookie("account", secret='some-secret-key'):
		cursor.execute('SELECT * FROM subscription_list')
		total = cursor.fetchall()
		print(total)
		fields = ['email']

		rows = total
		filename = "./csv/records.csv"

		with open(filename, 'w') as csvfile:  
			csvwriter = csv.writer(csvfile)  
			csvwriter.writerow(fields)
			csvwriter.writerows(rows) 
		redirect ("../download/records.csv")
	else:
		redirect("../../")
		
		
@route("/sub", method="POST")
def subscription():
	email= request.forms.get("email")
	cursor.execute('INSERT INTO subscription_list (email) VALUES (%s)', (email,))
	connection.commit()
	redirect('../')
	
@route('/download/<filename:path>')
def download(filename):
	if request.get_cookie("account", secret='some-secret-key'):
		return static_file(filename, root='./csv', download=filename)
		redirect ('../../dashboard')
	else:
	   redirect ("./$$56__56&&56&&66;-66--3__")
    
    
@route("/css/<filepath:path>")
def logo(filepath):
	return static_file(filepath, root="./css")

@route("/js/<filepath:path>")
def logo(filepath):
	return static_file(filepath, root="./js")


@route("/images/<filepath:path>")
def logo(filepath):
	return static_file(filepath, root="./images")

@route("/post/<filepath:path>")
def logo(filepath):
	return static_file(filepath, root="./post")

@route("/post/images/<filepath:path>")
def logo(filepath):
	return static_file(filepath, root="./post/images")

@route("/draft/<filepath:path>")
def logo(filepath):
	return static_file(filepath, root="./draft")

@route("/draft/images/<filepath:path>")
def logo(filepath):
	return static_file(filepath, root="./draft/images")
	
@route("/About")
def about():
	cursor.execute('SELECT * FROM popular')
	pop_posts = cursor.fetchall()
	
	popular_posts = []
	
	for i in range(len(pop_posts)):
		cursor.execute('SELECT * FROM posts WHERE p_id = %s', (pop_posts[i][0],))
		g = cursor.fetchone()
		popular_posts.append(g)
		
	cursor.execute('DROP TABLE IF EXISTS search;')
	connection.commit()
	
	cursor.execute('SELECT * FROM popular_tags ORDER BY id DESC')
	popular_tags = cursor.fetchall()
	
	parameters = {
		'popular_posts': popular_posts,
		'popular_tags': popular_tags,
		'home': 'http://localhost:8080'
	}
	
	return jinja2_template("about", **parameters)
	
@route("/support")
def about():
	cursor.execute('SELECT * FROM popular')
	pop_posts = cursor.fetchall()
	
	popular_posts = []
	
	for i in range(len(pop_posts)):
		cursor.execute('SELECT * FROM posts WHERE p_id = %s', (pop_posts[i][0],))
		g = cursor.fetchone()
		popular_posts.append(g)
		
	cursor.execute('DROP TABLE IF EXISTS search;')
	connection.commit()
	
	cursor.execute('SELECT * FROM popular_tags ORDER BY id DESC')
	popular_tags = cursor.fetchall()
	
	parameters = {
		'popular_posts': popular_posts,
		'popular_tags': popular_tags,
		'home': 'http://localhost:8080'
	}
	return jinja2_template("support", **parameters)
	
@route("/contact")
def about():
	cursor.execute('SELECT * FROM popular')
	pop_posts = cursor.fetchall()
	
	popular_posts = []
	
	for i in range(len(pop_posts)):
		cursor.execute('SELECT * FROM posts WHERE p_id = %s', (pop_posts[i][0],))
		g = cursor.fetchone()
		popular_posts.append(g)
		
	cursor.execute('DROP TABLE IF EXISTS search;')
	connection.commit()
	
	cursor.execute('SELECT * FROM popular_tags ORDER BY id DESC')
	popular_tags = cursor.fetchall()
	
	parameters = {
		'popular_posts': popular_posts,
		'popular_tags': popular_tags,
		'home': 'http://localhost:8080'
	}
	return jinja2_template("contact", **parameters)
	
@route("/write-for-us")
def about():
	cursor.execute('SELECT * FROM popular')
	pop_posts = cursor.fetchall()
	
	popular_posts = []
	
	for i in range(len(pop_posts)):
		cursor.execute('SELECT * FROM posts WHERE p_id = %s', (pop_posts[i][0],))
		g = cursor.fetchone()
		popular_posts.append(g)
		
	cursor.execute('DROP TABLE IF EXISTS search;')
	connection.commit()
	
	cursor.execute('SELECT * FROM popular_tags ORDER BY id DESC')
	popular_tags = cursor.fetchall()
	
	parameters = {
		'popular_posts': popular_posts,
		'popular_tags': popular_tags,
		'home': 'http://localhost:8080'
	}
	return jinja2_template("write-for-us", **parameters)
	

	


run(reloader = True, debug = True)