import datetime
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

# Definição das escolhas dos campos sexo
HOMEM = "homem"
MULHER = "mulher"
OUTRO = "outro"

opcoes_sexo = [
    (HOMEM, "Masculino"),
    (MULHER, "Feminino"),
    (OUTRO, "Outro"),
]


class Franquia(models.Model):
    # ligação com user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # campos de perfil
    cnpj = models.CharField(_("CNPJ"), max_length=15, unique=True, blank=True)
    nome = models.CharField(
        _("nome"), max_length=50, blank=True)
    nome_fantasia = models.CharField(
        _("nome fantasia"), max_length=50, blank=True)
    cep = models.CharField(
        _("CEP"), max_length=15, blank=True)
    uf = models.CharField(
        _("UF"), max_length=2, blank=True)
    cidade = models.CharField(
        _("cidade"), max_length=50, blank=True)
    bairro = models.CharField(
        _("bairro"), max_length=50, blank=True)
    logradouro = models.CharField(
        _("logradouro"), max_length=100, blank=True)
    numero = models.CharField(
        _("numero"), max_length=5, blank=True)
    telefone = models.CharField(
        _("telefone"), max_length=30, blank=True)
    is_aprovado = models.BooleanField(_('Aprovado'), default=False)

    def __str__(self):
        return self.nome_fantasia


class Supervisor(models.Model):
    # ligação com user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # campos de perfil
    nome = models.CharField(_("nome"), max_length=100, blank=True)
    cpf = models.CharField(_("CPF"), max_length=15, unique=True, blank=True)
    telefone = models.CharField(
        _("telefone"), max_length=30, blank=True)
    sexo = models.CharField(_("sexo"), choices=opcoes_sexo,
                            max_length=30, blank=True)
    datanasc = models.DateField(
        _("Data de nascimento"), auto_now=False, auto_now_add=False, blank=True)

    is_aprovado = models.BooleanField(_('Aprovado'), default=False)

    # ligação com franquia
    franquia = models.ForeignKey(
        Franquia, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome


class Meta(models.Model):
    # Definição das escolhas do campo nivel
    INICIANTE = "Iniciante"
    BRONZE = "Bronze"
    PRATA = "Prata"
    OURO = "Ouro"
    DIAMANTE = "Diamante"

    opcoes_nivel = [
        (INICIANTE, "iniciante"),
        (BRONZE, "bronze"),
        (PRATA, "prata"),
        (OURO, "ouro"),
        (DIAMANTE, "diamante"),
    ]

    nivel = models.CharField(choices=opcoes_nivel,
                             max_length=50)
    valor = models.FloatField(_("valor"))
    desconto = models.FloatField(_("desconto"))

    def __str__(self):
        return self.nivel

    # retorna desconto em decimal
    @property
    def descontocalc(self):
        return self.desconto / 100


class Revendedor(models.Model):
    # ligação com user
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)

    # campos de perfil
    nome = models.CharField(_("Nome"), max_length=100, blank=True)
    cpf = models.CharField(_("CPF"), max_length=15, blank=True)
    telefone = models.CharField(_("Telefone"), max_length=15, blank=True)
    cep = models.CharField(
        _("CEP"), max_length=15, blank=True)
    uf = models.CharField(
        _("UF"), max_length=2, blank=True)
    cidade = models.CharField(
        _("cidade"), max_length=50, blank=True)
    bairro = models.CharField(
        _("bairro"), max_length=50, blank=True)
    logradouro = models.CharField(
        _("logradouro"), max_length=100, blank=True)
    numero = models.CharField(
        _("numero"), max_length=5, blank=True)
    datanasc = models.DateField(
        _("Data de nascimento"), auto_now=False, auto_now_add=False, blank=True)
    sexo = models.CharField(_("sexo"), choices=opcoes_sexo,
                            max_length=30, blank=True)

    # ligação com supervisor
    supervisor = models.ForeignKey(Supervisor, verbose_name=_(
        "supervisor"), on_delete=models.SET_NULL, null=True, blank=True)

    def meta_iniciante():
        return Meta.objects.get(nivel=Meta.INICIANTE)

    # ligação com meta
    meta = models.ForeignKey(
        Meta, on_delete=models.SET_NULL, null=True, blank=True, default=meta_iniciante)

    # usado para ligação de revendedor com supervisor
    is_aprovado = models.BooleanField(_('Aprovado'), default=False)

    def __str__(self):
        return self.nome

    # retorna total comprado com desconto
    @property
    def total_comprado(self):
        pedidos = self.pedido_set.filter(completo=True)
        total = sum([pedido.get_meta_total for pedido in pedidos])
        return total

    @property
    def total_comprado_mes(self):
        now = datetime.datetime.now()
        pedidos = self.pedido_set.filter(completo=True, data__month=now.month)
        total = sum([pedido.get_meta_total for pedido in pedidos])
        return total

    # retorna a proxima meta do revendedor
    @property
    def get_proxima_meta(self):

        metas = Meta.objects.filter(
            valor__gt=self.meta.valor).order_by('valor')
        if not metas:
            metas = Meta.objects.get(nivel='Diamante')

        return metas[0]


