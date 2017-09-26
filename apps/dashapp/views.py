# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
import bcrypt
# Create your views here.

def index(request):
    if 'id' in request.session:
        return render(request,'dashapp/index.html')
    else:
        request.session['id'] = ''
        return render(request,'dashapp/index.html')

def signin(request):
    if request.method == 'GET':
        return render(request,'dashapp/signin.html')
    elif request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request,error, extra_tags=tag )
            return redirect('/signin')
        else:
            print request.POST['login_email']
            login_user = User.objects.filter(email = request.POST['login_email'])
            request.session['id'] = login_user[0].id
            if login_user[0].user_level == 9:
                return redirect('/dashboard/admin')
            else:
                return redirect('/dashboard')

def register(request):
    if request.method == 'GET':
        return render(request,'dashapp/register.html')
    elif request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request,error, extra_tags=tag )
            return redirect('/register')
        else:
            hash_pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
            if User.objects.all():
                new_user = User.objects.create(first_name = request.POST['first_name'],last_name = \
                request.POST['last_name'], email = request.POST['email'], password = hash_pw)
                request.session['id'] = new_user.id
                return redirect('/dashboard')
            else:
                new_user = User.objects.create(first_name = request.POST['first_name'],last_name = \
                request.POST['last_name'], email = request.POST['email'], password = hash_pw, \
                user_level = 9)
                request.session['id'] = new_user.id
                return redirect('/dashboard/admin')

def admin(request):
    all_users = User.objects.all()
    return render(request,'dashapp/admin.html',{'all_users':all_users})

def dashboard(request):
    all_users = User.objects.all()
    return render(request,'dashapp/dashboard.html',{'all_users':all_users})

def add_new(request):
    if request.method == 'GET':
        return render(request,'dashapp/new.html')
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request,error, extra_tags=tag )
            return redirect('/users/new')
        else:
            hash_pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
            new_user = User.objects.create(first_name = request.POST['first_name'],last_name = \
            request.POST['last_name'], email = request.POST['email'], password = hash_pw)
            return redirect('/dashboard/admin')

def user_edit(request, user_id):
    if request.method == 'GET':
        edit_user = User.objects.get(id = user_id)
        return render(request,'dashapp/edit_user.html',{'edit_user': edit_user})
    if request.method == 'POST':
        edit_user = User.objects.get(id = user_id)
        if request.POST['info'] == 'user':
            errors = User.objects.update_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request,error, extra_tags=tag )
                return redirect('/users/edit/{}'.format(user_id))
            else:
                edit_user = User.objects.get(id = user_id)
                edit_user.first_name = request.POST['first_name']
                edit_user.last_name = request.POST['last_name']
                edit_user.email = request.POST['email']
                edit_user.user_level = request.POST['user_level']
                edit_user.save()
                return redirect('/dashboard/admin')
        elif request.POST['info'] == 'pass':
            errors = User.objects.password_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request,error, extra_tags=tag )
                return redirect('/users/edit/{}'.format(user_id))
            else:
                edit_user = User.objects.get(id = user_id)
                hash_pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
                edit_user.password = hash_pw
                edit_user.save()
                return redirect('/dashboard/admin')

def edit(request):
    if request.method == 'GET':
        profile_user = User.objects.get(id = request.session['id'])
        return render(request,'dashapp/profile_user.html',{'edit_user': profile_user})
    if request.method == 'POST':
        profile_user = User.objects.get(id = request.session['id'])
        if request.POST['info'] == 'user':
            errors = User.objects.update_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request,error, extra_tags=tag )
                return redirect('/users/edit')
            else:
                profile_user.first_name = request.POST['first_name']
                profile_user.last_name = request.POST['last_name']
                profile_user.email = request.POST['email']
                profile_user.save()
                return redirect('/dashboard')
        elif request.POST['info'] == 'pass':
            errors = User.objects.password_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request,error, extra_tags=tag )
                return redirect('/users/edit')
            else:
                hash_pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
                profile_user.password = hash_pw
                profile_user.save()
                return redirect('/dashboard')
        elif request.POST['info'] == 'desc':
            if len(request.POST['desc']) < 10:
                messages.error(request,"Description should have at least 10 characters!!" )
                return redirect('/users/edit')
            else:                    
                profile_user.desc = request.POST['desc']
                profile_user.save()
                return redirect('/dashboard')

def show_user(request,user_id):
    if request.method == 'GET':
        the_user = User.objects.filter(id = user_id)
        the_user = the_user[0]
        all_messages = the_user.messages.all().order_by('-created_at')
        all_comments = Comment.objects.all().order_by('-created_at')
        print all_messages
        context ={
            'the_user': the_user,
            'all_messages':all_messages,
            'all_comments':all_comments,
        }
        return render(request,'dashapp/show.html',context)
    elif request.method == 'POST':
        the_user = User.objects.filter(id = user_id)
        the_user = the_user[0]
        if request.POST['input'] == 'message':
            new_message = Message.objects.create(content = request.POST['message'], poster = User.objects.filter(id = request.session['id'])[0], \
            receiver = the_user)
            the_user.messages.add(new_message)
            return redirect('/users/show/{}'.format(user_id))
        if request.POST['input'] == 'comment':
            the_message = Message.objects.filter(id =request.POST['id'] )[0]
            new_comment = Comment.objects.create(detail = request.POST['comment'], message = the_message, user = User.objects.filter(id = request.session['id'])[0])
            the_message.comments.add(new_comment)
            return redirect('/users/show/{}'.format(user_id))
def logoff(request):
    del request.session['id']
    return redirect('/')