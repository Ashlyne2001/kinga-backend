# Generated by Django 3.2.12 on 2023-10-26 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(0, 'admin'), (5, 'Privileged'), (1, 'Employee'), (2, 'Receipt Api User')], default=0, verbose_name='user type'),
        ),
    ]
