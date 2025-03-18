from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


ROLE_CHOICES = (
    ('student', 'Student'),
    ('teacher', 'Teacher'),
)

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  
        blank=True
    )



class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    enrollment_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"Student: {self.user.username}, Department: {self.department}"



class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )
    employee_id = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=50) 

    def __str__(self):
        return f"Teacher: {self.user.username}, Subject: {self.subject}"



class Book(models.Model):
    title = models.CharField(max_length=255)  
    author = models.CharField(max_length=255) 

    def __str__(self):
        return f"Book: {self.title}, Author: {self.author}"
