# Generated by Django 3.1 on 2022-08-06 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('surname', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scan_file', models.ImageField(blank=True, null=True, upload_to='passport/')),
                ('document_number', models.CharField(blank=True, max_length=250, null=True)),
                ('first_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('patronymic', models.CharField(blank=True, max_length=250, null=True)),
                ('nationality', models.CharField(blank=True, max_length=250, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('personal_number', models.CharField(blank=True, max_length=250, null=True)),
                ('gender', models.CharField(blank=True, max_length=250, null=True)),
                ('issue_date', models.DateField(blank=True, null=True)),
                ('expire_date', models.DateField(blank=True, null=True)),
                ('issuing_authority', models.CharField(blank=True, max_length=250, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
    ]
