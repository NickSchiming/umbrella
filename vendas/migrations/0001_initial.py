# Generated by Django 4.1.1 on 2022-09-30 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Franquia',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('razaosocial', models.CharField(max_length=150, verbose_name='razão social')),
                ('cnpj', models.IntegerField(unique=True, verbose_name='cnpj')),
                ('endereco', models.CharField(max_length=200, verbose_name='endereço')),
            ],
        ),
        migrations.CreateModel(
            name='Loja',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('razaosocial', models.CharField(max_length=150, verbose_name='razão social')),
                ('cnpj', models.IntegerField(unique=True, verbose_name='cnpj')),
                ('endereco', models.CharField(max_length=200, verbose_name='endereço')),
                ('franquia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.franquia', verbose_name='franquia')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='codigo do pedido')),
                ('descricao', models.CharField(max_length=200, verbose_name='descrição')),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='nome do produto')),
                ('qtde_estoque', models.IntegerField(verbose_name='quantidade em estoque')),
                ('valor', models.FloatField(verbose_name='valor do produto')),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nome', models.CharField(max_length=100, verbose_name='nome')),
                ('cpf', models.IntegerField(unique=True, verbose_name='cpf')),
            ],
        ),
        migrations.CreateModel(
            name='Revendedor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nome', models.CharField(max_length=100, verbose_name='nome')),
                ('cpf', models.IntegerField(unique=True, verbose_name='cpf')),
                ('telefone', models.IntegerField(verbose_name='telefone')),
                ('endereco', models.CharField(max_length=200, verbose_name='endereço')),
                ('datanasc', models.DateField(verbose_name='data de nascimento')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.supervisor', verbose_name='supervisor')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('cod_pedido', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='código do pedido')),
                ('status', models.CharField(choices=[('aprovação_pendente', 'Aprovação pendente'), ('aprovado', 'Aprovado'), ('recusado', 'Recusado'), ('enviado', 'Enviado'), ('finalizado', 'Finalizado')], max_length=50)),
                ('data', models.DateTimeField(auto_now=True, verbose_name='data do pedido')),
                ('valor', models.FloatField(verbose_name='valor total do pedido')),
                ('franquia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.franquia', verbose_name='franquia')),
                ('loja', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.loja', verbose_name='loja')),
                ('revendedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.revendedor', verbose_name='revendedor')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.supervisor', verbose_name='supervisor')),
            ],
        ),
        migrations.CreateModel(
            name='Nota_fiscal',
            fields=[
                ('nf', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='nota fiscal')),
                ('valor', models.FloatField(verbose_name='valor')),
                ('data_emissao', models.DateTimeField(auto_now_add=True, verbose_name='data de emissão')),
                ('inscricao_estadual', models.CharField(max_length=200, verbose_name='inscrição estadual')),
                ('razao_social', models.CharField(max_length=150, verbose_name='razão social')),
                ('cnpj', models.IntegerField(verbose_name='cnpj')),
                ('nome_fantasia', models.CharField(max_length=200, verbose_name='nome fantasia')),
                ('pedido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.pedido', verbose_name='pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('nivel', models.CharField(choices=[('bronze', 'Bronzee'), ('prata', 'Prata'), ('ouro', 'Ouro'), ('diamante', 'Diamante')], max_length=50, primary_key=True, serialize=False)),
                ('valor', models.FloatField(verbose_name='valor')),
                ('recompensa', models.CharField(max_length=150, verbose_name='recompensa')),
                ('Revendedor', models.ManyToManyField(to='vendas.revendedor', verbose_name='revendedor')),
            ],
        ),
        migrations.CreateModel(
            name='item_pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(verbose_name='quantidade do produto')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendas.pedido', verbose_name='pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendas.produto', verbose_name='produto')),
            ],
        ),
        migrations.CreateModel(
            name='item_nf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(verbose_name='quantidade do produto')),
                ('qtde_faturada', models.IntegerField(verbose_name='quantidade faturada')),
                ('nf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendas.nota_fiscal', verbose_name='pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendas.produto', verbose_name='produto')),
            ],
        ),
    ]