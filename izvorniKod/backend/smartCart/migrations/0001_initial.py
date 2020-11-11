# Generated by Django 3.1.2 on 2020-11-10 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import smartCart.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_kupac', models.BooleanField(default=False)),
                ('is_trgovac', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', smartCart.models.AccountManager()),
            ],
        ),
        migrations.CreateModel(
            name='Artikl',
            fields=[
                ('barkod_artikla', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('naziv_artikla', models.CharField(max_length=100)),
                ('autor_naziva', models.CharField(max_length=100, null=True)),
                ('vote_count_naziva', models.IntegerField(null=True)),
                ('opis_artikla', models.CharField(max_length=5000, null=True)),
                ('autor_opisa', models.CharField(max_length=100, null=True)),
                ('vote_count_opisa', models.IntegerField(null=True)),
                ('autor_proizvodaca', models.CharField(max_length=100, null=True)),
                ('vote_count_proizvodaca', models.IntegerField(null=True)),
                ('autor_zemlje_porijekla', models.CharField(max_length=100, null=True)),
                ('vote_count_zemlje_porijekla', models.IntegerField(null=True)),
                ('vegan', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Proizvodac',
            fields=[
                ('naziv', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='SecretCode',
            fields=[
                ('value', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Trgovina',
            fields=[
                ('sif_trgovina', models.AutoField(primary_key=True, serialize=False)),
                ('naz_trgovina', models.CharField(max_length=100)),
                ('adresa_trgovina', models.CharField(max_length=200)),
                ('radno_vrijeme_pocetak', models.TimeField()),
                ('radno_vrijeme_kraj', models.TimeField()),
                ('latitude', models.CharField(max_length=100, null=True)),
                ('longitude', models.CharField(max_length=100, null=True)),
                ('vlasnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Zemlja_porijekla',
            fields=[
                ('naziv', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='TrgovinaArtikli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cijena', models.DecimalField(decimal_places=2, max_digits=8)),
                ('akcija', models.BooleanField(default=False)),
                ('dostupan', models.BooleanField(default=False)),
                ('artikl', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartCart.artikl')),
                ('trgovina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartCart.trgovina')),
            ],
        ),
        migrations.AddField(
            model_name='artikl',
            name='proizvodac',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartCart.proizvodac'),
        ),
        migrations.AddField(
            model_name='artikl',
            name='zemlja_porijekla',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='smartCart.zemlja_porijekla'),
        ),
    ]
