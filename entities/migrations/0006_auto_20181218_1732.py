# Generated by Django 2.1.3 on 2018-12-18 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_heroacquaintance_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='headshot',
            field=models.ImageField(blank=True, null=True, upload_to='hero_headshots/'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='father',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='entities.Hero'),
        ),
    ]
