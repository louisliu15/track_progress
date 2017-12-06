from rest_framework import serializers
from .models import List, Process, Student
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'username', 'email', 'group')


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id', 'list_name', 'mark', 'desc', 'fall_due_date', 'winter_due_date')


class ProcessSerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = Process
        fields = ('id', 'actual_mark', 'status', 'student')


class ProcessSerializerForList(serializers.ModelSerializer):
    list = ListSerializer()

    class Meta:
        model = Process
        fields = ('id', 'actual_mark', 'status', 'feedback', 'list')
