#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/19 下午5:52
# @Author  : Aries
# @Site    : 
# @File    : views.py
# @Software: PyCharm Community Edition
from math import ceil
from . import www_site
from flask import jsonify, request, render_template, redirect, url_for
from app.models import Participator, Result, db, User
from app.interface.caculate import page_getter, recodes_getter, page_searcher, hash_md5, message_getter
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


@www_site.route('/register_in', methods=['POST'])
def register_in():
    if request.method == 'POST':
        counts = User.query.count()
        if counts > 2:
            return redirect(url_for('www_site.register'))
        dict_args = request.form.to_dict()
        user_name = dict_args['user_name']
        password = dict_args['password']
        email = dict_args['email']
        user = User.query.filter_by(user_name=user_name).first()
        if user:
            return redirect(url_for('www_site.register', message='用户已存在'))
        user = User(user_name=user_name,
                    email=email,
                    password_hash=generate_password_hash(password),
                    user_id=hash_md5(user_name))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('www_site.index'))
    return redirect(url_for('www_site.index'))


@www_site.route('/register')
def register():
    return render_template('register.html')


@www_site.route('/')
@www_site.route('/index')
def index():
    return render_template('login.html')


@www_site.route('/user_login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        dict_args = request.form.to_dict()
        user_name = str(dict_args['user_name'])
        password = dict_args['password']
        user = User.query.filter_by(user_name=user_name).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            return redirect(url_for('www_site.users'))
    return redirect(url_for('www_site.index'))


@www_site.route('/login_out', methods=['GET'])
def login_out():
    logout_user()
    return redirect(url_for('www_site.index'))


@www_site.route('/user', methods=['GET'])
@www_site.route('/user/<int:page>', methods=['GET'])
@www_site.route('/user/<int:page>/<int:page_content_number>')
@login_required
def users(page=1, page_content_number=10):
    content = page_getter(page, page_content_number, result_query=False)
    # caculate user records...
    user_records = recodes_getter(result_query=False)
    # caculate pages
    all_page_num = int(ceil(user_records / page_content_number))

    page_li = []

    for i in range(1, 3):
        if page - i > 0:
            page_li.append(page - i)

        if (page + i) < all_page_num + 1:
            page_li.append(page + i)

    page_li.append(page)
    page_li.sort()

    return render_template('user.html',
                           user_contents=content,
                           current_page_number=page,
                           user_records=user_records,
                           end_page=all_page_num,
                           page_li=page_li,
                           flag=1)


@www_site.route('/data', methods=['GET'])
@www_site.route('/data/<int:page>', methods=['GET'])
@www_site.route('/data/<int:page>/<int:page_content_number>')
@login_required
def data(page=1, page_content_number=10):

    # caculate user records...
    user_records = recodes_getter()
    # caculate pages
    all_page_num = int(ceil(user_records / page_content_number))

    page_li = []

    for i in range(1, 3):
        if page - i > 0:
            page_li.append(page - i)

        if (page + i) < all_page_num + 1:
            page_li.append(page + i)

    page_li.append(page)
    page_li.sort()
    ret = db.session.query(Result.Height, Result.Weight, Result.saPASI1, Result.saPASI2, Result.saPASI3, Result.saPASI4, Result.saPASI5,
                           Result.QualityOfLife, Result.Arthritis1, Result.Arthritis2, Result.Arthritis3,
                           Result.Arthritis4, Result.Arthritis5, Result.Arthritis6, Result.PR1, Result.PR2,
                           Result.PR3, Result.PR4, Result.PR5, Result.PR6, Result.PR7, Result.CreateTime,
                           Participator.Name, Participator.IDNum, Participator.IncidenceTime).join(Participator, Participator.HashInput == Result.HashInput)
    value = ret.order_by(Result.CreateTime.desc()).paginate(page, page_content_number, error_out=False)
    return render_template('data.html',
                           user_contents=value,
                           current_page_number=page,
                           user_records=user_records,
                           end_page=all_page_num,
                           page_li=page_li)


@www_site.route('/search/user', methods=['POST'])
@www_site.route('/search/user/<int:page>/<keywords>')
@login_required
def search(page=1, page_content_number=10, keywords=None):
    if request.method == 'POST':
        dict_args = request.form.to_dict()
        search_key_words = str(dict_args['keywords'])
    else:
        search_key_words = keywords

    is_IDNum = True

    for single_word in search_key_words[:12]:
        if 58 > ord(single_word) > 47:
            pass
        else:
            is_IDNum = False
            break
    search_key_words = '%{0}%'.format(search_key_words)
    if is_IDNum:
        ret = db.session.query(Participator).filter(Participator.IDNum.ilike(search_key_words))
        user_records = db.session.query(Participator).filter(Participator.IDNum.ilike(search_key_words)).count()
    else:
        ret = db.session.query(Participator).filter(Participator.Name.ilike(search_key_words))
        user_records = db.session.query(Participator).filter(Participator.Name.ilike(search_key_words)).count()

    value = ret.paginate(page, page_content_number, error_out=False)
    all_page_num = int(ceil(user_records / page_content_number))
    page_li = []

    for i in range(1, 3):
        if page - i > 0:
            page_li.append(page - i)

        if (page + i) < all_page_num + 1:
            page_li.append(page + i)

    page_li.append(page)
    page_li.sort()

    return render_template('search.html',
                           user_contents=value,
                           current_page_number=page,
                           user_records=user_records,
                           end_page=all_page_num,
                           page_li=page_li,
                           keywords=search_key_words)


@www_site.route('/result/<username>/<IDNum>', methods=['GET'])
@www_site.route('/result/<username>/<IDNum>/<int:page>', methods=['GET'])
@login_required
def search_by_hash_input(username, IDNum, page=1, page_content_number=10):
    input_hash = hash_md5(username+IDNum)
    ret = db.session.query(Result.Height, Result.Weight, Result.saPASI1, Result.saPASI2, Result.saPASI3, Result.saPASI4, Result.saPASI5,
                           Result.QualityOfLife, Result.Arthritis1, Result.Arthritis2, Result.Arthritis3,
                           Result.Arthritis4, Result.Arthritis5, Result.Arthritis6, Result.PR1, Result.PR2,
                           Result.PR3, Result.PR4, Result.PR5, Result.PR6, Result.PR7, Result.CreateTime,
                           Participator.Name, Participator.IDNum, Participator.IncidenceTime).join(Participator, Participator.HashInput == Result.HashInput, isouter=True)
    value = ret.order_by(Result.CreateTime.desc()).filter_by(HashInput=input_hash).paginate(page, page_content_number, error_out=False)

    user_records = Result.query.filter_by(HashInput=input_hash).count()
    all_page_num = int(ceil(user_records / page_content_number))
    page_li = []

    for i in range(1, 3):
        if page - i > 0:
            page_li.append(page - i)

        if (page + i) < all_page_num + 1:
            page_li.append(page + i)

    page_li.append(page)
    page_li.sort()
    return render_template('data.html',
                           user_contents=value,
                           current_page_number=page,
                           user_records=user_records,
                           end_page=all_page_num,
                           page_li=page_li)


@www_site.route('/result/message', methods=['GET'])
@www_site.route('/result/message/<int:page>', methods=['GET'])
@login_required
def messages(page=1, page_content_number=5):
    ret = db.session.query(Result.message, Participator.Name, Participator.PhoneNum).join(Participator, Participator.HashInput==Result.HashInput, isouter=True)
    value = ret.order_by(Result.CreateTime.desc()).filter(Result.message != '').paginate(page, page_content_number, error_out=False)
    num = message_getter()
    all_page_num = int(ceil(num / page_content_number))
    page_li = []

    for i in range(1, 3):
        if page - i > 0:
            page_li.append(page - i)

        if (page + i) < all_page_num + 1:
            page_li.append(page + i)

    page_li.append(page)
    page_li.sort()

    return render_template('messages.html',
                           flag=2,
                           message_contents=value,
                           current_page_number=page,
                           message_records=num,
                           end_page=all_page_num,
                           page_li=page_li)
