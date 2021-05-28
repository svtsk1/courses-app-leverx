from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import Users, Courses, HomeworkSolution


class IsUserAccount(permissions.BasePermission):
    """
    Check if request user if owner of user profile at course
    """

    def has_permission(self, request, view):
        user = get_object_or_404(Users, user=request.user)
        if view.action in ['create']:
            if len(request.data) == 0:
                return True
            return True if request.data['user'] == user.user.pk else False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        user = get_object_or_404(Users, user=request.user)
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            return True if user.user == obj.user else False


class IsCourseTeacher(permissions.BasePermission):
    """
    Check if user is teacher at course or not.
    Students can only read courses.
    """

    def has_permission(self, request, view):
        author = get_object_or_404(Users, user=request.user)
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return True if author.role == 'Преподаватель' else False

    def has_object_permission(self, request, view, obj):
        author = get_object_or_404(Users, user=request.user)
        if view.action in ['retrieve']:
            return True

        if view.action in ['update', 'partial_update', 'destroy']:
            return True if author == obj.author or author in obj.teachers.all() else False


class IsLectureTeacher(permissions.BasePermission):
    """
    Check if user is teacher at lecture or not.
    Students can only read lectures.
    """

    def has_permission(self, request, view):
        author = get_object_or_404(Users, user=request.user)
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            return True if author.role == 'Преподаватель' else False
        elif view.action in ['create']:
            if len(request.data) == 0:
                return True
            course = get_object_or_404(Courses, pk=request.data['course'])
            return True if author.role == 'Преподаватель' and \
                           (author in course.teachers.all() or author == course.author) else False

    def has_object_permission(self, request, view, obj):
        author = get_object_or_404(Users, user=request.user)
        if view.action in ['retrieve']:
            return True

        if view.action in ['update', 'partial_update', 'destroy']:
            return True if author.role == 'Преподаватель' else False


class IsHomeworkAuthor(permissions.BasePermission):
    """
    Teachers can only read homeworks.
    Students can do anything(because get_queryset() return only their homeworks)
    """

    def has_permission(self, request, view):
        author = get_object_or_404(Users, user=request.user)
        if author.role == 'Преподаватель':
            return True if view.action in ['list', 'retrieve'] else False

        elif author.role == 'Студент':
            return True


class IsMarkAuthor(permissions.BasePermission):
    """
    Teachers can do anything(because get_queryset() return marks at their courses).
    Students can only read marks.
    """
    def has_permission(self, request, view):
        author = get_object_or_404(Users, user=request.user)
        if view.action in ['retrieve', 'list']:
            return True
        if view.action in ['update', 'partial_update', 'destroy']:
            if author.role == 'Преподаватель':
                return True
        if view.action in ['create']:
            if len(request.data) == 0:
                return True
            homework = get_object_or_404(HomeworkSolution, pk=request.data['homework'])
            return True if author in homework.lecture.course.teachers.all() or \
                           author == homework.lecture.course.author else False

    def has_object_permission(self, request, view, obj):
        author = get_object_or_404(Users, user=request.user)
        if view.action in ['update', 'partial_update', 'destroy']:
            return True if obj.checking_teacher == author or \
                           author in obj.homework.lecture.course.teachers.all() or \
                           author == obj.homework.lecture.course.author else False
        else:
            return True


class IsCommentAuthor(permissions.BasePermission):
    """
    Users can update or delete only their comments.
    """
    def has_permission(self, request, view):
        author = get_object_or_404(Users, user=request.user)
        if view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return True
        if view.action in ['create']:
            if len(request.data) == 0:
                return True
            homework = get_object_or_404(HomeworkSolution, pk=request.data['homework'])
            return True if author in homework.lecture.course.teachers.all() or \
                           author == homework.lecture.course.author else False

    def has_object_permission(self, request, view, obj):
        author = get_object_or_404(Users, user=request.user)
        if view.action in ['retrieve', 'create']:
            return True

        if view.action in ['update', 'partial_update', 'destroy']:
            return True if author == obj.author else False
