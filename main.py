from bottle import run,route,jinja2_template,get,post,response,static_file,error,request,template,redirect
import bottle

import os
import sqlite3

app = bottle.Bottle()

@route("/login")
def login():
	response.delete_cookie("account",secret="zyber")
	return jinja2_template('''
	  <!DOCTYPE html>
    <html>
    <head>
    <title>Login:.script</title>
    <meta name="viewport" content="width=device-width; initial-scale= 1.0;">
    </head>
    <body>
    <h3 style="text-align:center;">LOGIN</h3>
    
    <p style="font-size:0.5em;text-align:center;">Admin</p>
    <div class=container style="align:center;padding:8px;border:1px solid #ccc;border-color:black;background-color:#f1f1f1;">
    <form method='post' action="/conf">
    
    <label style="font-size:0.5em;"><b>Username</b></label><br>
    <input type="text" placeholder="Enter username" name="use_name" required style="height:18px;width:95%;padding:6px 10px;margin:4px 0;border:1px solid #ccc;box-styling:border-box;font-size:10px;">
    
    <br>
    
    <label style="font-size:0.5em;"><b>Password</b></label><br>
    <input type="password" placeholder="Enter password" name="usr_pass" required style="height:18px;width:95%;padding:6px 10px;margin:4px 0;border:1px solid #ccc;box-styling:border-box;font-size:10px;">
    <hr style="height:5px;color:#141414">
    <input value="Login" type="submit" style="height:auto;width:99%;padding:5px 9px;background-color:#4CAF50;font-size:7.5px;">
    </form>
    </div>
    
    	<footer style="text-align:center;background-color:#141414;color:#f1f1f1;font-size:10px;">
	<div style="height:auto;">
	<nav class="navigation">
	<p style="color:grey;">All Rights Reserved</p>
	<p>2018.</p>
	</nav>
	</div>
	</footer>
    </body>
    </html>
    ''')


	
@route("/conf",method=['get','post'])
def index():
	password = request.forms.get("usr_pass")
	username = request.forms.get("use_name")
	
	conn = sqlite3.connect("shoplog")
	c = conn.cursor()
	c.execute("select * from usr")
	x = c.fetchall()
	
	for y in x:
		if username == y[0] and password == y[4]:
			response.set_cookie("account",username,secret="zyber",max_age=90000)
			conv=request.get_cookie("account",secret="zyber")
			redirect("/")
		else:
			redirect("/login")


