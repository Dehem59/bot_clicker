# Generated by Django 4.0.1 on 2022-01-15 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bo', '0002_keyword_proxy_useragent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proxy',
            old_name='Proxy Host',
            new_name='host',
        ),
    ]
