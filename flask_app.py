try:
	from flask import Flask,render_template,request,redirect,make_response
	import os
	import sqlite3
	import requests
	from datetime import datetime
except Exception as error:
	print(error)

path = "/home/gimage/mysite/static/image/"
app = Flask(__name__)
auth = "werrweirjwewe842349394e3"
try:
	# login
	@app.route("/login",methods=["POST","GET"])
	def login():
		if(request.method=="POST"):
			conn = sqlite3.connect("data.db")
			con = conn.cursor()
			username = request.form['username']
			password= request.form['password']
			res = con.execute(f"SELECT * FROM user_data  where email='{username}' and password='{password}' ")
			if(res.fetchall()):
				con.close()
				res= make_response(redirect("/"))
				res.set_cookie(auth,f"{username}_{password}")
				return res
			else:
				con.close()
				return render_template("login.html",response='show',error="Invalid email or password.")
		else:
			if(request.cookies.get(auth)):
				return redirect("/")
			else:
				return render_template("login.html")
	# join
	@app.route("/join",methods=["GET","POST"])
	def join():
		if(request.method=="POST"):
			conn = sqlite3.connect("data.db")
			con = conn.cursor()
# 			try:
			fname = request.form["fname"]
			lname = request.form["lname"]
			email = request.form["email"]
			username = request.form["username"]
			password = request.form["password"]
			con.execute("CREATE TABLE if not exists user_data (sno INTEGER NOT NULL UNIQUE,fname TEXT NOT NULL ,lname TEXT NOT NULL,email TEXT NOT NULL UNIQUE,username TEXT NOT NULL UNIQUE,password TEXT NOT NULL,PRIMARY KEY(sno AUTOINCREMENT)) ")
			res = con.execute(f"SELECT * FROM user_data where email='{email}' or username='{username}'")
			if(res.fetchall()):
				con.close()
				return render_template("join.html",error = "email or  username already exists ?",response="show")
			else:
				con.execute(f"INSERT INTO user_data(fname,lname,email,username,password) VALUES('{fname}','{lname}','{email}','{username}','{password}' ) ")
				conn.commit()
				con.close()
				os.mkdir(f"/home/gimage/mysite/static/{email}_{password}")
				resP = make_response(redirect("/"))
				resP.set_cookie(auth,f"{email}_{password}")
				return resP
# 			except:
				con.close()
				return redirect("/join")

		else:
			if(request.cookies.get(auth)):
				return redirect("/")
			else:
				return render_template("join.html")

	# default web page
	@app.route("/")
	def home():
		if(request.cookies.get(auth)):
			images_list = os.listdir(path)
			return render_template('index.html',image = images_list,auth= auth )
		else:
			images_list = os.listdir(path)
			return render_template("index.html",image=images_list)

	# upload image
	@app.route("/upload",methods=['GET',"POST"])
	def upload():
		if(request.method=='POST'):
			try:
				if(request.files['file']):
					file = request.files['file']
					default = request.form["default"]
					file_name = file.filename
					if(default == "Public"):
						if(file_name.endswith("jpg") or file_name.endswith("jpeg") or file_name.endswith('png') or file_name.endswith("gif")):
							file.save(f"{path}{file.filename}")
							return redirect("/upload")
						else:
							return redirect("/upload")

					else:
						if(file_name.endswith("jpg") or file_name.endswith("jpeg") or file_name.endswith('png') or file_name.endswith("gif")):
							store_image = "static/"
							dir_path = request.cookies.get(auth)
							if(os.path.exists(f"/home/gimage/mysite/static/{dir_path}")):
								file.save(f"/home/gimage/mysite/static/{dir_path}/{file.filename}")
								return redirect("/upload")
							else:
								os.mkdir(f"{store_image}{dir_path}")
								file.save(f"{store_image}{dir_path}/{file.filename}")
								return redirect("/upload")
						else:
							return redirect("/upload")
				elif(request.form['url']):
					url = request.form['url']
					name_img = url
					if(name_img.endswith("jpg") or name_img.endswith("0") or name_img.endswith("00") or name_img.endswith("jpeg") or name_img.endswith('png') or name_img.endswith("gif")):
					    default = request.form["default"]
					    res = requests.get(url).content
					    now = datetime.now()
					    if(default=="Public"):
					        now = datetime.now()
					        with open(f"/home/gimage/mysite/static/image/{now}-{str(url[-8:-5:])}.jpg",'wb') as image:
					            image.write(res)
					            image.close()
					            return redirect("/upload")
					    else:
					        dir_path = request.cookies.get(auth)
					        with open(f"/home/gimage/mysite/static/{dir_path}/{str(now)}.jpg",'wb') as image:
					            image.write(res)
					            image.close()
					            return redirect("/upload")
				else:
					return redirect('/')
			except:
				redirect("/")
		else:
			if(request.cookies.get(auth)):
				dir_path = request.cookies.get(auth)
				images_list = os.listdir(f"/home/gimage/mysite/static/{dir_path}")
				return render_template("upload.html",auth=auth,image = images_list)
			else:
				return redirect("/")

	# signout
	@app.route("/signout")
	def signout():
		if(request.cookies.get(auth)):
			resP = make_response(redirect("/"))
			resP.delete_cookie(auth)
			return resP
		else:
			return redirect("/")


	# delete
	@app.route("/delete/<img>")
	def delete(img):
		if(request.cookies.get(auth)):
			dir_path = request.cookies.get(auth)
			os.remove(f"/home/gimage/mysite/static/{dir_path}/{img}")
			return redirect("/upload")
		else:
			return redirect("/")
except:
	@app.route("/")
	def abort():
		return "NOT SITE "
if(__name__=="__main__"):
	app.run(debug=True)