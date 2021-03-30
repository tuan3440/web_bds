from flask import Flask, render_template, request, session
from pymongo import MongoClient
from flask_pymongo import PyMongo,DESCENDING,ASCENDING
from flask_paginate import Pagination, get_page_args
import numpy as np


app = Flask(__name__)
client = MongoClient('mongodb+srv://nambn007:nambn007@cluster0.oki5a.mongodb.net/BatDongSan?retryWrites=true&w=majority')
app.secret_key = 'super secret key'
db = client.BatDongSan
batdongsan = db.batdongsan


allBatDongSan = list(batdongsan.find())
total = len(allBatDongSan)
def get_bds(offset=0, per_page=10):
    return allBatDongSan[offset: offset + per_page]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/testData', methods = ['GET'])
def test():
    items = batdongsan.find({})
    return render_template('1.html', items = items)

@app.route('/dangki', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        session['usename'] = name
        email = request.form['email']
        password = request.form['password']
        return render_template('signin.html')
    else:
        return render_template('register.html')

@app.route('/dangnhap', methods = ['POST', 'GET'])
def signIn():
    if request.method == 'POST' :
        name = "tuandz"
        session['usename'] = name
        return render_template('home.html', username = session['usename'])
    else :
        return render_template('signin.html')

@app.route('/dangxuat', methods = ['GET'])
def logOut():
    session.pop('usename')
    return render_template('home.html')

@app.route('/xemTin', methods = ['GET', 'POST'])
def viewPost():
    if 'usename' in session:
            page, per_page, offset = get_page_args(page_parameter='page',
                                                   per_page_parameter='per_page')
            pagination_bds = get_bds(offset=offset, per_page=per_page)
            pagination = Pagination(page=page, per_page=per_page, total=total,
                                    css_framework='bootstrap4')
            return render_template('listHouse.html',
                                   items=pagination_bds,
                                   page=page,
                                   per_page=per_page,
                                   pagination=pagination,
                                   username=session['usename']
                                   )
    else :
        return render_template('signin.html')

# @app.route('/xemTin')
# def viewHouse():

@app.route('/danh-sach-yeu-thich')
def viewWishList():
    if 'usename' in session :
        return render_template('wishList.html',  username = session['usename'])
    else :
        return render_template('signin.html')

@app.route('/xem-chi-tiet')
def viewDetail():
    if 'usename' in session:
        return render_template('detail.html', username=session['usename'])
    else:
        return render_template('signin.html')

