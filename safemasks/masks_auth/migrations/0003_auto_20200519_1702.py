# Generated by Django 3.0.5 on 2020-05-19 15:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('masks_auth', '0002_auto_20200518_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.CharField(blank=True, help_text='Name of your company or institution.', max_length=256, null=True, verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, help_text='Additional information, descriptions and references.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ip',
            field=models.GenericIPAddressField(blank=True, help_text='Ip address associated with user.', null=True, verbose_name='IP address'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_reviewed',
            field=models.BooleanField(default=False, help_text='Was the authenticity of the user reviewed by the administration?', verbose_name='Is reviewed?'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, help_text='Last time the profile was updated.', verbose_name='Last update'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, help_text='+999999999 Up to 15 digits allowed', max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(help_text='User instance.', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