@route('/image-upload')
def image_upload():
	return jinja2_template('''
	<!DOCTYPE html>
				<html>
				<head>
				
				<style>
				.overlay-content {
				position: relative;
				top: 15%;
				width: 100%;
				text-align: center;
				margin-top: 30px;
				}
				
				ul { list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #fff; top: 0;font-size:7px}
				li { float: left; }
				li a { display: block; color: block; text-align: center; padding: 7px 8px; text-decoration: none; }
				li a:hover:not(.active) { background-color: turquoise; }
				.active { background-color: steelblue; } 
				</style>
				
				<meta name="viewport" content="width=device-width; initial-scale= 1.0;">
				</head>
				
				<body>

<div style="text-align:center;background-color:#000;">

<div>
<ul style="background-color:black;">
<li class="active"><a href="/">Home</a></li>
<li><a href="upload">Upload</a></li>
<li><a href="/login">Logout</a></li>
</ul>
</div>

<h1 style="color:purple;">Anchor Blog</h1>

<div>
<ul style="list-style-type: none; margin: 0; padding: 0; overflow: hidden; top: 0; width: 100%; font-size:8px;text-align:center;">

<li><a href="/">Home</a></li>
<li><a href="/tag/entertainment">Entertainment</a></li>
<li><a href="/tag/technology">Technology</a></li>
<li><a href="/tag/sports">Sports</a></li>
<li><a href="/tag/finance">Finance</a></li>
<li><a href="/tag/foreign">Foreign</a></li>
</ul>
</div>

<form action="/search" method="post">
<div class="overlay-content">
		<input type="text" style="width:70%;padding:6px 0px;margin:4px 0;border:2px solid orange;box-styling:border-box;border-radius:20px;font-size:0.5em;" name="search"/>
		
		<input type="submit" style="height:auto;width:30%;background-color:gold;border-radius:1em;padding:6px 10px;font-size:10px;" value="search">
</div>
</form>
</div>
   
   
   <form action="/image-upl" method="POST" enctype="multipart/form-data"/>
   
   <p>Choose a picture: </p>
   <input type="file" name="pic_1" />
   
   <p>Choose a picture: </p>
   <input type="file" name="pic_2" />
   
   <p>Choose a picture: </p>
   <input type="file" name="pic_3" />
   
   <p>Choose a picture: </p>
   <input type="file" name="pic_4" />
   
      <br>
   
   <div class="overlay-content">
   <input type="submit" style="height:auto;width:30%;background-color:gold;border-radius:1em;padding:6px 10px;color:blue" value="upload">
   </div>
   
   <hr color=#000000>
   </div>
   </form>
   <hr color=#000000>
   
   <nav>
   <footer style="text-align:center;background-color:#141414;color:#f1f1f1;font-size:10px;">
	<div style="height:auto;">
	<nav class="navigation">
	<p style="color:grey;">All Rights Reserved</p>
	<p>2018.</p>
	</nav>
	</div>
	</footer>
   </body>
   </html>
   ''')
	

@route('/image-upl',method='post')
def image_upl():
	pic_1 = request.forms.get('pic_1')
	upli = request.files.get('pic_1')
	
	pic_2= request.forms.get('pic_2')
	uplii = request.files.get('pic_2')
	
	pic_3 = request.forms.get('pic_3')
	upliii = request.files.get('pic_3')
	
	pic_4= request.forms.get('pic_4')
	upliv= request.files.get('pic_4')
	
	images = [upli,uplii,upliii,upliv]
	i,ext1=os.path.splitext(upli.filename)
	ii,ext2=os.path.splitext(uplii.filename)
	iii,ext3=os.path.splitext(upliii.filename)
	iv,ext4=os.path.splitext(upliv.filename)
	save_path = "./images"
	upli.save('./images/',overwrite=True)
	uplii.save('./images/',overwrite=True)
	upliii.save('./images/',overwrite=True)
	upliv.save('./images/',overwrite=True)
	
	
	name = [i,ii,iii,iv]
	extension = [ext1,ext2,ext3,ext4]
	
	list = []
	conn = sqlite3.connect('shoplog')
	c = conn.cursor()
	for i in name:
		for j in extension:
			ds = i+j
			list.append(ds)
		
	k = -5
	while k != len(list)-1:
		d = list[k+5]
		k=k+5
		conn = sqlite3.connect('shoplog')
		c = conn.cursor()
		c.execute("INSERT INTO images VALUES (?)",(d,))		
		conn.commit()
		conn.close()
			
