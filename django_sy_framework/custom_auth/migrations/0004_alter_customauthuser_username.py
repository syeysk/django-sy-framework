# Generated by Django 4.2.1 on 2024-04-04 19:31

from django.db import migrations, models
import django_sy_framework.custom_auth.validators


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_delete_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customauthuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.', max_length=150, validators=[django_sy_framework.custom_auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
