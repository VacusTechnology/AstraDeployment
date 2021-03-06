# Generated by Django 3.1.5 on 2021-07-28 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_employeetag_floor'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistanceTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
                ('tag1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag1', to='employee.employeeregistration')),
                ('tag2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag2', to='employee.employeeregistration')),
            ],
        ),
    ]
