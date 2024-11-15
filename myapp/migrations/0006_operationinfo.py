# Generated by Django 5.1.1 on 2024-10-18 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_delete_member_alter_memberinfo_member_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationInfo',
            fields=[
                ('operation_id', models.AutoField(primary_key=True, serialize=False)),
                ('operationtime', models.DateTimeField()),
                ('membername', models.CharField(max_length=100)),
                ('membertelphone', models.CharField(max_length=11)),
                ('operationitem', models.CharField(max_length=100)),
                ('operationrequest', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
