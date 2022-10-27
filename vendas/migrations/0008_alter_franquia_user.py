# Generated by Django 4.1.2 on 2022-10-27 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendas', '0007_remove_meta_revendedor_revendedor_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='franquia',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='franquia', to=settings.AUTH_USER_MODEL),
        ),
    ]
