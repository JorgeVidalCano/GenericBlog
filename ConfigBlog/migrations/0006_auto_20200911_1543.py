# Generated by Django 3.0.5 on 2020-09-11 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConfigBlog', '0005_auto_20200911_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configblog',
            name='abouts',
            field=models.ManyToManyField(to='ConfigBlog.AboutFields'),
        ),
    ]
