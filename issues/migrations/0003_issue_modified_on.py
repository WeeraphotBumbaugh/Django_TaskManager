# Generated by Django 4.2.2 on 2023-06-11 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_auto_20230611_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='modified_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]