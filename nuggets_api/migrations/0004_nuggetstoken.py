# Generated by Django 2.1.7 on 2019-04-22 00:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nuggets_api', '0003_auto_20190408_0503'),
    ]

    operations = [
        migrations.CreateModel(
            name='NuggetsToken',
            fields=[
                ('key', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Key')),
                ('given_name', models.TextField(null=True)),
                ('family_name', models.TextField(null=True)),
                ('profile_url', models.TextField(null=True)),
                ('google_email', models.TextField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='nuggets_auth_token', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
                'abstract': False,
            },
        ),
    ]
