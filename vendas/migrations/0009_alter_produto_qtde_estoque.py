# Generated by Django 4.1.2 on 2022-10-28 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0008_alter_franquia_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='qtde_estoque',
            field=models.PositiveIntegerField(null=True, verbose_name='quantidade em estoque'),
        ),
    ]
