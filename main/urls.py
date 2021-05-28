from django.urls import path, include
from .views import UsersView, CoursesView, LecturesView, HomeworkSolutionView, MarkView, CommentsToHomeworkView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UsersView, basename='UsersView')
router.register('courses', CoursesView, basename='CoursesView')
router.register('lectures', LecturesView, basename='LecturesView')
router.register('homeworks', HomeworkSolutionView, basename='HomeworkSolutionView')
router.register('marks', MarkView, basename='MarkView')
router.register('comments', CommentsToHomeworkView, basename='CommentsToHomeworkView')

urlpatterns = [
    path('', include(router.urls))
]