@route("/upload")
def upload():
	conv = request.get_cookie('account',secret='zyber')
	if conv:
		return jinja2_template('''
		<!DOCTYPE html>
				<html>
				<head>
				
				<style>
				.overlay-content {
				position: relative;
				top: 15%;
				width: 100%;
				text-align: center;
				margin-top: 30px;
				}
				
				ul { list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #fff; top: 0;font-size:7px}
				li { float: left; }
				li a { display: block; color: block; text-align: center; padding: 7px 8px; text-decoration: none; }
				li a:hover:not(.active) { background-color: turquoise; }
				.active { background-color: steelblue; } 
				</style>
				
				<meta name="viewport" content="width=device-width; initial-scale= 1.0;">
				</head>
				
				<body>

<div style="text-align:center;background-color:#000;">

<div>
<ul style="background-color:black;">
<li><a href="/">Home</a></li>
<li class="active"><a href="upload">Upload</a></li>
<li><a href="/login">Logout</a></li>
</ul>
</div>

<h1 style="color:purple;">Anchor Blog</h1>

<div>
<ul style="list-style-type: none; margin: 0; padding: 0; overflow: hidden; top: 0; width: 100%; font-size:8px;text-align:center;">

<li><a href="/">Home</a></li>
<li><a href="/tag/entertainment">Entertainment</a></li>
<li><a href="/tag/technology">Technology</a></li>
<li><a href="/tag/sports">Sports</a></li>
<li><a href="/tag/finance">Finance</a></li>
<li><a href="/tag/foreign">Foreign</a></li>
</ul>
</div>

<form action="/search" method="post">
<div class="overlay-content">
		<input type="text" style="width:70%;padding:6px 0px;margin:4px 0;border:2px solid orange;box-styling:border-box;border-radius:20px;font-size:0.5em;" name="search"/>
		
		<input type="submit" style="height:auto;width:30%;background-color:gold;border-radius:1em;padding:6px 10px;font-size:10px;" value="search">
</div>
</form>
</div>
   
   
   <form action="/upl" method="POST" enctype="multipart/form-data"/>
   
   <p>Title: </p>
   <input type="text" style="width:50%;padding:6px 0px;margin:4px 0;border:2px solid #000;box-styling:border-box;border-radius:20px;" name="topic" required />
   
   <p>Post: </p>
   <textarea style="width:95%;height:50em;padding:6px 0px;margin:4px 0;border:2px solid #000;box-styling:border-box;border-radius:20px;"  name="post" required />
   </textarea>
   
   
   <label>Category: </label>
   <select name="category">
		<option value="entertainment">Entertainment</option>
		<option value="technology">Technology</option>
		<option value="sports">Sports</option>
		<option value="finance">Finance</option>
			<option value="foreign">Foreign</option>
	</select>
	
   <br>
   <br>
   
   <div class="overlay-content">
   <input type="submit" style="height:auto;width:30%;background-color:gold;border-radius:1em;padding:6px 10px;color:blue" value="upload">
   </div>
   
   <hr color=#000000>
   </div>
   </form>
   <hr color=#000000>
   
   <nav>
   <footer style="text-align:center;background-color:#141414;color:#f1f1f1;font-size:10px;">
	<div style="height:auto;">
	<nav class="navigation">
	<p style="color:grey;">All Rights Reserved</p>
	<p>2018.</p>
	</nav>
	</div>
	</footer>
   </body>
   </html>
	''')
	else:
		redirect("/login")
	

