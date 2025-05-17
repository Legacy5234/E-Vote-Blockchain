from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

#---------------------------------------------------------------------------------------------------------
# ACCOUNT CREATION
#---------------------------------------------------------------------------------------------------------
class StaffAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Username of staff not found')
        if not email:
            raise ValueError('Staff email is missing')
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # ADMIN USER ACCOUNT CREATION
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password
        )

        user.is_superuser = True
        user.is_active = True
        user.is_staff = True

        user.save(using=self._db)
        return user




#---------------------------------------------------------------------------------------------------------
# CUSTOM USER MODEL
#---------------------------------------------------------------------------------------------------------
class Voter_User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True, blank=False)
    email = models.EmailField(unique=True)

    # FLAGS
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    # SIGN-UP METHOD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = StaffAccountManager()

    def __str__(self):
        return f'{self.username} : {self.email}'
    

#---------------------------------------------------------------------------------------------------------
# PROFILE MODEL
#---------------------------------------------------------------------------------------------------------
GENDER = (
    ('Male','Male'),('Female','Female'),
)

class Profile(models.Model):
    user = models.OneToOneField(Voter_User, on_delete=models.CASCADE, related_name='profile')

    image = models.ImageField(upload_to='VoteChain-profileimages/', null=True, blank=True)
    
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30)
    gender = models.CharField(max_length=20, choices=GENDER)

    location = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True)


    @property
    def profile_image(self):
        if self.image:
            return self.image.url
        return static('images/avatar_default.svg')
    

    @property
    def full_name(self):
        return f"{self.first_name} {self.surname} {self.middle_name}"

    

    def __str__(self):
        return f'{self.user.username}'
