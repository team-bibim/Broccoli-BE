# Generated by Django 4.0.3 on 2023-08-03 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('exercise_id', models.IntegerField(primary_key=True, serialize=False)),
                ('exerciseName_English', models.CharField(blank=True, max_length=50, null=True)),
                ('exerciseName_Korean', models.CharField(blank=True, max_length=50, null=True)),
                ('equipment_name', models.CharField(blank=True, max_length=50, null=True)),
                ('videolink', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'exercise',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usebody',
            fields=[
                ('usebody_id', models.IntegerField(primary_key=True, serialize=False)),
                ('usebody_name', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'usebody',
                'managed': False,
            },
        ),
    ]
