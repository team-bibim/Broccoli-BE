from django.db import models

class Exercise(models.Model):
    exercise_id = models.IntegerField(primary_key=True)
    usebody = models.ForeignKey('usebody.Usebody', on_delete=models.CASCADE, max_length=11)
    exerciseName_English= models.CharField(max_length=50, blank=True, null=True)
    exerciseName_Korean = models.CharField(max_length=50, blank=True, null=True)
    equipment_name = models.CharField(max_length=50, blank=True, null=True)
    videolink =  models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exercise'


# class Exercise(models.Model):
#     exercise_id = models.IntegerField(primary_key=True)
#     usebody = models.ForeignKey('Usebody', models.DO_NOTHING, blank=True, null=True)
#     exercisename_english = models.CharField(db_column='exerciseName_english', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     exercisename_korean = models.CharField(db_column='exerciseName_korean', max_length=50, blank=True, null=True)  # Field name made lowercase.
#     equipment_name = models.CharField(max_length=50, blank=True, null=True)
#     videolink = models.CharField(max_length=150, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'exercise'
