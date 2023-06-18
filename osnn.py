from flask import Flask, render_template, request, redirect, flash, get_flashed_messages
import random
from mod import *
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from werkzeug.utils import secure_filename
import uuid


import numpy as np
import base64

@newsite.route('/')
def index():
       if current_user.is_authenticated:
         return render_template("osn_auth.html")
       else:
         return render_template("osn.html")


@newsite.route('/reg', methods=['POST', 'GET'])
def registracia():
     if request.method == 'POST':
      login = request.form['login']
      password = request.form['password']
      hash = generate_password_hash(password)
      article = registr(username=login, password=hash)
      db.session.add(article)
      db.session.commit()
      if login and password:
       User = registr.query.filter_by(username=login).first()
       if check_password_hash(User.password, password):
        login_user(User)
        return redirect('/')
     return render_template("regg.html")


@newsite.route('/log', methods=['POST', 'GET'])
def avtorizacia():
    if request.method == 'POST':
     loginn = request.form['login']
     passwordd = request.form['password']


     if loginn and passwordd:
       User = registr.query.filter_by(username=loginn).first()

       if check_password_hash(User.password, passwordd):
        login_user(User)
        return redirect('/')
       
       else:
        flash('Неверный логин или пароль')
        get_flashed_messages()
       return render_template("logg.html")
      
     else:
       flash('заполните все поля')
       get_flashed_messages()


       return render_template("logg.html") 
     
    return render_template("logg.html")  


@newsite.route(f'/<id>', methods=['POST', 'GET'])
def home_page():  
   if current_user.is_authenticated:
    return render_template("home_page.html")
   
   else:
    return redirect('/') 
   

@newsite.route('/logout', methods=['POST', 'GET'])
def logout():
   if current_user.is_authenticated:
    logout_user()
    return redirect('/')
   
   else:
     return redirect('/')


@newsite.route('/catalog', methods=['POST', 'GET'])
def catalog():
     if request.method == 'POST':
      name = str(request.form['title'])
      price = str(request.form['price'])
      description = str(request.form['description'])
      photo = request.files['photo']
      photo = photo.read()
      article = UserModifications(usernick=str(current_user.get_id()), itemname=name, itemdescr=description, itemprice=price, itemphoto=photo)
      db.session.add(article)
      db.session.commit()
      flash('Товар добавлен!')
      get_flashed_messages()
     articles = UserModifications.query.all()
     return render_template("catalog.html", user_modifications=articles)

if __name__== '__main__':
    newsite.run() 