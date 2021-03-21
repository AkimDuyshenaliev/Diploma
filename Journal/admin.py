from django.contrib import admin

from .models import *


@admin.register(JournalPageModel)
class JournalPageModelAdmin(admin.ModelAdmin):
    list_display = ('full_name_display', 'group_name_display', 'grade', 'subject')
    list_filter = ('group', 'grade')

    def full_name_display(self, obj):
        return '{} {}'.format(obj.name.first_name, obj.name.last_name)

    def group_name_display(self, obj):
        return '{}'.format(obj.group.name)


admin.site.register(GradeModel)
admin.site.register(SubjectsModel)
admin.site.register(StudentGroupModel)
