# Generated by Django 4.2.6 on 2024-05-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0015_alter_classes_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='SemisterFee',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Semister Fee'),
        ),
    ]
