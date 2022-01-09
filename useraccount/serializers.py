# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import User
class FidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'user_id', 'company', 'companycode']

class JsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'companycode']

class UserRegisterationSerializer(serializers.ModelSerializer):
    profile = FidoSerializer(required=False)

    class Meta:
        model = User

