# Generated by Django 4.1.1 on 2022-10-24 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0002_alter_pedido_franquia'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item_pedido',
            old_name='Pedido',
            new_name='pedido',
        ),
    ]
