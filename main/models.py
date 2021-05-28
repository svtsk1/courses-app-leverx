from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    ROLE_CHOICES = (
        ('Преподаватель', 'Преподаватель'),
        ('Студент', 'Студент')
    )
    role = models.CharField(max_length=13, choices=ROLE_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Профили пользователя'
        verbose_name_plural = 'Профили пользователей'


class Courses(models.Model):
    title = models.CharField(max_length=111)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    students = models.ManyToManyField(Users, related_name='students', blank=True)
    teachers = models.ManyToManyField(Users, related_name='teachers', blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lectures(models.Model):
    topic = models.CharField(max_length=111)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='lectures_at_course')
    file = models.FileField(null=True, blank=True, upload_to='lecture_files/')
    homework = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'


class HomeworkSolution(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lectures, on_delete=models.CASCADE)
    solution = models.TextField(null=True, blank=True)
    attached_file = models.FileField(null=True, blank=True, upload_to='homework_solutions/')

    def __str__(self):
        return f'Домашнее задание {self.author} к лекции {self.lecture}'

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'


class Mark(models.Model):
    MARK_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    homework = models.OneToOneField(HomeworkSolution, on_delete=models.CASCADE)
    mark = models.IntegerField(choices=MARK_CHOICES)
    checking_teacher = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return f'Оценка преподавателя {self.checking_teacher} к решению {self.homework.author}'

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class CommentsToHomework(models.Model):
    homework = models.ForeignKey(HomeworkSolution, on_delete=models.CASCADE)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'Комментарий пользователя {self.author} к решению {self.homework.author}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
