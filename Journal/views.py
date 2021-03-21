import re

from datetime import date

from django import template
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.text import slugify
from django.db.models import Q, Value
from django.urls import reverse

from django.contrib.auth.models import User

from Authorization.models import *
from .models import *
from .forms import *
from .methods import (
    get_ids_marks_and_markdates,
    compate_and_save_marks,
    compare_and_save_dates,
)


class MainPageView(TemplateView):
    name = 'Journal/mainPage.html'

    def get(self, request):

        gradesIdsList = GradeModel.objects.all().values_list('id', flat=True)
        gradesRaw = GradeModel.objects.filter().values('name')

        groupsRaw = StudentGroupModel.objects.all().order_by('grade').values_list('name',
                                                                                  'grade')  # By the order of 'grade' take fields 'name' and 'grade' and return them as a tuple in a list

        grades = [None] * len(gradesRaw)
        groups = [[] for _ in range(len(gradesIdsList))]
        groupsSlugifyed = [[] for _ in range(len(gradesIdsList))]

        for _ in range(len(grades)):
            tempGrades = gradesRaw.__getitem__(_)  # rewrite them to make a regular dict
            grades[_] = tempGrades.get('name')  # Write all grade names into the list as regular strings

        for _ in range(len(gradesIdsList)):
            for j in range(len(groupsRaw)):
                if groupsRaw[j][1] == (_ + 1):
                    groups[_].append(groupsRaw[j][0])
                    groupsSlugifyed[_].append(slugify(groupsRaw[j][0], allow_unicode=True))

        context = {
            'title': 'Главная страница',
            'mainPageInfo': zip(
                grades,
                groups,
                groupsSlugifyed,
            ),
        }
        return render(request, self.name, context)


class GroupPageView(TemplateView):
    name = 'Journal/groupPage.html'

    def get(self, request, group_slug):
        chosenGroup = StudentGroupModel.objects.filter(name__icontains=group_slug).values('subjects')
        groupID = StudentGroupModel.objects.filter(name__icontains=group_slug).values_list('pk')
        groupStudentsIDs = Student.objects.filter(group=groupID[0][0]).values('user')

        subjectNames = [None] * len(chosenGroup)
        subjectNamesSlugged = [None] * len(chosenGroup)

        groupUserNames = [None] * len(groupStudentsIDs)

        for _ in range(len(groupStudentsIDs)):
            temp = User.objects.filter(pk=groupStudentsIDs[_]['user']).values_list('first_name', 'last_name')
            temp = temp[0][0] + ' ' + temp[0][1]
            groupUserNames[_] = temp

        for _ in range(len(chosenGroup)):
            temp = chosenGroup.__getitem__(_)
            temp = temp.get('subjects')

            temp = SubjectsModel.objects.filter(pk=temp).values('name')
            temp = temp.__getitem__(0)
            temp = temp.get('name')

            subjectNames[_] = temp
            subjectNamesSlugged[_] = slugify(temp, allow_unicode=True)

        context = {
            'title': group_slug.upper(),
            'subjects': zip(
                subjectNames,
                subjectNamesSlugged,
            ),
            'userNames': groupUserNames,
        }

        return render(request, self.name, context)


