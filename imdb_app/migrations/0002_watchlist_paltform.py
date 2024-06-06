# Generated by Django 5.0.3 on 2024-03-09 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='paltform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='imdb_app.streamplatform'),
            preserve_default=False,
        ),
    ]
