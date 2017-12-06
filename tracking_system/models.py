from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

def validate_range(value):
    if value>100 or value < 1:
        raise ValidationError('%s should between 1 to 100' % value)

# Create your models here.
class List(models.Model):
    list_name = models.CharField(max_length=50, )
    desc = models.TextField(null=True)
    mark = models.IntegerField(validators=[validate_range])
    fall_due_date = models.DateField(null=True)
    winter_due_date = models.DateField(null=True)

class Student(User):
    GROUP_CHOICE = (
        ('FALL','Fall'),
        ('WINTER', 'Winter'),
    )
    group = models.CharField(max_length=20, choices=GROUP_CHOICE)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

class Process(models.Model):
    STATUS_CHOICE = (
        ('PEND','Pending'),
        ('DONE', 'Done'),
        ('OVER', 'Over Due'),
    )

    actual_mark = models.IntegerField(validators=[validate_range], null=True)
    student = models.ForeignKey(Student)
    list = models.ForeignKey(List)
    status = models.CharField(max_length=4, choices=STATUS_CHOICE, default='PEND')
    feedback = models.TextField(null=True)

# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)