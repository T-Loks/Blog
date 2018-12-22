from bottle import run,route,jinja2_template

@route('/')
def home():
	ls={'PDP primaries Governor Ayade receives Saraki,decries influx of Cameroonians':'In a development that followed as anoffshoot of struggle for the AmbazoniaRepublic in Cameroon, Cross Rivergovernor, Ayade has raised concern overthe increasing numbers of Camerooniansin the state.'}
	return jinja2_template('''
     <!DOCTYPE html>
     <html>
	<head>
	<style>
    h1{
     text-align:center;
     }
    h1{
     font-family:'Pacifico';
     }
     #wrapper{
 width:1024px;
 margin:0px auto;
 border:3px solid #000;
 padding:1px 0px;
}
</style>

<meta name="viewport" content="width=device-width,initial-scale=1.0;">
</head>

<body>
<center>
<p style="background-color:green;">Online shop</p>
</center>
<br />

{%for i in ls%}
<p>{{i}}</p>
<p>{{ls[i]}}</p>
{%endfor%}
</body>
</html>
    ''',x=80,ls=ls,xnx='Tega')

run(host="localhost",port=8080,debug=True,reloader=True)