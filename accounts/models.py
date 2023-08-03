from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    nickname = models.CharField(max_length=10, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

class Userinfo(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    bmi = models.FloatField(blank=True, null=True)
    info = models.CharField(max_length=100, blank=True, null=True)
    accvisibility = models.IntegerField(db_column='accVisibility', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userinfo'
