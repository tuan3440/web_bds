from asn1crypto._ffi import null
from flask import Flask, render_template, request, session, redirect, url_for, flash
from pymongo import MongoClient
from flask_paginate import Pagination, get_page_args
from bson.objectid import ObjectId
from bson.json_util import dumps,loads

app = Flask(__name__)
client = MongoClient('mongodb+srv://nambn007:nambn007@cluster0.oki5a.mongodb.net/RealEstate?retryWrites=true&w=majority')
app.secret_key = 'super secret key'
db = client.RealEstate
batdongsan = db.RealEstateRaw
users = db.users
wishlist = db.wishlist

# def get_users(offset=0, per_page=10):
#     return users[offset: offset + per_page]

@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', user = loads(session['user']))
    else:
        return render_template('home.html')
@app.route('/testData', methods = ['GET'])
def test():
    items = batdongsan.find({})
    return render_template('1.html', items = items)

@app.route('/dangki', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = {
            "name" : name,
            "email" : email,
            "password" : password
        }
        users.insert_one(user)
        flash('Đăng kí thành công.Vui lòng đăng nhập')
        return redirect(url_for('signIn'))
    else:
        return render_template('register.html')

@app.route('/dangnhap', methods = ['POST', 'GET'])
def signIn():
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        allUsers = users.find()
        for user in allUsers:
            if (user['email'] == email and user['password'] == password):
                session['user'] = dumps(user)
                break
        if ('user' in session):
            return render_template('home.html', user = loads(session['user']))
        else :
            flash('Email hoặc password không chính xác')
            return render_template('signin.html')
    else :
        return render_template('signin.html')

@app.route('/dangxuat', methods = ['GET'])
def logOut():
    session.pop('user')
    return render_template('home.html')

# @app.route('/xemTin', methods = ['GET', 'POST'])
# def viewPost():
#     if 'user' in session:
#             sq_from = 0
#             sq_to = 10000
#             pr_from = 0
#             pr_to = 10000
#             if request.args.get('sq_from'):
#                sq_from = request.args.get('sq_from')
#             if request.args.get('sq_to'):
#                sq_to = request.args.get('sq_to')
#             if request.args.get('pr_from'):
#                pr_from = request.args.get('pr_from')
#             if request.args.get('pr_to'):
#                pr_to = request.args.get('pr_to')
#             print(sq_from)
#             print(sq_to)
#             print(pr_from)
#             print(pr_to)
#             bds = batdongsan.find({"$and" : [{"square" : {"$lt": float(sq_to)}}, {"square" : {"$gt": float(sq_from)}}, {"price" : {"$lt": float(pr_to)}}, {"price" : {"$gt": float(pr_from)}}]}).limit(20)
#             listPostWish = wishlist.find({"user_id": str(loads(session['user'])['_id'])})
#             idPostWish = []
#             for l in listPostWish:
#                 idPostWish.append(ObjectId(l['post_id']))
#             return render_template('listHouse.html', bds = bds,  user=loads(session['user']), idPostWish=idPostWish)
#     else :
#             return render_template('signin.html')

@app.route('/xemTin', methods = ['GET', 'POST'])
def viewPost():
    if 'user' in session:
            sq_from = 0
            sq_to = 10000
            pr_from = 0
            pr_to = 10000
            if request.args.get('sq_from'):
               sq_from = request.args.get('sq_from')
            if request.args.get('sq_to'):
               sq_to = request.args.get('sq_to')
            if request.args.get('pr_from'):
               pr_from = request.args.get('pr_from')
            if request.args.get('pr_to'):
               pr_to = request.args.get('pr_to')
            page, per_page, offset = get_page_args(page_parameter='page',
                                                   per_page_parameter='per_page')
            bds = batdongsan.find({"$and" : [{"square" : {"$lt": float(sq_to)}}, {"square" : {"$gt": float(sq_from)}}, {"price" : {"$lt": float(pr_to)}}, {"price" : {"$gt": float(pr_from)}}]})
            bds = list(bds)
            total = len(bds)
            bds = bds[offset : offset + per_page]
            pagination = Pagination(page=page, per_page=per_page, total=total,
                                    css_framework='bootstrap4')
            listPostWish = wishlist.find({"user_id": str(loads(session['user'])['_id'])})
            idPostWish = []
            for l in listPostWish:
                idPostWish.append(ObjectId(l['post_id']))
            return render_template('listHouse.html',user=loads(session['user']), idPostWish=idPostWish, bds=bds,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
    else :
            return render_template('signin.html')


@app.route('/add-wishlist/<post_id>', methods = ['POST', 'GET'])
def addWishList(post_id) :
    user_id = str(loads(session['user'])['_id'])
    item = {
        "post_id" : post_id,
        "user_id" : user_id
    }
    wishlist.insert_one(item)
    flash('Thêm thành công')
    return redirect(url_for('viewPost'))

@app.route('/delete-wishlist/<post_id>', methods = ['POST', 'GET'])
def deleteWishList(post_id) :
        x = wishlist.delete_one({"post_id": post_id} and {"user_id": str(loads(session['user'])['_id'])})
        flash('Xóa thành công')
        return redirect(url_for('viewWishList'))

@app.route('/danh-sach-yeu-thich')
def viewWishList():
    if 'user' in session :
        list = wishlist.find({ 'user_id': str(loads(session['user'])['_id'])})
        posts = []
        id = []
        for l in list:
            post = batdongsan.find_one({"_id" : ObjectId(l['post_id'])})
            posts.append(post)
            id.append(str(ObjectId(l['post_id'])))
        return render_template('wishList.html',  user=loads(session['user']), list = posts,ids = id, index=0 )
    else :
        return render_template('signin.html')

@app.route('/xem-chi-tiet/<id>')
def viewDetail(id):
    if 'user' in session:
        data = batdongsan.find_one( { '_id' : ObjectId(id)} )
        # api get tin lien quan
        return render_template('detail.html', user=loads(session['user']), data = data)
    else:
        return render_template('signin.html')

# search text
@app.route('/search', methods=['GET'])
def searchPost():
    if 'user' in session:
        keyword = ''
        if request.args.get('keyword'):
            keyword = request.args.get('keyword')
        bds = {}
        listPostWish = wishlist.find({"user_id": str(loads(session['user'])['_id'])})
        idPostWish = []
        for l in listPostWish:
            idPostWish.append(ObjectId(l['post_id']))
        return render_template('listHouse.html', bds=bds, user=loads(session['user']), idPostWish=idPostWish)
    else:
        return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)
