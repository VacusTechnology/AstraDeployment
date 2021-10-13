# Generated by Django 3.1.5 on 2021-08-06 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zones', '0002_zonetracking'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyZoneTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('timestamp', models.DateTimeField(null=True)),
                ('zoneid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zones.zones')),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyZoneTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagid', models.IntegerField()),
                ('timestamp', models.DateTimeField(null=True)),
                ('zoneid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zones.zones')),
            ],
        ),
    ]