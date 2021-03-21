from django.db import models, transaction
from django.contrib.auth.base_user import BaseUserManager

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from Journal.models import *


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudentGroupModel, on_delete=models.CASCADE)

    def __str__(self):
        name = self.user.first_name
        surname = self.user.last_name
        grade = self.group.grade.name
        group = self.group.name
        fullinfo = name + ' ' + surname + ', ' + grade + ', ' + group
        return fullinfo