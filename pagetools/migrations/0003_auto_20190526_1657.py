# Generated by Django 2.2.1 on 2019-05-26 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagetools', '0002_auto_20190521_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageownerbytokenuser',
            name='token_user_profile',
            field=models.ManyToManyField(blank=True, null=True, to='pagetools.TokenUserProfile'),
        ),
    ]