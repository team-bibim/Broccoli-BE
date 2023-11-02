# Generated by Django 4.0.3 on 2023-10-06 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('routine_id', models.IntegerField(primary_key=True, serialize=False)),
                ('routine_name', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('routine_comment', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('recommend_count', models.IntegerField(blank=True, default=0, null=True)),
                ('routine_day', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'routine',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoutineBox',
            fields=[
                ('box_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'box',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RoutineDetail',
            fields=[
                ('routine_detail_id', models.IntegerField(primary_key=True, serialize=False)),
                ('day', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'routinedetail',
                'managed': False,
            },
        ),
    ]