from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets
from .permissions import IsCourseTeacher, IsLectureTeacher, IsHomeworkAuthor, IsMarkAuthor, IsCommentAuthor, IsUserAccount
from .models import Users, Courses, Lectures, HomeworkSolution, Mark, CommentsToHomework
from .serializers import UsersSerializer, CoursesSerializer, LecturesSerializer, HomeworkSolutionSerializer, \
    MarkSerializer, CommentsSerializer


class UsersView(viewsets.ModelViewSet):
    """
    View for work with Users table.
    """
    serializer_class = UsersSerializer
    queryset = Users.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsUserAccount]


class CoursesView(viewsets.ModelViewSet):
    """
    View for work with Courses table.
    'author' field if auto-creating.
    Permissions are in permissions.py
    """
    serializer_class = CoursesSerializer
    queryset = Courses.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsCourseTeacher]

    def perform_create(self, serializer):
        author = get_object_or_404(Users, user=self.request.user)
        serializer.save(author=author)


class LecturesView(viewsets.ModelViewSet):
    """
    View for work with Lectures table.
    Permissions are in permissions.py
    """
    serializer_class = LecturesSerializer
    permission_classes = [permissions.IsAuthenticated, IsLectureTeacher]

    def get_queryset(self):
        """
        Users get back the lectures at their courses.
        """
        user = get_object_or_404(Users, user=self.request.user)
        courses = []
        if user.role == 'Преподаватель':
            courses = list(Courses.objects.filter(author=user))  # list of courses, where user is author
            courses.extend(user.teachers.all())  # list of courses where user is teacher
        if user.role == 'Студент':
            courses = user.students.all()  # list of courses where user is student
        return Lectures.objects.filter(course__in=courses)


class HomeworkSolutionView(viewsets.ModelViewSet):
    """
    View for work with HomeworkSolution table.
    'author' field if auto-creating.
    Permissions are in permissions.py
    """
    serializer_class = HomeworkSolutionSerializer
    permission_classes = [permissions.IsAuthenticated, IsHomeworkAuthor]

    def get_queryset(self):
        """
        Teachers get back the homework done for their courses .
        Students get back their homeworks.
        """
        user = get_object_or_404(Users, user=self.request.user)
        if user.role == 'Преподаватель':
            teacher_courses = user.teachers.all()
            return HomeworkSolution.objects.filter(lecture__course__in=teacher_courses)
        if user.role == 'Студент':
            return user.homeworksolution_set.all()

    def perform_create(self, serializer):
        author = get_object_or_404(Users, user=self.request.user)
        serializer.save(author=author)


class MarkView(viewsets.ModelViewSet):
    """
    View for work with 'Mark' table.
    'checking_teacher' field if auto-creating.
    Permissions are in permissions.py
    """
    serializer_class = MarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsMarkAuthor]

    def get_queryset(self):
        """
        Teachers get back the marks done for their courses.
        Students get back the marks done for their homeworks.
        """
        user = get_object_or_404(Users, user=self.request.user)
        if user.role == 'Преподаватель':
            teacher_courses = list(Courses.objects.filter(author=user))
            teacher_courses.extend(user.teachers.all())
            return Mark.objects.filter(homework__lecture__course__in=teacher_courses)
        if user.role == 'Студент':
            student_homeworks = user.homeworksolution_set.all()
            return Mark.objects.filter(homework__in=student_homeworks)

    def perform_create(self, serializer):
        checking_teacher = get_object_or_404(Users, user=self.request.user)
        serializer.save(checking_teacher=checking_teacher)


class CommentsToHomeworkView(viewsets.ModelViewSet):
    """
    View for work with 'CommentsToHomework' table.
    'author' field if auto-creating.
    Permissions are in permissions.py
    """
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthor]

    def get_queryset(self):
        """
        Teachers get back the comments done for their courses.
        Students get back the comments done for their homeworks.
        """
        user = get_object_or_404(Users, user=self.request.user)
        if user.role == 'Преподаватель':
            teacher_courses = user.teachers.all()
            return CommentsToHomework.objects.filter(homework__lecture__course__in=teacher_courses)
        if user.role == 'Студент':
            student_homeworks = user.homeworksolution_set.all()
            return CommentsToHomework.objects.filter(homework__in=student_homeworks)

    def perform_create(self, serializer):
        author = get_object_or_404(Users, user=self.request.user)
        serializer.save(author=author)
