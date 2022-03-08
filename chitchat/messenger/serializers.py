from dataclasses import field
from rest_framework import serializers
from .models import Profile, Message, Image, Report
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message_contents', 'message_datetime', 'message_type', 'user_id')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('report_contents', 'report_datetime', 'report_update_datetime', 'user_id', 'message_id')


class ImageSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Image
        fields = ['image_path']