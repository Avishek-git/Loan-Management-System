# Generated by Django 4.2.6 on 2023-10-08 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registerPayment', '0003_payment_interest_due_payment_principal_due'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='Interest_due',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='Principal_due',
        ),
    ]
