# Generated by Django 4.0.4 on 2022-09-07 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('housewars', '0006_facilitator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facilitator',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='housewars.activity'),
        ),
    ]
