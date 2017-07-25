# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from models import UserModel, SessionToken
from demoapp.forms import SignUpForm, LoginForm, PostForm
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from instagram.settings import BASE_DIR


# Create your views here.
def signup_view(request):
    if request.method=='GET':
      #display signup form
     #today= datetime.now
      form =  SignUpForm()
      template_name='signup.html'
      return render(request, template_name, {'form': form})
    elif request.method == 'POST':
         form = SignUpForm(request.POST)
         if form.is_valid():
             print "I am at line 22"
             username = form.cleaned_data['username']
             name = form.cleaned_data['name']
             email = form.cleaned_data['email']
             password = form.cleaned_data['password']
             new_user= UserModel(name=name,password=make_password(password),username=username,email=email)
             new_user.save()
             template_name='success.html'
             return render(request,template_name,{'form': form })
         else:
             print "I am at line 31"
             form = SignUpForm()
             template_name = 'signup.html'
             return render(request, template_name, {'form': form})
    else:
        return render(request, 'error.html',{'error':'error'})

def login_view(request):
        response_data = {}
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = UserModel.objects.filter(username=username).first()

                if user:
                    if check_password(password, user.password):
                        token = SessionToken(user=user)
                        token.create_token()
                        token.save()
                        response = redirect('feed/')
                        response.set_cookie(key='session_token', value=token.session_token)
                        return response
                    else:

                     response_data['message'] = 'Incorrect Password! Please try again!'


