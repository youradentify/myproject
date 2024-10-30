# Generated by Django 5.1.1 on 2024-10-10 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberInfo',
            fields=[
                ('member_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('membername', models.CharField(max_length=100)),
                ('membertelphone', models.CharField(max_length=11)),
                ('memberpurchasecount', models.CharField(max_length=3)),
                ('memberremaincount', models.CharField(max_length=3)),
            ],
            options={
                'unique_together': {('membername', 'membertelphone')},
            },
        ),
    ]
