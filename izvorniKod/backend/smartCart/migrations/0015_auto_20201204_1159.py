# Generated by Django 3.1.2 on 2020-12-04 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartCart', '0014_auto_20201204_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='secretcode',
            name='uloga',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='smartCart.uloga'),
        ),
        migrations.AlterField(
            model_name='baseusermodel',
            name='uloga',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='smartCart.uloga'),
        ),
    ]
