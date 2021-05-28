from rest_framework import serializers
from .models import Users, Courses, Lectures, HomeworkSolution, Mark, CommentsToHomework


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'id',
            'role',
            'user',
        )


class LecturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lectures
        fields = (
            'id',
            'topic',
            'course',
            'file',
            'homework',
        )


class CoursesSerializer(serializers.ModelSerializer):
    lectures_at_course = LecturesSerializer(many=True)

    class Meta:
        model = Courses
        fields = (
            'id',
            'title',
            'author',
            'students',
            'teachers',
            'lectures_at_course',
        )
        read_only_fields = ['author']


class HomeworkSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkSolution
        fields = (
            'id',
            'author',
            'lecture',
            'solution',
            'attached_file',
        )
        read_only_fields = ['author']


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = (
            'id',
            'homework',
            'mark',
            'checking_teacher',
        )
        read_only_fields = ['checking_teacher']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsToHomework
        fields = (
            'id',
            'homework',
            'author',
            'text',
        )
        read_only_fields = ['author']