@route("/upl",method="post")
def upl():
	conv = request.get_cookie("account",secret="zyber")
	
	topic = request.forms.get('topic')
	post = request.forms.get('post')
	category = request.forms.get('category')
	
	
	conn = sqlite3.connect('shoplog')
	c = conn.cursor()
	num = c.execute("select * from post where topic == ? and post == ?",(topic,post)).fetchall()
	num = len(num)
	if num >= 1:
		return jinja2_template('''
		<!DOCTYPE html>
				<html>
				<head>
				
				<style>
				.overlay-content {
				position: relative;
				top: 15%;
				width: 100%;
				text-align: center;
				margin-top: 30px;
				}
				
				ul { list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #fff; top: 0;font-size:9px}
				li { float: left; }
				li a { display: block; color: block; text-align: center; padding: 7px 8px; text-decoration: none; }
				li a:hover:not(.active) { background-color: turquoise; }
				.active { background-color: steelblue; } 
				</style>
				
				<meta name="viewport" content="width=device-width; initial-scale= 1.0;">
				
				<title>Upload</title>
				</head>
				
				<body>

<div style="text-align:center;background-color:#000;">

{%if conv%}
<div>
<ul style=background-color:black;>
<li><a href="/">Home</a></li>

<li><a href="upload">Upload</a></li>
<li><a href="/login">Logout</a></li>
</ul>
</div>
{%endif%}

<h1 style="color:purple;">Anchor Blog</h1>

<div>
<ul style="list-style-type: none; margin: 0; padding: 0; overflow: hidden; top: 0; width: 100%; font-size:8px;text-align:center;">

<li><a href="/">Home</a></li>
<li><a href="/tag/entertainment">Entertainment</a></li>
<li><a href="/tag/technology">Technology</a></li>
<li><a href="/tag/sports">Sports</a></li>
<li><a href="/tag/finance">Finance</a></li>
<li><a href="/tag/foreign">Foreign</a></li>
</ul>
</div>

<form action="/search" method="post">
<div class="overlay-content">
		<input type="text" style="width:70%;padding:6px 0px;margin:4px 0;border:2px solid orange;box-styling:border-box;border-radius:20px;font-size:0.5em;" name="search"/>
		
		<input type="submit" style="height:auto;width:30%;background-color:purple;border-radius:1em;padding:6px 10px;font-size:10px;" value="search">
</div>
</form>
</div>

<hr color='red'>
<br>

<p style="font-size:3em;text-align:center;"><i>OOPS SEEMS YOU`VE ALREADY POSTED THIS</i></p>

  <nav>
   <footer style="text-align:center;background-color:#141414;color:#f1f1f1;font-size:10px;">
	<div style="height:auto;">
	<nav class="navigation">
	<p style="color:grey;">All Rights Reserved</p>
	<p>2018.</p>
	</nav>
	</div>
	</footer>
</nav>

</body>
</html>
		''',conv=conv)
	else:
		c.execute("INSERT INTO post VALUES (?,?,?)",(topic,post,category))		
	conn.commit()
	conn.close()
		
	redirect("/")




PER_PAGE = 15

