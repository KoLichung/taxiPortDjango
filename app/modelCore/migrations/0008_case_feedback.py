# Generated by Django 4.1.6 on 2023-03-08 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0007_alter_case_case_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='feedback',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
