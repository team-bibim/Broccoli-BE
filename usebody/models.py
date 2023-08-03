from django.db import models

# Create your models here.
class Usebody(models.Model):
    usebody_id = models.IntegerField(primary_key=True)
    usebody_name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usebody'