class Loja(models.Model):
    # ligação com user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # campos de perfil
    cnpj = models.CharField(_("CNPJ"), max_length=15, unique=True, blank=True)
    nome = models.CharField(
        _("nome"), max_length=50, blank=True)
    nome_fantasia = models.CharField(
        _("nome fantasia"), max_length=50, blank=True)
    cep = models.CharField(
        _("CEP"), max_length=15, blank=True)
    uf = models.CharField(
        _("UF"), max_length=2, blank=True)
    cidade = models.CharField(
        _("cidade"), max_length=50, blank=True)
    bairro = models.CharField(
        _("bairro"), max_length=50, blank=True)
    logradouro = models.CharField(
        _("logradouro"), max_length=100, blank=True)
    numero = models.CharField(
        _("numero"), max_length=5, blank=True)
    telefone = models.CharField(
        _("telefone"), max_length=30, blank=True)
    is_aprovado = models.BooleanField(_('Aprovado'), default=False)

    # ligação com franquia
    franquia = models.ForeignKey(Franquia, verbose_name=_(
        "franquia"), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome_fantasia

    # retorna total comprado
    @property
    def total_comprado(self):
        pedidos = self.pedido_set.filter(completo=True)
        total = sum([pedido.get_meta_total for pedido in pedidos])
        return total


class Produto(models.Model):
    codigo = models.IntegerField(_("codigo do produto"), unique=True)
    descricao = models.CharField(_("descrição"), max_length=200)
    nome = models.CharField(_("nome do produto"),
                            max_length=100)
    qtde_estoque = models.PositiveIntegerField(
        _("quantidade em estoque"))
    preco = models.FloatField(_("preço do produto"))
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.codigo) + ' - ' + self.nome

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Pedido(models.Model):
    cod_pedido = models.CharField(
        _("código do pedido"), max_length=100, null=True)

    # lista de opções para status do pedido
    APROV_PEND = "aprovacao_pendente"
    APROVADO = "aprovado"
    ENVIADO = "enviado"
    FINALIZADO = "finalizado"

    opcoes_status = [
        (APROV_PEND, "Aprovação pendente"),
        (APROVADO, "Aprovado"),
        (ENVIADO, "Enviado"),
        (FINALIZADO, "Finalizado"),
    ]

    status = models.CharField(choices=opcoes_status,
                              max_length=50, null=True, blank=True, default=APROV_PEND)

    # usado para logica do carrinho
    completo = models.BooleanField(default=False)
    data = models.DateTimeField(
        _("data do pedido"), default=timezone.now, null=True, blank=True)
    subtotal = models.FloatField(
        _("valor pré-desconto do pedido"), null=True, blank=True)
    total = models.FloatField(
        _("valor total do pedido"), null=True, blank=True)

    # lista de opções para o metodo de pagamento
    CREDITO = "credito"
    DEBITO = "debito"
    PIX = "pix"
    BOLETO = "boleto"

    opcoes_pagamento = [
        (CREDITO, "Credito"),
        (DEBITO, "Debito"),
        (PIX, "Pix"),
        (BOLETO, "Boleto"),
    ]

    metodo_de_pagamento = models.CharField(
        choices=opcoes_pagamento, max_length=200, null=True, blank=True)

    # ligação com franquia
    franquia = models.ForeignKey(Franquia, verbose_name=_(
        "franquia"), on_delete=models.SET_NULL, null=True, blank=True)

    # ligação com loja
    loja = models.ForeignKey(Loja, verbose_name=_(
        "loja"), on_delete=models.SET_NULL, null=True, blank=True)

    # ligação com revendedor
    revendedor = models.ForeignKey(Revendedor, verbose_name=_(
        "revendedor"), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.cod_pedido != None:
            return self.cod_pedido
        elif self.revendedor == None:
            return str(self.loja) + ' - Temporário'
        else:
            return str(self.revendedor) + ' - Temporário'

    # retorna total do pedido com desconto
    @property
    def get_meta_total(self):
        subtotal = self.get_carrinho_total
        if self.revendedor:
            total = subtotal * (1 - (self.revendedor.meta.desconto / 100))
        else:
            total = subtotal
        return total

    # retorna total do pedido sem desconto
    @property
    def get_carrinho_total(self):
        itenspedido = self.itempedido_set.filter()
        total = sum([item.get_total for item in itenspedido])
        return total

    # retorna quantidade de itens do pedido
    @property
    def get_carrinho_itens(self):
        itenspedido = self.itempedido_set.all()
        total = sum([item.quantidade for item in itenspedido])
        return total

    # retorna se tem produto suficiente em estoque e qual produto falta
    def falta_estoque(self):
        itenspedido = self.itempedido_set.all()
        for item in itenspedido:
            if item.quantidade > item.produto.qtde_estoque:
                return [True, item.produto.nome]
            else:
                return [False, item.produto.nome]

    # remove do estoque os itens do pedido
    def baixa_estoque(self):
        itenspedido = self.itempedido_set.all()
        for item in itenspedido:
            item.produto.qtde_estoque -= item.quantidade
            item.produto.save()

    # retorna os itens do pedido para o estoque
    def devolve_produtos(self):
        itenspedido = self.itempedido_set.all()
        for item in itenspedido:
            item.produto.qtde_estoque += item.quantidade
            item.produto.save()


class ItemPedido(models.Model):

    # ligaçao com pedido
    pedido = models.ForeignKey(Pedido, verbose_name=_(
        "Pedido"), on_delete=models.CASCADE, null=True)

    # ligaçao com produto
    produto = models.ForeignKey(Produto, verbose_name=_(
        "produto"), on_delete=models.CASCADE, null=True)

    quantidade = models.IntegerField(
        _("quantidade"), default=0, null=True, blank=True)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pedido.cod_pedido + ' - ' + self.produto.nome

    # retorna preço total de cada produto
    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade
        return total
