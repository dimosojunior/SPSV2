# Generated by Django 4.2.6 on 2024-05-16 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0016_classes_semisterfee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Years',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Year', models.CharField(blank=True, max_length=200, null=True, verbose_name='Year')),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('Updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Years',
            },
        ),
        migrations.AddField(
            model_name='students',
            name='Year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='App.years'),
        ),
    ]