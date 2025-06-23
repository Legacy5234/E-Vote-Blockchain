from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

#---------------------------------------------------------------------------------------------------------
# ACCOUNT CREATION
#---------------------------------------------------------------------------------------------------------
class College(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return f"{self.name} ({self.college.name})"


#---------------------------------------------------------------------------------------------------------
# CUSTOM USER CREATION MODEL
#---------------------------------------------------------------------------------------------------------
class StaffAccountManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )


#---------------------------------------------------------------------------------------------------------
# CUSTOM USER MODEL
#---------------------------------------------------------------------------------------------------------
class Voter_User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    location = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = StaffAccountManager()

    def __str__(self):
        return f'{self.username} ({self.email})'



    

#---------------------------------------------------------------------------------------------------------
# PROFILE MODEL
#---------------------------------------------------------------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(Voter_User, on_delete=models.CASCADE, related_name='profile')

    image = models.ImageField(upload_to='E-Vote-Profile Images', null=True)

    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True)

    @property
    def profile_image(self):
        if self.image:
            return self.image.url
        return static('images/avatar_default.svg')
    
    def __str__(self):
        return f'{self.user.username}'
