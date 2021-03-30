# Generated by Django 3.1.7 on 2021-03-30 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, null=True)),
            ],
            options={
                'db_table': 'book_status',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('number_of_guests', models.PositiveIntegerField()),
                ('message', models.CharField(max_length=45, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('serial_number', models.CharField(max_length=45)),
                ('book_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='book.bookstatus')),
            ],
            options={
                'db_table': 'books',
            },
        ),
    ]