@route("/")
@route("/<page:int>")
def home(page=0):
	conn = sqlite3.connect("shoplog")
	c = conn.cursor()
	
	ACTIVITY_TOTAL,=c.execute('SELECT COUNT(*) FROM post').fetchone()
	per = PER_PAGE
	start, end = ACTIVITY_TOTAL-(page *per), ACTIVITY_TOTAL-((page + 1)*per)
	
	c.execute("select * from post where rowid <= ? and rowid >= ? order by rowid DESC",(start,end))
	all = c.fetchall()
	
	parameters = {
		'start':start,
		'end':end,
		'page' : page,
		'all' : all,
		'ACTIVITY_TOTAL':ACTIVITY_TOTAL,
		'has_next' : end > 0,
		'query_string' : request.query_string,
		}
	conv=request.get_cookie("account",secret="zyber")
	return jinja2_template('''
		<!DOCTYPE html>
				<html>
				<head>
				
				<style>
				.overlay-content {
				position: relative;
				top: 15%;
				width: 100%;
				text-align: center;
				margin-top: 30px;
				}
				
				ul { list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #fff; top: 0;font-size:9px}
				li { float: left; }
				li a { display: block; color: block; text-align: center; padding: 7px 8px; text-decoration: none; }
				li a:hover:not(.active) { background-color: turquoise; }
				.active { background-color: steelblue; } 
				</style>
				
				<meta name="viewport" content="width=device-width; initial-scale= 1.0;">
				
				<title>Anchor blog</title>
				</head>
				
				<body>

<div style="text-align:center;background-color:#000;">

{%if conv%}
<div>
<ul style=background-color:black;>
<li class="active"><a href="/">Home</a></li>

<li><a href="upload">Upload</a></li>
<li><a href="/login">Logout</a></li>
</ul>
</div>
{%endif%}

<h1 style="color:purple;">Anchor Blog</h1>

<div>
<ul style="list-style-type: none; margin: 0; padding: 0; overflow: hidden; top: 0; width: 100%; font-size:8px;text-align:center;">

<li><a href="/">Home</a></li>
<li><a href="/tag/entertainment">Entertainment</a></li>
<li><a href="/tag/technology">Technology</a></li>
<li><a href="/tag/sports">Sports</a></li>
<li><a href="/tag/finance">Finance</a></li>
<li><a href="/tag/foreign">Foreign</a></li>
</ul>
</div>

<form action="/search" method="post">
<div class="overlay-content">
		<input type="text" style="width:70%;padding:6px 0px;margin:4px 0;border:2px solid orange;box-styling:border-box;border-radius:20px;font-size:0.5em;" name="search"/>
		
		<input type="submit" style="height:auto;width:30%;background-color:purple;border-radius:1em;padding:6px 10px;font-size:10px;" value="search">
</div>
</form>
</div>

<hr color='red'>
<br>
{%for y in all%}
<h6 style="text-align:center;"><a style="text-decoration:none;color:#000;" href="/{{y[0]}}">{{y[0]}}</a></h6><hr color="black">
{%endfor%}

	<nav>
	{% if page > 0%}
		{% if page == 1 %}
			<form action= "/" />
			<input value="Prev" type="submit" style="height:auto;width:30%;padding:5px 9px;background-color:#4CAF50;font-size:0.5em;float:left;">
			</form>
		{% else %}
			<form action= "./{{ page-1 }}" >
			<input value="Prev" type="submit" style="height:auto;width:30%;padding:5px 9px;background-color:#4CAF50;font-size:0.5em;float:left;">
			</form>
		{% endif %}
	{% endif %}
	{% if has_next %}
	<form action ="./{{ page+1 }}" >
	<input value="Next" type="submit" style="height:auto;width:30%;padding:5px 9px;background-color:#4CAF50;font-size:0.5em;float:right;">
	</form>
	{% endif %}
	</nav>
	
	</div>
	<br>
	<footer style="text-align:center;background-color:#141414;color:#f1f1f1;font-size:10px;">
	<div>
	<nav class="navigation">
	<p style="color:grey;">All Rights Reserved</p>
	<p>2018.</p>
	</nav>
	</div>
	</footer>
	</body>
	</html>
</body>
</html>
	''',conv=conv,**parameters)
	

