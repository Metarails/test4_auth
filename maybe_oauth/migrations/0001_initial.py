# Generated by Django 4.2.1 on 2023-06-01 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoolBeans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('something', models.CharField(default='cool stuff bro', max_length=255)),
            ],
        ),
    ]
