# Generated by Django 4.0.4 on 2022-05-24 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_student_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.CharField(max_length=200)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.student')),
            ],
        ),
    ]