@route("/<topic>")
def topic(topic):
	conv = request.get_cookie("account",secret="zyber")
	
	conn = sqlite3.connect("shoplog")
	c = conn.cursor()
	c.execute("select * from post where topic == ?",(topic,))
	post = c.fetchall()
	conn.close()
	
	
	conn = sqlite3.connect("shoplog")
	c = conn.cursor()
	c.execute("select * from comment where post == ?",(topic,))
	comm = c.fetchall()
	conn.close()
	
	
	return jinja2_template('''
	<!DOCTYPE html>
				<html>
				<head>
				
				<style>
				.overlay-content {
				position: relative;
				top: 15%;
				width: 100%;
				text-align: center;
				margin-top: 30px;
				}
				
				ul { list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #fff; top: 0;font-size:9px}
				li { float: left; }
				li a { display: block; color: block; text-align: center; padding: 7px 8px; text-decoration: none; }
				li a:hover:not(.active) { background-color: turquoise; }
				.active { background-color: steelblue; } 
				</style>
				
				<meta name="viewport" content="width=device-width; initial-scale= 1.0;">
				
				<title>{{topic}}</title>
				</head>
				
				<body>

<div style="text-align:center;background-color:#000;">

{%if conv%}
<div>
<ul style="background-color:black;">
<li class="active"><a href="/">Home</a></li>

<li><a href="upload">Upload</a></li>
<li><a href="/login">Logout</a></li>
</ul>
</div>
{%endif%}

<h1 style="color:purple;">Anchor Blog</h1>

<div>
<ul style="list-style-type: none; margin: 0; padding: 0; overflow: hidden; top: 0; width: 100%; font-size:8px;text-align:center;">

<li><a href="/">Home</a></li>
<li><a href="/tag/entertainment">Entertainment</a></li>
<li><a href="/tag/technology">Technology</a></li>
<li><a href="/tag/sports">Sports</a></li>
<li><a href="/tag/finance">Finance</a></li>
<li><a href="/tag/foreign">Foreign</a></li>
</ul>
</div>

<form action="/search" method="post">
<div class="overlay-content">
		<input type="text" style="width:70%;padding:6px 0px;margin:4px 0;border:2px solid orange;box-styling:border-box;border-radius:20px;font-size:0.5em;" name="search"/>
		
		<input type="submit" style="height:auto;width:30%;background-color:purple;border-radius:1em;padding:6px 10px;font-size:10px;" value="search">
</div>
</form>
</div>

<hr color='red'>
</div>

{%for y in post%}
<h4>{{y[0]}}</h4>
<hr color='black'>

<p style="font-size:13px;">{{y[1]}}</p>
{%endfor%}

<h5>Comment</h5>
<hr>

{%for c in comm%}
<p>{{c[2]}}</p>
<h6>By {{c[1]}}</h6>
<hr>
{%endfor%}

<form action="/c-ment" method="post">
<h5>Leave a reply</h5>
<div class = 'container' style="border-left:20px solid white;height:auto;">

<input type="text" value={{topic}} name="pst" style='color:white;border:1px solid white;height:0.1px;width:0.1px;'>

Name: <input type="text" name="name" style='border:1px solid grey;height:auto;width:40%;'>
<br><br>
Comment: <textarea name="comment" style='border:1px solid grey;height:70px;width:75%;'>
</textarea>

		<input type="submit" style="height:auto;width:30%;background-color:#4CAF50;border-radius:1em;padding:6px 10px;font-size:10px;" value="comment">
</div>
</form>


<footer style="text-align:center;background-color:#141414;color:#f1f1f1;font-size:10px;">
	<div id="wrapper">
	<nav class="navigation">
	<p style="color:grey;">All Rights Reserved</p>
	<p>2018.</p>
	</nav>
	</footer>
</body>
</html>
	''',topic=topic,post=post,comm=comm,conv=conv)


