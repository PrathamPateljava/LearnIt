# Generated by Django 4.1.5 on 2023-03-19 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catergory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='cash',
            field=models.IntegerField(blank=True, default=10000, null=True),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=200)),
                ('imageurl', models.CharField(max_length=200)),
                ('price', models.IntegerField(max_length=20)),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.catergory')),
                ('watchlist', models.ManyToManyField(blank=True, null=True, related_name='watching', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
