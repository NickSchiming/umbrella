from django.utils import timezone
from email.policy import default
from django.db import DatabaseError, models
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Franquia(models.Model):
    # um perfil de franquia deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de franquia
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # campos de perfil
    razaosocial = models.CharField(
        _("razão social"), max_length=150, blank=True)
    cnpj = models.IntegerField(_("cnpj"), unique=True, blank=True)
    endereco = models.CharField(_("endereço"), max_length=200, blank=True)

    def __str__(self):
        return self.razaosocial


class Supervisor(models.Model):
    # um perfil de Supervisor deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de Supervisor
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # campos de perfil
    nome = models.CharField(_("nome"), max_length=100, blank=True)
    cpf = models.IntegerField(_("cpf"), unique=True, blank=True)

    franquia = models.ForeignKey(
        Franquia, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome


class Meta(models.Model):

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

    @property
    def descontocalc(self):
        return self.desconto / 100


class Revendedor(models.Model):
    # um perfil de Revendedor deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de Revendedor
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)

    # campos de perfil
    nome = models.CharField(_("Nome"), max_length=100, blank=True)
    cpf = models.IntegerField(_("Cpf"), blank=True)
    telefone = models.CharField(_("Telefone"), max_length=15, blank=True)
    cep = models.CharField(_("CEP"), max_length=15, blank=True)
    endereco = models.CharField(_("Endereço"), max_length=200, blank=True)
    datanasc = models.DateField(
        _("Data de nascimento"), auto_now=False, auto_now_add=False, blank=True)

    # um revendedor é associado a um supervisor e um suppervisor à muitos revendedores
    # on_delete=SET_NULL pos ao deletar um supervisor o revendedor não é deletado, o camppo vira null
    supervisor = models.ForeignKey(Supervisor, verbose_name=_(
        "supervisor"), on_delete=models.SET_NULL, null=True, blank=True)

    """ data_ingressao = models.DateTimeField(
        _("Data de ingressão"), auto_now_add=True, blank=True) """

    meta = models.ForeignKey(
        Meta, on_delete=models.SET_NULL, null=True, blank=True)

    is_aprovado = models.BooleanField(_('Aprovado'), default=False)

    class Meta:
        verbose_name = "Revendedor"
        verbose_name_plural = "Revendedores"

    def __str__(self):
        return self.nome

    @property
    def total_comprado(self):
        pedidos = self.pedido_set.filter(completo=True)
        total = sum([pedido.get_meta_total for pedido in pedidos])
        return total

    @property
    def get_proxima_meta(self):

        metas = Meta.objects.filter(
            valor__gt=self.meta.valor).order_by('valor')
        if not metas:
            metas = Meta.objects.get(nivel='Diamante')

        return metas[0]


