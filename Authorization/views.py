from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.db.models.functions import Concat
from django.db.models import Q, Value

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from Journal.models import *
from .forms import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Аккаунт зарегистрирован!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'Authorization/register.html', {'form': form, 'title': 'Регистрация'})


@login_required
def profile(request):
    profileTemplateName = 'Authorization/profile.html'
    currentUser = request.user.pk

    currentUserGroup = Student.objects.filter(user=currentUser).values('group')
    currentUserGroup = currentUserGroup[0]['group']

    currentUserGroupName = StudentGroupModel.objects.filter(pk=currentUserGroup).values('name')
    currentUserGroupName = currentUserGroupName[0]['name']

    currentUserGrade = StudentGroupModel.objects.filter(pk=currentUserGroup).values('grade')
    currentUserGrade = GradeModel.objects.filter(pk=currentUserGrade[0]['grade']).values('name')
    currentUserGrade = currentUserGrade[0]['name']

    currentUserSubjects = StudentGroupModel.objects.filter(pk=currentUserGroup).values('subjects')


    currentUserSubjectsList = [None] * len(currentUserSubjects)

    for _ in range(len(currentUserSubjects)):
        temp = SubjectsModel.objects.filter(pk=currentUserSubjects[_]['subjects']).values('name')
        temp = temp[0]['name']
        currentUserSubjectsList[_] = temp

    context = {
        'userGroup': currentUserGroupName,
        'userGrade': currentUserGrade,
        'userSubjectList': currentUserSubjectsList,
    }

    return render(request, profileTemplateName, context)

class AllUsersView(TemplateView):
    template_name = 'Authorization/allUsers.html'

    def get(self, request):

        ### Variables
        usernames = User.objects.all()
        usersId = User.objects.filter().values('id')  # Get all user id
        userGroups = [None] * len(usernames)
        usersGrade = [None] * len(usernames)
        user_list = [None] * len(usernames)


        for _ in range(len(usernames)):
            num = _ + 1

            ### Get first and last name, combine them and put into a list
            temp = User.objects.filter(username__icontains=usernames[_]).values('first_name',
                                                                'last_name')  # Get first name and last name
            temp = temp.__getitem__(0)  # Rewrite to make it regular dict

            firstName = temp.get('first_name')
            lastName = temp.get('last_name')
            fullName = firstName + ' ' + lastName  # Combine to make a single string with first and last names

            user_list[_] = fullName  # Write full name into list on a position


            temp = Student.objects.filter(user=num).values('group')
            temp = temp.__getitem__(0)
            temp = temp.get('group')

            temp = StudentGroupModel.objects.filter(pk=temp).values_list('name', 'grade')
            tempName = temp[0][0]
            userGroups[_] = tempName

            tempGrade = temp[0][1]
            tempGrade = GradeModel.objects.filter(pk=tempGrade).values_list('name')
            tempGrade = tempGrade[0][0]
            usersGrade[_] = tempGrade


        context = {
            'title': 'Пользователи',
            'usersInfo': zip(
                user_list,
                userGroups,
                usersGrade,
            ),
        }

        return render(request, self.template_name, context)

class AllSubjectsView(TemplateView):
    template_name = 'Authorization/allSubjects.html'

    def get(self, request):

        subjectsRaw = SubjectsModel.objects.filter().values_list('name')
        subjects = [None] * len(subjectsRaw)

        for _ in range(len(subjectsRaw)):
            temp = subjectsRaw[_][0]
            subjects[_] = temp

        context = {
            'title': 'Предметы',
            'subjects': subjects,
        }

        return render(request, self.template_name, context)


def search(request):
    template_name = 'Authorization/base.html'

    query = request.GET.get('search')
    result = []

    groupResultRaw = StudentGroupModel.objects.filter(Q(name__icontains=query)).values_list('name')
    nameResultRaw = User.objects.annotate(fullname=Concat('first_name', Value(' '), 'last_name'))
    nameResultRaw = nameResultRaw.filter(fullname__icontains=query)


    if len(groupResultRaw) > 0 and len(nameResultRaw) == 0:
        result = [None] * len(groupResultRaw)
        for _ in range(len(groupResultRaw)):
            temp = groupResultRaw.__getitem__(_)  # rewrite them to make a regular dict
            result[_] = temp[0]  # Write all id's into the list as regular strings
    elif len(groupResultRaw) == 0 and len(nameResultRaw) > 0:
        result = [None] * len(nameResultRaw)
        for _ in range(len(nameResultRaw)):
            temp = nameResultRaw.__getitem__(_)  # rewrite them to make a regular dict
            temp = User.objects.filter(username=temp).values('first_name', 'last_name')
            temp = temp.__getitem__(0)
            firstName = temp.get('first_name')
            lastName = temp.get('last_name')
            fullName = firstName + ' ' + lastName
            result[_] = fullName  # Write all id's into the list as regular strings

    context = {
        'search': query,
        'result': result,
    }
    return render(request, template_name, context)