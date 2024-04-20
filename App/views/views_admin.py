from flask import Blueprint, render_template, request, redirect, jsonify
from ..models.models_admin import *
from ..models.models import *

admin = Blueprint('admin', __name__)


# Backstage Management--Home
@admin.route('/admin')
@admin.route('/admin/index')
def index():
    # get cookie
    user_id = request.cookies.get('user_id')
    if user_id:
        user = AdminUserModel.query.get(user_id)
        categorys = CategoryModel.query.filter()
        return render_template('admin/index.html', username=user.name, categorys=categorys)
    else:
        # redirect to login page
        return redirect('/admin/login')


# Backstage Management--Login
@admin.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        userpwd = request.form.get('userpwd')
        # if username and userpwd are correct
        user = AdminUserModel.query.filter_by(name=username, passwd=userpwd).first()
        if user:
            # login successfully
            pass
            response = redirect('/admin/index')
            response.set_cookie('user_id', str(user.id), max_age=7 * 24 * 3600)
            return response
        else:
            return redirect('/admin/login')


# Backstage Management--Logout
@admin.route('/admin/logout')
def admin_logout():
    response = redirect('/admin/login')
    response.delete_cookie('user_id')
    # delete cookie
    return response

# Backstage Management--register
@admin.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'GET':
        return render_template('/admin/register.html')
    elif request.method == 'POST':
        username = request.form.get('username1')
        userpwd = request.form.get('userpwd1')
        # add new user
        user = AdminUserModel()
        user.name = username
        user.passwd = userpwd
        response = redirect('/admin/register')
        response.set_cookie('user_id', str(user.id), max_age=7 * 24 * 3600)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        return redirect('/admin/login')


# -------------------Backstage Category Management-------------------#
# Backstage Management--Category Management panel
@admin.route('/admin/category')
def admin_category():
    # get cookie
    user_id = request.cookies.get('user_id')
    if user_id:
        user = AdminUserModel.query.get(user_id)
        categorys = CategoryModel.query.all()
        return render_template('admin/category.html', username=user.name, categorys=categorys)
    else:
        # redirect to login page
        return redirect('/admin/login')


# Backstage Management--Add
@admin.route('/admin/addcategory', methods=['GET', 'POST'])
def admin_addcategory():
    user_id = request.cookies.get('user_id')
    if user_id:
        user = AdminUserModel.query.get(user_id)
        if request.method == 'POST':
            name = request.form.get('name')
            describe = request.form.get('describe')
            # add
            category = CategoryModel()
            category.name = name
            category.describe = describe
            try:
                db.session.add(category)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
            return redirect('/admin/category')
        return 'false'
    else:
        return redirect('/admin/login')


# Backstage Management--Delete
@admin.route('/admin/delcategory', methods=['GET', 'POST'])
def admin_delcategory():
    user_id = request.cookies.get('user_id')
    if user_id:
        user = AdminUserModel.query.get(user_id)
        if request.method == 'POST':
            id = request.form.get('id')
            category = CategoryModel.query.get(id)
            # delete
            try:
                db.session.delete(category)
                db.session.commit()
            except Exception as e:
                print('e:', e)
                db.session.rollback()
            return 'ok'
    else:
        return redirect('/admin/login')


# Backstage Management--Update
@admin.route('/admin/updatecategory/<id>', methods=['GET', 'POST'])
def admin_update_category(id):
    user_id = request.cookies.get('user_id')
    if user_id:
        user = AdminUserModel.query.get(user_id)
        if request.method == 'GET':
            category = CategoryModel.query.get(id)
            return render_template('admin/updatecategory.html', id=id, username=user.name, category=category)
        elif request.method == 'POST':
            name = request.form.get('name')
            describe = request.form.get('describe')
            # update
            category = CategoryModel.query.get(id)
            category.name = name
            category.describe = describe
            try:
                db.session.commit()
                return jsonify({'id': id, 'name': name, 'describe': describe})  # return json data
            except Exception as e:
                print('e:', e)
                db.session.rollback()
                return jsonify({'error': 'Database error'}), 500  # return error message
    else:
        return redirect('/admin/login')
