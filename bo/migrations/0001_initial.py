# Generated by Django 4.0.1 on 2022-01-09 17:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aclicker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultat', models.CharField(max_length=50)),
                ('date_heure', models.DateTimeField(default=django.utils.timezone.now)),
                ('proxy', models.CharField(max_length=100)),
                ('timescrolling', models.IntegerField()),
                ('positition_page', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Requete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='SiteWeb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('requetes', models.ManyToManyField(blank=True, through='bo.Aclicker', to='bo.Requete')),
            ],
        ),
        migrations.AddField(
            model_name='aclicker',
            name='requete',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bo.requete'),
        ),
        migrations.AddField(
            model_name='aclicker',
            name='siteweb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bo.siteweb'),
        ),
    ]
