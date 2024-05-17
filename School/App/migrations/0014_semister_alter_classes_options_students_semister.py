# Generated by Django 4.2.6 on 2024-05-15 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_students_issuedamount_students_issuedby_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SemisterName', models.CharField(blank=True, max_length=200, null=True, verbose_name='Semister Name')),
                ('SemisterFee', models.IntegerField(blank=True, default=0, null=True, verbose_name='Semister Total Fee')),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('Updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Semisters',
            },
        ),
        migrations.AlterModelOptions(
            name='classes',
            options={},
        ),
        migrations.AddField(
            model_name='students',
            name='Semister',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.semister'),
        ),
    ]