@route("/tag/<tag>")
@route("/tag/<tag>/<page:int>")
def tag(tag,page=0):
	conv = request.get_cookie("account",secret="zyber")
	
	conn = sqlite3.connect("shoplog")
	c = conn.cursor()
	
	ACTIVITY_TOTAL, = c.execute('SELECT COUNT(*) FROM post where category == ?',(tag,)).fetchone()
	
	per = PER_PAGE
	start = ACTIVITY_TOTAL - (page*per)
	end = ACTIVITY_TOTAL - (page+1)*per
	
	c.execute("select * from post where category == ? and rowid <= ? and rowid >= ? ORDER BY rowid DESC",(tag,start,end))
	all = c.fetchall()
	
	parameters = {
		'tag' : tag,
		'r' : ACTIVITY_TOTAL,
		'conv':conv,
		'page' : page,
		'all' : all,
		'has_next' : end > 0,
		'query_string' : '?'+request.query_string,
		}

	return jinja2_template('''
	<!DOCTYPE html>
				<html>
				<head>
				
				<style>
				.overlay-content {
				position: relative;
				top: 15%;
				width: 100%;
				text-align: center;
				margin-top: 30px;
				}
				
				ul { list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #fff; top: 0;font-size:9px}
				li { float: left; }
				li a { display: block; color: block; text-align: center; padding: 7px 8px; text-decoration: none; }
				li a:hover:not(.active) { background-color: turquoise; }
				.active { background-color: steelblue; } 
				</style>
				
				<meta name="viewport" content="width=device-width; initial-scale= 1.0;">
				
				<title>{{tag}}</title>
				</head>
				
				<body>

<div style="text-align:center;background-color:#000;">

{%if conv%}
<div>
<ul style="background-color:black;">
<li class="active"><a href="/">Home</a></li>
<li><a href="upload">Upload</a></li>
<li><a href="/login">Logout</a></li>
</ul>
</div>
{%endif%}

<h1 style="color:purple;">Anchor Blog</h1>

<div>
<ul style="list-style-type: none; margin: 0; padding: 0; overflow: hidden; top: 0; width: 100%; font-size:8px;text-align:center;">

<li><a href="/">Home</a></li>
<li><a href="/tag/entertainment">Entertainment</a></li>
<li><a href="/tag/technology">Technology</a></li>
<li><a href="/tag/sports">Sports</a></li>
<li><a href="/tag/finance">Finance</a></li>
<li><a href="/tag/foreign">Foreign</a></li>
</ul>
</div>

<form action="/search" method="get">
<div class="overlay-content">
		<input type="text" style="width:70%;padding:6px 0px;margin:4px 0;border:2px solid orange;box-styling:border-box;border-radius:20px;font-size:0.5em;" name="search"/>
		
		<input type="submit" style="height:auto;width:30%;background-color:purple;border-radius:1em;padding:6px 10px;font-size:10px;" value="search">
</div>
</form>
</div>

<hr color='red'>
</div>

{%for y in all%}
<h5 style="text-align:center;"><a style="text-decoration:none;color:#000;" href="/{{y[0]}}">{{y[0]}}</a></h5><hr color="black">
{%endfor%}

<nav>
	{% if page > 0%}
	{% if page == 1 %}
	<form action= "/tag/{{tag}}" />
	<input value="Next" type="submit" style="height:auto;width:30%;padding:5px 9px;background-color:#4CAF50;font-size:0.5em;float:left;">
	</form>
	{% else %}
	<form action= "/tag/{{tag}}/{{ page-1 }}{{ query_string }}" >
	<input value="Next" type="submit" style="height:auto;width:30%;padding:5px 9px;background-color:#4CAF50;font-size:0.5em;float:left;">
	</form>
	{% endif %}
	{% endif %}
	{% if has_next %}
	<form action ="/tag/{{tag}}/{{ page+1 }}{{ query_string }}" >
	<input value="Prev" type="submit" style="height:auto;width:30%;padding:5px 9px;background-color:#4CAF50;font-size:0.5em;float:right;">
	</form>
	{% endif %}
	</nav>
	<br>
	
	<footer style="text-align:center;background-color:#141414;color:#f1f1f1;font-size:10px;">
	<div style="height:auto;">
	<nav class="navigation">
	<p style="color:grey;">All Rights Reserved</p>
	<p>2018.</p>
	</nav>
	</div>
	</footer>
</body>
</html>
	''',**parameters)



@route("/c-ment",method="post")
def c_ment():
	pst = request.forms.get("pst")
	name = request.forms.get("name")
	comment = request.forms.get("comment")
	conn = sqlite3.connect("shoplog")
	c = conn.cursor()
	c.execute("INSERT INTO comment VALUES (?,?,?)",(pst,name,comment))
	conn.commit()
	conn.close()
	
	redirect(pst)


