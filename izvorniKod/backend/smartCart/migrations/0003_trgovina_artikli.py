# Generated by Django 3.1.2 on 2020-10-31 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartCart', '0002_trgovina'),
    ]

    operations = [
        migrations.AddField(
            model_name='trgovina',
            name='artikli',
            field=models.ManyToManyField(to='smartCart.Artikl'),
        ),
    ]
