# Generated by Django 5.0.6 on 2024-05-23 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_organizationprofile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationprofile',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]