# -*- coding: utf-8 -*-
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #웹
    path('signup/', views.signup, name='웹회원가입'),
    path('login/', views.login, name='웹로그인'),
    #프로그램
    path('program_login/', views.program_login, name='프로그램로그인'),
    path('program_signup/', views.program_signup, name='프로그램회원가입'),
    #Key
    path('keystore/', views.keystore, name='공개키저장'),
    path('recvfilekey/', views.receivefilekey, name="복호화파일이름리턴"),
    path('receivesignal/', views.receivesignal, name="복호화키리턴"),

    #app
    path('app_login/<str:id>', views.app_login),
    path('receivesynkey/', views.receivesynkey, name='app_signup'),
    path('synnkey/', views.encryptsynnkey),
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('list/', views.file_list, name='file_list'),
    path('testupload/', views.test_upload),
    path('returnlist/<str:name>', views.return_list, name='return_list'),


    #web
    path('summernote/', include('django_summernote.urls')),
    #jwt
    path('verify/', views.verity)
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
