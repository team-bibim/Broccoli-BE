from django.db import models

class Exercise(models.Model):
    exercise_id = models.IntegerField(primary_key=True)
    usebody_id = models.ForeignKey('Usebody', on_delete=models.CASCADE, max_length=11)
    exerciseName_English= models.CharField(max_length=50, blank=True, null=True)
    exerciseName_Korean = models.CharField(max_length=50, blank=True, null=True)
    equipment_name = models.CharField(max_length=50, blank=True, null=True)
    videolink =  models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exercise'
