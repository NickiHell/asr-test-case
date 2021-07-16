# Generated by Django 3.2.5 on 2021-07-16 04:36

from django.db import migrations
from faker import Faker

faker = Faker()


def create_users_forward(apps, _):
    User = apps.get_model('users', 'User')
    new_users = [
        User(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            timezone=faker.date_time_this_month(),
        )
    ]
    User.objects.bulk_create(new_users)


def create_users_backward(apps, _):
    User = apps.get_model('users', 'User')
    User.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_users_forward, create_users_backward),
    ]
