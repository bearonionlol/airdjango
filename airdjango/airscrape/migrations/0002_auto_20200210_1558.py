# Generated by Django 3.0.2 on 2020-02-10 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airscrape', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upc', models.CharField(max_length=128, unique=True)),
                ('name', models.CharField(default='', max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('url', models.URLField(max_length=512, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='price',
            old_name='cheapest_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='price',
            name='stores_and_prices',
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='airscrape.Product'),
        ),
        migrations.AddField(
            model_name='price',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='airscrape.Store'),
        ),
    ]
