# -*- coding: utf-8 -*-
from django.contrib.auth.models import(BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import ImageField
from django.utils.translation import ugettext_lazy as _
from urllib.parse import urlparse
from django.core.files import File
from .common import file_upload_path


class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username, user_id, company, companycode, password=None):

        if not username:
            raise ValueError(_('Users must have an name!'))

        user = self.model(
            username=username,
            user_id = user_id,
            company= company,
            companycode = companycode,
        )
        user.set_password(companycode)
        user.save()
        return user

    def create_superuser(self, username, user_id, company, companycode, password):
        user = self.create_user(
            username=username,
            user_id = user_id,
            company = company,
            companycode = companycode,
            password=password,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, verbose_name="이름")
    user_id = models.CharField(max_length=40, unique=True, verbose_name="아이디")
    company = models.CharField(max_length=100, verbose_name="회사")
    companycode = models.CharField(max_length=100, verbose_name="회사코드")
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'django_user'

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_id', 'company', 'companycode']
    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    get_full_name.short_description = _('Full name')

class UploadFileModel(models.Model):
    title = models.TextField(default='')
    file = models.FileField(null=True)

