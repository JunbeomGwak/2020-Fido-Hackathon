# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from useraccount.models import User
from django.contrib.auth.hashers import check_password
class UseraccountBackend(ModelBackend):
    def authenticate(self, request, password=None, **kwargs):
         username = kwargs['username']
         password = kwargs['companycode']

         try:
             useracc = User.objects.get(username=username)
             if check_password(password, useracc.password):
                 return useracc
                 
         except User.DoesNotExist:
             pass