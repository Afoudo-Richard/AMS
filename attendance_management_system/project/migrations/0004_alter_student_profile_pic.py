# Generated by Django 4.0.4 on 2022-05-24 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_student_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='students'),
        ),
    ]
