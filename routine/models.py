from django.db import models

# Create your models here.

class Routine(models.Model):
    routine_id = models.IntegerField(primary_key=True)
    routine_name = models.CharField(max_length=10, blank=True, null=True, default=None)
    routine_comment = models.CharField(max_length=50, blank=True, null=True, default=None)
    recommend_count = models.IntegerField(blank=True, null=True, default=0)
    routine_day = models.IntegerField(blank=True, null=True, default=0)
    nickname = models.ForeignKey('accounts.User', on_delete=models.CASCADE, to_field='nickname', db_column= 'nickname')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'routine'

class RoutineDetail(models.Model):
    routine_detail_id = models.IntegerField(primary_key=True)
    routine = models.ForeignKey('Routine', on_delete=models.CASCADE, max_length=11)
    exercise = models.ForeignKey('Exer.Exercise', on_delete=models.CASCADE, max_length=11)
    usebody = models.ForeignKey('usebody.Usebody', on_delete=models.CASCADE, max_length=11)
    day = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routinedetail'

class RoutineBox(models.Model):
    box_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, max_length=11)
    routine = models.ForeignKey('Routine', on_delete=models.CASCADE, max_length=11)

    class Meta:
        managed = False
        db_table = 'box'