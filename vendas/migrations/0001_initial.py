# Generated by Django 4.1.1 on 2022-11-18 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import vendas.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Franquia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(blank=True, max_length=15, unique=True, verbose_name='cnpj')),
                ('nome', models.CharField(blank=True, max_length=50, verbose_name='nome')),
                ('nome_fantasia', models.CharField(blank=True, max_length=50, verbose_name='nome fantasia')),
                ('cep', models.CharField(blank=True, max_length=15, verbose_name='CEP')),
                ('uf', models.CharField(blank=True, max_length=2, verbose_name='UF')),
                ('cidade', models.CharField(blank=True, max_length=50, verbose_name='cidade')),
                ('bairro', models.CharField(blank=True, max_length=50, verbose_name='bairro')),
                ('logradouro', models.CharField(blank=True, max_length=100, verbose_name='logradouro')),
                ('numero', models.CharField(blank=True, max_length=5, verbose_name='numero')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='telefone')),
                ('is_aprovado', models.BooleanField(default=False, verbose_name='Aprovado')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Loja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(blank=True, max_length=15, unique=True, verbose_name='cnpj')),
                ('nome', models.CharField(blank=True, max_length=50, verbose_name='nome')),
                ('nome_fantasia', models.CharField(blank=True, max_length=50, verbose_name='nome fantasia')),
                ('cep', models.CharField(blank=True, max_length=15, verbose_name='CEP')),
                ('uf', models.CharField(blank=True, max_length=2, verbose_name='UF')),
                ('cidade', models.CharField(blank=True, max_length=50, verbose_name='cidade')),
                ('bairro', models.CharField(blank=True, max_length=50, verbose_name='bairro')),
                ('logradouro', models.CharField(blank=True, max_length=100, verbose_name='logradouro')),
                ('numero', models.CharField(blank=True, max_length=5, verbose_name='numero')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='telefone')),
                ('is_aprovado', models.BooleanField(default=False, verbose_name='Aprovado')),
                ('franquia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.franquia', verbose_name='franquia')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.CharField(choices=[('Iniciante', 'iniciante'), ('Bronze', 'bronze'), ('Prata', 'prata'), ('Ouro', 'ouro'), ('Diamante', 'diamante')], max_length=50)),
                ('valor', models.FloatField(verbose_name='valor')),
                ('desconto', models.FloatField(verbose_name='desconto')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(unique=True, verbose_name='codigo do produto')),
                ('descricao', models.CharField(max_length=200, verbose_name='descrição')),
                ('nome', models.CharField(max_length=100, verbose_name='nome do produto')),
                ('qtde_estoque', models.PositiveIntegerField(verbose_name='quantidade em estoque')),
                ('preco', models.FloatField(verbose_name='preço do produto')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=100, verbose_name='nome')),
                ('cpf', models.CharField(blank=True, max_length=15, unique=True, verbose_name='cpf')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='telefone')),
                ('sexo', models.CharField(blank=True, choices=[('homem', 'Homem'), ('mulher', 'Mulher'), ('outro', 'Outro')], max_length=30, verbose_name='sexo')),
                ('datanasc', models.DateField(blank=True, verbose_name='Data de nascimento')),
                ('is_aprovado', models.BooleanField(default=False, verbose_name='Aprovado')),
                ('franquia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.franquia')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Revendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=100, verbose_name='Nome')),
                ('cpf', models.CharField(blank=True, max_length=15, verbose_name='Cpf')),
                ('telefone', models.CharField(blank=True, max_length=15, verbose_name='Telefone')),
                ('cep', models.CharField(blank=True, max_length=15, verbose_name='CEP')),
                ('uf', models.CharField(blank=True, max_length=2, verbose_name='UF')),
                ('cidade', models.CharField(blank=True, max_length=50, verbose_name='cidade')),
                ('bairro', models.CharField(blank=True, max_length=50, verbose_name='bairro')),
                ('logradouro', models.CharField(blank=True, max_length=100, verbose_name='logradouro')),
                ('numero', models.CharField(blank=True, max_length=5, verbose_name='numero')),
                ('datanasc', models.DateField(blank=True, verbose_name='Data de nascimento')),
                ('sexo', models.CharField(blank=True, choices=[('homem', 'Homem'), ('mulher', 'Mulher'), ('outro', 'Outro')], max_length=30, verbose_name='sexo')),
                ('is_aprovado', models.BooleanField(default=False, verbose_name='Aprovado')),
                ('meta', models.ForeignKey(blank=True, default=vendas.models.Revendedor.meta_iniciante, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.meta')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.supervisor', verbose_name='supervisor')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_pedido', models.CharField(max_length=100, null=True, verbose_name='código do pedido')),
                ('status', models.CharField(blank=True, choices=[('aprovacao_pendente', 'Aprovação pendente'), ('aprovado', 'Aprovado'), ('enviado', 'Enviado'), ('finalizado', 'Finalizado')], default='aprovacao_pendente', max_length=50, null=True)),
                ('completo', models.BooleanField(default=False)),
                ('data', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='data do pedido')),
                ('subtotal', models.FloatField(blank=True, null=True, verbose_name='valor pré-desconto do pedido')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='valor total do pedido')),
                ('metodo_de_pagamento', models.CharField(blank=True, choices=[('credito', 'Credito'), ('debito', 'Debito'), ('pix', 'Pix'), ('boleto', 'Boleto')], max_length=200, null=True)),
                ('franquia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.franquia', verbose_name='franquia')),
                ('loja', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.loja', verbose_name='loja')),
                ('revendedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendas.revendedor', verbose_name='revendedor')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(blank=True, default=0, null=True, verbose_name='quantidade')),
                ('data_adicionado', models.DateTimeField(auto_now_add=True)),
                ('pedido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendas.pedido', verbose_name='Pedido')),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendas.produto', verbose_name='produto')),
            ],
        ),
    ]
