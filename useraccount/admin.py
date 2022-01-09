from django.contrib import admin
from .models import User
from django_summernote.admin import SummernoteModelAdmin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id', 'company', 'companycode')


class UserAdmin(SummernoteModelAdmin):
    list_display = ('username', 'password') # user list 사용자명과 비밀번호를 확인할 수 있도록 구성
    summernote_fields = ('content',)

admin.site.register(User, UserAdmin)