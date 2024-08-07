# Generated by Django 3.2.12 on 2023-10-15 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0003_auto_20231015_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(default='', max_length=50, verbose_name='model name')),
                ('color', models.CharField(default='', max_length=50, verbose_name='from location name')),
                ('registration_number', models.CharField(default='', max_length=50, verbose_name='registration number')),
                ('year_of_manufacture', models.BigIntegerField(default=0, verbose_name='year of manufacture')),
                ('reg_no', models.BigIntegerField(db_index=True, default=0, unique=True, verbose_name='reg no')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.driver')),
            ],
        ),
    ]
