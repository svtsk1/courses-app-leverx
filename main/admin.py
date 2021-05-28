from django.contrib import admin
from .models import Users, Courses, Lectures, HomeworkSolution, Mark, CommentsToHomework

admin.site.register(Users)
admin.site.register(Courses)
admin.site.register(Lectures)
admin.site.register(HomeworkSolution)
admin.site.register(Mark)
admin.site.register(CommentsToHomework)
