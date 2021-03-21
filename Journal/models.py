import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class GradeModel(models.Model):
    name = models.CharField(max_length=18)

    def __str__(self):
        return str(self.name)


class SubjectsModel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class StudentGroupModel(models.Model):
    name = models.CharField(max_length=20)
    grade = models.ForeignKey(GradeModel, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(SubjectsModel)

    def __str__(self):
        name = self.name
        grade = self.grade.name
        nameAndGrade = name + ', ' + grade
        return nameAndGrade


class JournalPageModel(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.ForeignKey(GradeModel, blank=True, on_delete=models.CASCADE)
    group = models.ForeignKey(StudentGroupModel, blank=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectsModel, blank=True, on_delete=models.CASCADE)
    marks = ArrayField(models.CharField(max_length=2, blank=True), blank=True)
    marksDate = ArrayField(models.CharField(max_length=20, blank=True), blank=True)

    def __str__(self):
        firstName = self.name.first_name
        lastName = self.name.last_name
        grade = self.grade.name
        group = self.group.name
        subject = self.subject.name
        return str(firstName + ' ' + lastName + ', ' + grade + ', ' + group + ', ' + subject)
        # return str(firstName + ' ' + lastName)