import re

from datetime import date
from django.contrib.auth.models import User

from .models import *

def get_ids_marks_and_markdates(usernames, usersId, subjectID):
    today = date.today()

    today = today.strftime("%Y/%m/%d")
    today = re.sub('/', '-', today)

    userIdList = [None] * len(usernames)
    user_list = [None] * len(usernames)
    user_marks = [None] * len(usernames)
    user_markdates = [None] * len(usernames)


    ### Write all user ID's into a list
    for _ in range(len(usernames)):
        tempUserId = usersId.__getitem__(_)  # rewrite them to make a regular dict
        userIdList[_] = tempUserId.get('id')  # Write all id's into the list as regular strings

    for _ in range(len(usernames)):
        ### Get first and last name, combine them and put into a list
        temp = User.objects.filter(id=userIdList[_]).values('first_name',
                                                                    'last_name')  # Get first name and last name
        temp = temp.__getitem__(0)  # Rewrite to make it regular dict

        firstName = temp.get('first_name')
        lastName = temp.get('last_name')
        fullName = firstName + ' ' + lastName  # Combine to make a single string with first and last names

        user_list[_] = fullName  # Write full name into list on a position

        ### Get marks by user ID and current subject
        tempUserMarks = JournalPageModel.objects.filter(name=userIdList[_], subject=subjectID).values('marks')  # Get all marks of a selected id
        temp = tempUserMarks[0]
        temp = temp.get('marks')

        if len(tempUserMarks) == 0:
            if len(temp) == 0:
                user_marks[_] = '-'
            elif re.search('\D', temp[0]):
                user_marks[_] = '-'
        else:
            tempUserMarks = tempUserMarks.__getitem__(0)  # Rewrite them to make a regular dict
            user_marks[_] = tempUserMarks.get('marks')  # Write user marks into the dict


    ### Get mark dates by user ID and current subject
    tempUserMarkDates = JournalPageModel.objects.filter(name=userIdList[0], subject=subjectID).values('marksDate') # Get all mark dates of a selected id
    temp = tempUserMarkDates[0]
    temp = temp.get('marksDate')

    if len(temp) == 0:
        user_markdates = []
    elif len(userIdList) == 1:
        tempUserMarkDates = tempUserMarkDates.__getitem__(0)  # Rewrite them to make a regular dict
        tempUserMarkDates = tempUserMarkDates.get('marksDate')  # Write user marks into the dict

        user_markdates = tempUserMarkDates

    else:
        tempUserMarkDates = tempUserMarkDates.__getitem__(0)  # Rewrite them to make a regular dict
        user_markdates[_] = tempUserMarkDates.get('marksDate')  # Write user marks into the dict

        if len(user_markdates) >= 2:
            user_markdates = user_markdates[_]

    return(userIdList, user_list, user_marks, user_markdates)


def compate_and_save_marks(usernames, userIdList, user_marks, receivedMarks, subjectID):
    for _ in range(len(usernames)):
        user = JournalPageModel.objects.get(name=userIdList[_], subject=subjectID)
        for j in range(len(user_marks[_])):
            if user_marks[_] == receivedMarks[_][j]:
                continue
            else:
                user.marks = receivedMarks[_]

                user.save()
                break


def compare_and_save_dates(usernames, userIdList, user_marks, user_markdates, receivedMarkDates, subjectID):
    for _ in range(len(usernames)):
        user = JournalPageModel.objects.get(name=userIdList[_], subject=subjectID)
        for j in range(len(user_marks[_])):
            if len(user_markdates) == 1:
                if user_markdates[_] == receivedMarkDates[_]:
                    continue
                else:
                    user.marksDate = receivedMarkDates

                    user.save()
                    break
            else:
                if user_markdates[j] == receivedMarkDates[j]:
                    continue
                else:
                    user.marksDate = receivedMarkDates

                    user.save()
                    break