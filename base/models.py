from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from stats.models import Semester


class University(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=300)
    email_pattern = models.CharField(max_length=100)  # university pattern
    sid_pattern = models.CharField(max_length=100)  # student id pattern

    def validate_email(self, email):
        return True
        # return email.endswith(self.email_pattern)

    def validate_sid(self, sid):
        return True
        # return sid.startswith(self.sid_pattern)

    def __str__(self):
        return f'{self.name}'


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **other_fields)

    def create_user(self, email, first_name, last_name, password, username, department, university, **other_fields):
        # Validations
        if not email:
            raise ValueError(_('You must provide an email address'))
        if university.validate_email(email) is False:
            raise ValueError(_('You must provide a valid email address'))
        if not username:
            raise ValueError(_('You must provide a student ID'))
        if university.validate_sid(username) is False:
            raise ValueError(_('You must provide a valid student ID'))

        # Normalizations and creation 
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, username=username,
                          department=department, university=university, **other_fields)
        user.set_password(password)
        user.save()
        return user


# Create user extending default user model
class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(_('Email Address'), max_length=100, unique=True)
    username = models.CharField(_('Student ID'), max_length=20, unique=True)
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    profile_picture = models.FileField(upload_to='profile_pictures/', default='profile_pictures/avatar-male.png')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'department', 'university']

    objects = CustomAccountManager()

    def __str__(self):
        return self.username


class Content(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.FileField(upload_to='thumbnails/', default='thumbnails/default.jpg')
    course_code = models.CharField(max_length=100)
    file = models.FileField(upload_to='content/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.user})'


class Reaction(models.Model):
    id = models.AutoField(primary_key=True)
    reaction = models.IntegerField()  # 1: like, 2: dislike
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reaction} ({self.user})'


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content} ({self.user})'


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.IntegerField()  # 1: comment, 2: reaction, 3: reply, 4: mention, 5: content approved, 6: content rejected
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type} ({self.user})'


class Unread_Counts(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.IntegerField(default=0)
    message = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} ({self.user})'


class What_if(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    gpa = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.semester.name} ({self.gpa})'
