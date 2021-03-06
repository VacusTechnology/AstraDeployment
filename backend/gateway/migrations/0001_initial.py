# Generated by Django 3.1.5 on 2021-03-30 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterGateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('macaddress', models.CharField(max_length=20, unique=True)),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.map')),
            ],
        ),
        migrations.CreateModel(
            name='SlaveGateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('macaddress', models.CharField(max_length=20, unique=True)),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gateway.mastergateway')),
            ],
        ),
    ]
