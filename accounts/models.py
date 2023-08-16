from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# class User(models.Model):
#     user_id = models.IntegerField(primary_key=True)
#     nickname = models.CharField(max_length=10, blank=True, null=True)
#     password = models.CharField(max_length=20, blank=True, null=True)
#     email = models.CharField(max_length=100, blank=True, null=True)
#
#     # USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['username']
#
#     class Meta:
#         managed = False
#         db_table = 'user'
#         db_table_comment = '사용자 데이터'

# class User(AbstractBaseUser):
#     user_id = models.AutoField(primary_key=True)
#     nickname = models.CharField(max_length=10, blank=True, null=True)
#     password = models.CharField(max_length=20, blank=True, null=True)
#     email = models.CharField(max_length=100, blank=True, null=True, unique=True)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     class Meta:
#         managed = False
#         db_table = 'user'
#         db_table_comment = '사용자 데이터'


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # email=email,
            nickname=nickname
        )
        user.set_password(password)
        #print(user.password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, nickname=None, password=None):
        superuser = self.create_user(
            email=email,
            nickname=nickname,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    nickname = models.CharField(max_length=20, blank=False, null=False, unique=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

# class Userinfo(models.Model):
#     user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
#     height = models.IntegerField(blank=True, null=True)
#     weight = models.FloatField(blank=True, null=True)
#     bmi = models.FloatField(blank=True, null=True)
#     info = models.CharField(max_length=100, blank=True, null=True)
#     accvisibility = models.IntegerField(db_column='accVisibility', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'userinfo'
#         db_table_comment = '사용자 정보'
