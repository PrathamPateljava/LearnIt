# Generated by Django 4.1.5 on 2023-04-12 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='resource',
            field=models.FileField(upload_to='uploads/{self.topic}'),
        ),
    ]
