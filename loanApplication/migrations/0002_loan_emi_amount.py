# Generated by Django 4.2.6 on 2023-10-08 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApplication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='emi_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