class Loja(models.Model):
    # um perfil de loja deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de loja
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # campos de perfil
    razaosocial = models.CharField(
        _("razão social"), max_length=150, blank=True)
    cnpj = models.IntegerField(_("cnpj"), unique=True, blank=True)
    endereco = models.CharField(_("endereço"), max_length=200, blank=True)

    # uma loja é associada a uma franquia e uma franquia à muitos lojas
    # on_delete=SET_NULL pos ao deletar um supervisor o revendedor não é deletado, o camppo vira null
    franquia = models.ForeignKey(Franquia, verbose_name=_(
        "franquia"), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.razaosocial

    @property
    def total_comprado(self):
        pedidos = self.pedido_set.filter(completo=True)
        total = sum([pedido.get_meta_total for pedido in pedidos])
        return total


class Produto(models.Model):
    codigo = models.IntegerField(
        _("codigo do produto"), unique=True)

    descricao = models.CharField(_("descrição"), max_length=200, null=True)
    nome = models.CharField(_("nome do produto"),
                            max_length=100, unique=True, null=True)
    qtde_estoque = models.PositiveIntegerField(
        _("quantidade em estoque"), null=True)
    preco = models.FloatField(_("preço do produto"), null=True)
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

    # lista de opções para status do ppedido
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
                              max_length=50, null=True, blank=True)

    completo = models.BooleanField(default=False)

    data = models.DateTimeField(
        _("data do pedido"), default=timezone.now, null=True, blank=True)

    # estranho parece na vdd ser uma relação com objetos nota fiscal
    # nf = models.IntegerField(_("nota fiscal"))

    subtotal = models.FloatField(
        _("valor pré-desconto do pedido"), null=True, blank=True)

    total = models.FloatField(
        _("valor total do pedido"), null=True, blank=True)

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

    # um pedido é associado a uma franquia e uma franquia à muitos pedidos
    # on_delete=SET_NULL pos ao deletar uma franquia o pedido não é deletado, o camppo vira null
    franquia = models.ForeignKey(Franquia, verbose_name=_(
        "franquia"), on_delete=models.SET_NULL, null=True, blank=True)

    # um pedido pode (blank=True) ser associado a uma loja e uma loja à muitos pedidos
    # on_delete=SET_NULL pos ao deletar uma loja o pedido não é deletado, o camppo vira null
    loja = models.ForeignKey(Loja, verbose_name=_(
        "loja"), on_delete=models.SET_NULL, null=True, blank=True)

    # um pedido pode (blank=True) ser associado a um revendedor e um revendedor à muitos pedidos
    # on_delete=SET_NULL pos ao deletar um revendedor o pedido não é deletado, o camppo vira null
    revendedor = models.ForeignKey(Revendedor, verbose_name=_(
        "revendedor"), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.cod_pedido != None:
            return self.cod_pedido
        elif self.revendedor == None:
            return str(self.loja) + ' - Temporário'
        else:
            return str(self.revendedor) + ' - Temporário'

    @property
    def get_meta_total(self):
        subtotal = self.get_carrinho_total
        if self.revendedor:
            total = subtotal * (1 - (self.revendedor.meta.desconto / 100))
        else:
            total = subtotal
        return total

    @property
    def get_carrinho_total(self):
        itenspedido = self.itempedido_set.filter()
        total = sum([item.get_total for item in itenspedido])
        return total

    @property
    def get_carrinho_itens(self):
        itenspedido = self.itempedido_set.all()
        total = sum([item.quantidade for item in itenspedido])
        return total

    def falta_estoque(self):
        itenspedido = self.itempedido_set.all()
        for item in itenspedido:
            if item.quantidade > item.produto.qtde_estoque:
                return [True, item.produto.nome]
            else:
                return [False, item.produto.nome]

    def baixa_estoque(self):
        itenspedido = self.itempedido_set.all()
        for item in itenspedido:
            item.produto.qtde_estoque -= item.quantidade
            item.produto.save()

    def devolve_produtos(self):
        itenspedido = self.itempedido_set.all()
        for item in itenspedido:
            item.produto.qtde_estoque += item.quantidade
            item.produto.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = self.APROV_PEND

        return super().save(*args, **kwargs)


class ItemPedido(models.Model):

    pedido = models.ForeignKey(Pedido, verbose_name=_(
        "Pedido"), on_delete=models.CASCADE, null=True)

    produto = models.ForeignKey(Produto, verbose_name=_(
        "produto"), on_delete=models.CASCADE, null=True)

    quantidade = models.IntegerField(
        _("quantidade"), default=0, null=True, blank=True)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pedido.cod_pedido + ' - ' + self.produto.nome

    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade
        return total


class Nota_fiscal(models.Model):
    nf = models.IntegerField(_("nota fiscal"), unique=True)

    valor = models.FloatField(_("valor"))
    data_emissao = models.DateTimeField(
        _("data de emissão"), auto_now_add=True)
    inscricao_estadual = models.CharField(
        _("inscrição estadual"), max_length=200)
    razao_social = models.CharField(_("razão social"), max_length=150)
    cnpj = models.IntegerField(_("cnpj"))
    nome_fantasia = models.CharField(_("nome fantasia"), max_length=200)

    pedido = models.ForeignKey(Pedido, verbose_name=_(
        "pedido"), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nf


class item_nf(models.Model):
    nf = models.ForeignKey(Nota_fiscal, verbose_name=_(
        "pedido"), on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, verbose_name=_(
        "produto"), on_delete=models.CASCADE)

    quantidade = models.IntegerField(_("quantidade do produto"))
    qtde_faturada = models.IntegerField(_("quantidade faturada"))
