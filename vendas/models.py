from email.policy import default
from django.db import DatabaseError, models
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Supervisor(models.Model):
    # um perfil de Supervisor deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de Supervisor
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # campos de perfil
    nome = models.CharField(_("nome"), max_length=100)
    cpf = models.IntegerField(_("cpf"), unique=True)

    def __str__(self):
        return self.nome


class Revendedor(models.Model):
    # um perfil de Revendedor deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de Revendedor
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='revendedor')

    # campos de perfil
    nome = models.CharField(_("Nome"), max_length=100, null=True)
    cpf = models.IntegerField(_("Cpf"), null=True)
    telefone = models.IntegerField(_("Telefone"), null=True)
    endereco = models.CharField(_("Endereço"), max_length=200, null=True)
    datanasc = models.DateField(
        _("Data de nascimento"), auto_now=False, auto_now_add=False, null=True)

    # um revendedor é associado a um supervisor e um suppervisor à muitos revendedores
    # on_delete=SET_NULL pos ao deletar um supervisor o revendedor não é deletado, o camppo vira null
    supervisor = models.ForeignKey(Supervisor, verbose_name=_(
        "supervisor"), on_delete=models.SET_NULL, null=True)

    is_aprovado = models.BooleanField(_('Aprovado'), default=False)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Revendedor"
        verbose_name_plural = "Revendedores"

    def __str__(self):
        return self.nome


class Franquia(models.Model):
    # um perfil de franquia deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de franquia
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # campos de perfil
    razaosocial = models.CharField(_("razão social"), max_length=150)
    cnpj = models.IntegerField(_("cnpj"), unique=True)
    endereco = models.CharField(_("endereço"), max_length=200)

    # def __str__(self):
    #     return self.razaosocial


class Loja(models.Model):
    # um perfil de loja deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de loja
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # campos de perfil
    razaosocial = models.CharField(_("razão social"), max_length=150)
    cnpj = models.IntegerField(_("cnpj"), unique=True)
    endereco = models.CharField(_("endereço"), max_length=200)

    # uma loja é associada a uma franquia e uma franquia à muitos lojas
    # on_delete=SET_NULL pos ao deletar um supervisor o revendedor não é deletado, o camppo vira null
    franquia = models.ForeignKey(Franquia, verbose_name=_(
        "franquia"), on_delete=models.SET_NULL, null=True)

    # def __str__(self):
    #     return self.razaosocial


class Produto(models.Model):
    codigo = models.IntegerField(
        _("codigo do produto"), unique=True)

    descricao = models.CharField(_("descrição"), max_length=200, null=True)
    nome = models.CharField(_("nome do produto"),
                            max_length=100, unique=True, null=True)
    qtde_estoque = models.IntegerField(_("quantidade em estoque"), null=True)
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
    RECUSADO = "recusado"
    ENVIADO = "enviado"
    FINALIZADO = "finalizado"

    opcoes_status = [
        (APROV_PEND, "Aprovação pendente"),
        (APROVADO, "Aprovado"),
        (RECUSADO, "Recusado"),
        (ENVIADO, "Enviado"),
        (FINALIZADO, "Finalizado"),
    ]

    status = models.CharField(choices=opcoes_status,
                              max_length=50, null=True, blank=True)
    
    completo = models.BooleanField(default=False)

    data = models.DateTimeField(
        _("data do pedido"), auto_now_add=True, null=True, blank=True)

    # estranho parece na vdd ser uma relação com objetos nota fiscal
    # nf = models.IntegerField(_("nota fiscal"))

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

    # um pedido pode (blank=True) ser associado a um supervisor e um supervisor à muitos pedidos
    # on_delete=SET_NULL pos ao deletar um supervisor o pedido não é deletado, o camppo vira null
    supervisor = models.ForeignKey(Supervisor, verbose_name=_(
        "supervisor"), on_delete=models.SET_NULL, null=True, blank=True)

    # um pedido pode (blank=True) ser associado a um revendedor e um revendedor à muitos pedidos
    # on_delete=SET_NULL pos ao deletar um revendedor o pedido não é deletado, o camppo vira null
    revendedor = models.ForeignKey(Revendedor, verbose_name=_(
        "revendedor"), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.cod_pedido

    @property
    def get_carrinho_total(self):
        itenspedido = self.itempedido_set.all()
        total = sum([item.get_total for item in itenspedido])
        return total

    @property
    def get_carrinho_itens(self):
        itenspedido = self.itempedido_set.all()
        total = sum([item.quantidade for item in itenspedido])
        return total

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = self.APROV_PEND

        # if Item_pedido.objects.get(pedido=self):
        #     Pedido.calcula_total(self)
        return super().save(*args, **kwargs)


class ItemPedido(models.Model):

    pedido = models.ForeignKey(Pedido, verbose_name=_(
        "Pedido"), on_delete=models.SET_NULL, null=True)
    
    produto = models.ForeignKey(Produto, verbose_name=_(
        "produto"), on_delete=models.SET_NULL, null=True)

    quantidade = models.IntegerField(
        _("quantidade"), default=0, null=True, blank=True)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if self.produto.qtde_estoque < self.quantidade:
    #         DatabaseError('Quantidade em estoque insuficiente')
    #     else:
    #         self.subtotal = self.quantidade * self.produto.valor
    #         self.produto.qtde_estoque -= self.quantidade
    #     super().save(*args, **kwargs)
    
    def __str__(self):
        return self.produto.nome

    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade
        return total


class Meta(models.Model):

    BRONZE = "bronze"
    PRATA = "prata"
    OURO = "ouro"
    DIAMANTE = "diamante"

    opcoes_nivel = [
        (BRONZE, "Bronzee"),
        (PRATA, "Prata"),
        (OURO, "Ouro"),
        (DIAMANTE, "Diamante"),
    ]

    nivel = models.CharField(choices=opcoes_nivel,
                             max_length=50)
    valor = models.FloatField(_("valor"))
    recompensa = models.CharField(_("recompensa"), max_length=150)

    Revendedor = models.ManyToManyField(
        Revendedor, verbose_name=_("revendedor"))

    def __str__(self):
        return self.nivel


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
