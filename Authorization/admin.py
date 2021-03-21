from django.contrib import admin

from .models import *

@admin.register(Student)
class StudentAdminForm(admin.ModelAdmin):
    list_display = ('full_name_display', 'group_name_display', 'cours_display')
    list_filter = ('group',)

    def full_name_display(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    def group_name_display(self, obj):
        return '{}'.format(obj.group.name)

    def cours_display(self, obj):
        return '{}'.format(obj.group.grade.name)