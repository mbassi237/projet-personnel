# Generated by Django 5.1.3 on 2024-12-03 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Start_Date', models.DateField()),
                ('End_Date', models.DateField()),
                ('Status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=50)),
                ('Created_At', models.DateTimeField(auto_now_add=True)),
                ('Updated_At', models.DateTimeField(auto_now=True)),
                ('Mentee_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentorships_as_mentee', to='user.customuser')),
                ('Mentor_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentorships_as_mentor', to='user.customuser')),
            ],
        ),
    ]