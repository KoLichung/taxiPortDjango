# Generated by Django 4.1.6 on 2023-02-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelCore', '0005_case_expect_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='case_type',
            field=models.CharField(choices=[('direct', 'direct'), ('reserve', 'reserve')], default='', max_length=20),
        ),
        migrations.AddField(
            model_name='case',
            name='reserve_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
