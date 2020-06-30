# Generated by Django 3.0.5 on 2020-06-30 14:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masks_auth', '0003_auto_20200519_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.CharField(blank=True, help_text='Position in company or institution.', max_length=256, null=True, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default='+999999999', help_text='+999999999 Up to 15 digits allowed', max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone number'),
            preserve_default=False,
        ),
    ]