@route("/search")
@route("/search/<page:int>")
def search(page=0):
	conv = request.get_cookie("account",secret="zyber")
	
	search = request.forms.get("search")
	conn = sqlite3.connect("shoplog")
	c = conn.cursor()
	

	ACTIVITY_TOTAL,=c.execute('SELECT COUNT(*) FROM post where topic like ?',(search,)).fetchone()
	per = PER_PAGE
	start, end = ACTIVITY_TOTAL-(page *per), ACTIVITY_TOTAL-((page + 1)*per)
	
	c.execute("select * from post where topic like ? and rowid <= ? and rowid >= ? ORDER BY rowid DESC",(search,start,end))
	src = c.fetchall()
	
	parameters = {
		#'search':search,
		'page' : page,
		'src' : src,
		'has_next' : end < ACTIVITY_TOTAL,
		'query_string' : '?'+request.query_string,
		}

	c.close()
	
	conv=request.get_cookie("account",secret="zyber")
	return jinja2_template('''{{search}}{{conv}}
		<!DOCTYPE html>
				<html>
				<head>
				
				<style>
				.overlay-content {
				position: relative;
				top: 15%;
				width: 100%;
				text-align: center;
				margin-top: 30px;
				}
				
				ul { list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #fff; top: 0;font-size:9px}
				li { float: left; }
				li a { display: block; color: block; text-align: center; padding: 7px 8px; text-decoration: none; }
				li a:hover:not(.active) { background-color: turquoise; }
				.active { background-color: steelblue; } 
				</style>
				
				<meta name="viewport" content="width=device-width; initial-scale= 1.0;">
				
				<title>{{search}}</title>
				</head>
				
				<body>

<div style="text-align:center;background-color:#000;">

{%if conv%}
<div>
<ul style="background-color:black;">
<li class="active"><a href="/">Home</a></li>
<li><a href="upload">Upload</a></li>
<li><a href="/login">Logout</a></li>
</ul>
</div>
{%endif%}

<h1 style="color:purple;">Anchor Blog</h1>

<div>
<ul style="list-style-type: none; margin: 0; padding: 0; overflow: hidden; top: 0; width: 100%; font-size:8px;text-align:center;">

<li><a href="/">Home</a></li>
<li><a href="/tag/entertainment">Entertainment</a></li>
<li><a href="/tag/technology">Technology</a></li>
<li><a href="/tag/sports">Sports</a></li>
<li><a href="/tag/finance">Finance</a></li>
<li><a href="/tag/foreign">Foreign</a></li>
</ul>
</div>

<form action="/search" method="post">
<div class="overlay-content">
		<input type="text" style="width:70%;padding:6px 0px;margin:4px 0;border:2px solid orange;box-styling:border-box;border-radius:20px;font-size:0.5em;" name="search"/>
		
		<input type="submit" style="height:auto;width:30%;background-color:purple;border-radius:1em;padding:6px 10px;font-size:10px;" value="search">
</div>
</form>
</div>

<hr color='red'>
</div>


{%for y in src%}
<h5 style="text-align:center;"><a style="text-decoration:none;color:#000;" href="/{{y[0]}}">{{y[0]}}</a></h5><hr color="black">
{%endfor%}


<nav>
	{% if page > 0%}
	{% if page == 1 %}
	<form action= "/search" />
	<input value="Next" type="submit" style="height:auto;width:30%;padding:5px 9px;background-color:#4CAF50;float:left;">
	</form>
	{% else %}
	<form action= "/search/{{ page-1 }}{{ query_string }}" >
	<input value="Next" type="submit" style="height:auto;width:30%;padding:5px 9px;background-color:#4CAF50;font-size:0.5em;float:left;">
	</form>
	{% endif %}
	{% endif %}
	{% if has_next %}
	<form action ="/search/{{ page+1 }}{{ query_string }}" >
	<input value="Prev" type="submit" style="height:auto;width:30%;padding:5px 9px;background-color:#4CAF50;font-size:0.5em;float:right;">
	</form>
	{% endif %}
	</nav>
	<br>
	
	<footer style="text-align:center;background-color:#141414;color:#f1f1f1;font-size:10px;">
	<div style="height:auto;">
	<nav class="navigation">
	<p style="color:grey;">All Rights Reserved</p>
	<p>2018.</p>
	</nav>
	</div>
	</footer>

</body>
</html>
	''',conv=conv,search=search,**parameters)
	
@route('/images/<filepath:path>')
def images(filepath):
	return static_file(filepath,root='./images')

run(debug=True,reloader=True)