class JournalPageView(TemplateView):
    name = 'Journal/journal.html'
    DATE_FORMAT = "%d-%m-%Y"

    def get(self, request, group_slug, subject):
        ### Variables

        group = group_slug.upper()
        groupID = StudentGroupModel.objects.filter(name__icontains=group).values('pk')
        groupID = groupID[0]['pk']

        currentSubject = subject.capitalize()
        currentSubject = re.sub("-", " ", currentSubject)

        currentSubjectID = SubjectsModel.objects.filter(Q(name__icontains=currentSubject)).values('id')
        currentSubjectID = currentSubjectID[0]['id']

        usersWithGroupAndSubjectRaw = JournalPageModel.objects.filter(Q(group=groupID, subject=currentSubjectID)).values('name')
        usersWithGroupAndSubject = [None] * len(usersWithGroupAndSubjectRaw)

        for _ in range(len(usersWithGroupAndSubjectRaw)):
            usersWithGroupAndSubject[_] = usersWithGroupAndSubjectRaw[_]['name']

        usernames = User.objects.filter(pk__in=usersWithGroupAndSubject).values('username')
        usersId = User.objects.filter(pk__in=usersWithGroupAndSubject).values('id') # Get all user id

        # print('\n',
        # 'Group ID', groupID, '\n',
        # 'Current subject ID', currentSubjectID, '\n',
        # 'Current group with subject', usersWithGroupAndSubject, '\n',
        # 'Usernames', usernames, '\n',
        # 'User ID', usersId, '\n',
        # )

        ### Get today and parse it into a string with dd/mm/YY
        today = date.today()

        today = today.strftime("%Y/%m/%d")
        today = re.sub('/', '-', today)

        ### Call function to get user id list mark lists and mark date list
        func = get_ids_marks_and_markdates(usernames, usersId, currentSubjectID)

        ### Put function return into a variables
        userIdList = func[0]
        user_list = func[1]
        user_marks = func[2]
        user_markdates = func[3]

        # print('\n', 'User id - ', userIdList, '\n',
        # 'User list - ', user_list, '\n',
        # 'User marks - ', user_marks, '\n',
        # 'User markdates - ', user_markdates,  '\n',)

        context = {
            'userMarkDates': user_markdates,
            'today': today,
            'student': zip(
                userIdList,
                user_list,
                user_marks,
            ),
            'group': group,
            'subject': currentSubject,
            'title': 'Страница журнала',
        }
        return render(request, self.name, context)

    def post(self, request, group_slug, subject):
        ### Variables
        group = group_slug.upper()
        groupID = StudentGroupModel.objects.filter(name__icontains=group).values('pk')
        groupID = groupID[0]['pk']

        currentSubject = subject.capitalize()
        currentSubject = re.sub("-", " ", currentSubject)

        currentSubjectID = SubjectsModel.objects.filter(Q(name__icontains=currentSubject)).values('id')
        currentSubjectID = currentSubjectID[0]['id']

        usersWithGroupAndSubjectRaw = JournalPageModel.objects.filter(Q(group=groupID, subject=currentSubjectID)).values('name')
        usersWithGroupAndSubject = [None] * len(usersWithGroupAndSubjectRaw)

        for _ in range(len(usersWithGroupAndSubjectRaw)):
            usersWithGroupAndSubject[_] = usersWithGroupAndSubjectRaw[_]['name']

        usernames = User.objects.filter(pk__in=usersWithGroupAndSubject).values('username')
        usersId = User.objects.filter(pk__in=usersWithGroupAndSubject).values('id')  # Get all user id

        newMarks = [None] * len(usernames)

        ### Call function to get user id list mark lists and mark date list
        func = get_ids_marks_and_markdates(usernames, usersId, currentSubjectID)

        ### Put function return into a variables
        userIdList = func[0]
        user_list = func[1]
        user_marks = func[2]
        user_markdates = func[3]

        i = 0
        j = 0

        ### Initialize oldMarks 2d array
        receivedMarks = []
        for i in range(len(usernames)):
            column = []
            for j in range(len(user_marks[i])):
                column.append(None)
            receivedMarks.append(column)

        receivedMarkDates = [None] * len(user_markdates)

        # print('\n', 'Post request data', request.POST, '\n',
        #       'User id list', userIdList, '\n',
        #       'Existing marks', user_marks, '\n',
        #       'Existing mark dates', user_markdates, '\n')


        ### Get data from HTML form

        for _ in range(len(usernames)):
            newMarks[_] = request.POST.get(user_list[_])

            for j in range(len(user_marks[_])):
                receivedMarks[_][j] = request.POST.get(
                    'User_' + user_list[_] + '_loopcounter_' + str(j + 1) + '_mark_' + str(user_marks[_][j]))

        for _ in range(len(user_markdates)):
            receivedMarkDates[_] = request.POST.get('date_' + str(_ + 1))

        newDate = request.POST.get('date')

        # print('\n', 'New marks', newMarks, '\n',
        #       'Received marks', receivedMarks, '\n',
        #       'Received mark dates', receivedMarkDates, '\n',
        #       'New date', newDate, '\n')

        ### Check if new and old marks and dates are identical

        compate_and_save_marks(usernames, userIdList, user_marks, receivedMarks, currentSubjectID)
        compare_and_save_dates(usernames, userIdList, user_marks, user_markdates, receivedMarkDates, currentSubjectID)

        ### Save data from HTML form to database
        for _ in range(len(usernames)):
            user = JournalPageModel.objects.get(name=userIdList[_], subject=currentSubjectID)
            if len(user.marks) == 1 and user.marks == [
                '-']:  ### If there is only one entry and that entry is default "-" then...
                ### Replace the default entry with the mark
                user.marks.pop()
                user.marks.append(newMarks[_])

                ### Replace the entry with the date
                user.marksDate.pop()
                user.marksDate.append(newDate)

                user.save()
            elif newMarks[_] == '':
                pass
            else:
                ### Append the mark
                user.marks.append(newMarks[_])

                ### Append the date
                user.marksDate.append(newDate)

                user.save()

        return redirect(reverse('Journal:JournalPage', kwargs={'group_slug': group_slug, 'subject': subject}))
