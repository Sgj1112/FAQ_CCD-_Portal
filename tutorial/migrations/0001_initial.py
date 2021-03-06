# Generated by Django 3.0.1 on 2020-01-30 19:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ques',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('answer', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('date_asked', models.DateTimeField(default=django.utils.timezone.now)),
                ('asked_by', models.CharField(max_length=50)),
            ],
        ),
    ]
