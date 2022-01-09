from django import forms
from .models import UploadFileModel, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect # 리다이렉트 함수 import
from django.http import HttpResponse


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel
        fields = ('title', 'file')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False

class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'user_id', 'company', 'companycode']

class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={
            'required' : '아이디를 입력해주세요.' # 입력하지 않은 경우('required'키에 저장) 에러메시지 지정
        },
        max_length=100, label="사용자 이름")
    password = forms.CharField(
        error_messages={
            'required' : '비밀번호를 입력해주세요' # 입력하지 않은 경우('required'키에 저장) 에러메시지 지정
        },
        widget=forms.PasswordInput, label="비밀번호") # 비밀번호를 표시할 위젯을 지정

    def clean(self):
        cleaned_data = super().clean() # super을 통해 기존의 form안에 들어있는 clean함수를 호출 값이 들어있지 않다면 이부분에서 실패처리되어 나가짐
        username = cleaned_data.get('username') # 값이 존재한다면 값들을 가져옴
        password = cleaned_data.get('password')
        if not (username and password):
            self.add_error('password', '모든 값을 입력해야합니다.')  # 특정 필드에 에러를 넣는 함수
        else:
            user = User.objects.get(username=username)  # username필드의 값이 username인 사용자 정보를 가져옴
            if not check_password(password, user.password):  # 입력된 비밀번호와 데이터베이스에서 가져온 비밀번호 비교
                self.add_error('password', '비밀번호를 틀렸습니다.')  # 특정 필드에 에러를 넣는 함수
            else:  # 비밀번호가 일치하는 경우
                self.user_id = user.id  # self를 통해 클래스 변수 안에 저장되므로 밖에서 접근가능
