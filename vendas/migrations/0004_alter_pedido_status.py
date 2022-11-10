# Generated by Django 4.1.1 on 2022-11-10 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0003_alter_pedido_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(blank=True, choices=[('Aprovação pendente', 'aprovacao_pendente'), ('aprovado', 'Aprovado'), ('enviado', 'Enviado'), ('finalizado', 'Finalizado')], max_length=50, null=True),
        ),
    ]
