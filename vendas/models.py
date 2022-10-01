from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User

class Supervisor(models.Model):
    # um perfil de Supervisor deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de Supervisor
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    # campos de perfil
    nome = models.CharField(_("nome"), max_length=100)
    cpf = models.IntegerField(_("cpf"), unique=True)
    
    def __str__(self):
        return self.nome
    
class Revendedor(models.Model):
    # um perfil de Revendedor deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de Revendedor
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    # campos de perfil
    nome = models.CharField(_("nome"), max_length=100)
    cpf = models.IntegerField(_("cpf"), unique=True)
    telefone = models.IntegerField(_("telefone"))
    endereco = models.CharField(_("endereço"), max_length=200)
    datanasc = models.DateField(
        _("data de nascimento"), auto_now=False, auto_now_add=False)
    
    # um revendedor é associado a um supervisor e um suppervisor à muitos revendedores
    # on_delete=SET_NULL pos ao deletar um supervisor o revendedor não é deletado, o camppo vira null
    supervisor = models.ForeignKey(Supervisor, verbose_name=_("supervisor"), on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nome
    


class Franquia(models.Model):
    # um perfil de franquia deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de franquia
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    # campos de perfil
    razaosocial = models.CharField(_("razão social"), max_length=150)
    cnpj = models.IntegerField(_("cnpj"), unique=True)
    endereco = models.CharField(_("endereço"), max_length=200)
    
    def __str__(self):
        return self.razaosocial


class Loja(models.Model):
    # um perfil de loja deve ser de apenas um usuario, e um usuario pode ter apenas um perfil de loja
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    # campos de perfil
    razaosocial = models.CharField(_("razão social"), max_length=150)
    cnpj = models.IntegerField(_("cnpj"), unique=True)
    endereco = models.CharField(_("endereço"), max_length=200)

    # uma loja é associada a uma franquia e uma franquia à muitos lojas
    # on_delete=SET_NULL pos ao deletar um supervisor o revendedor não é deletado, o camppo vira null
    franquia = models.ForeignKey(Franquia, verbose_name=_(
        "franquia"), on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.razaosocial
    
class Pedido(models.Model):
    
    cod_pedido = models.IntegerField(_("código do pedido"), unique=True, primary_key=True)
    
    # lista de opções para status do ppedido
    APROV_PEND = "aprovação_pendente"
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
    
    status = models.CharField(choices=opcoes_status, max_length=50)
    
    data = models.DateTimeField(_("data do pedido"), auto_now=True, auto_now_add=False)
    
    # estranho parece na vdd ser uma relação com objetos nota fiscal
    # nf = models.IntegerField(_("nota fiscal"))
    
    valor = models.FloatField(_("valor total do pedido"))
    
    # um pedido é associado a uma franquia e uma franquia à muitos pedidos
    # on_delete=SET_NULL pos ao deletar uma franquia o pedido não é deletado, o camppo vira null
    franquia = models.ForeignKey(Franquia, verbose_name=_("franquia"), on_delete=models.SET_NULL, null=True)
    
    # um pedido pode (blank=True) ser associado a uma loja e uma loja à muitos pedidos
    # on_delete=SET_NULL pos ao deletar uma loja o pedido não é deletado, o camppo vira null
    loja = models.ForeignKey(Loja, verbose_name=_("loja"), on_delete=models.SET_NULL, null=True, blank=True)
    
    # um pedido pode (blank=True) ser associado a um supervisor e um supervisor à muitos pedidos
    # on_delete=SET_NULL pos ao deletar um supervisor o pedido não é deletado, o camppo vira null
    supervisor = models.ForeignKey(Supervisor, verbose_name=_("supervisor"), on_delete=models.SET_NULL, null=True, blank=True)
    
    # um pedido pode (blank=True) ser associado a um revendedor e um revendedor à muitos pedidos
    # on_delete=SET_NULL pos ao deletar um revendedor o pedido não é deletado, o camppo vira null
    revendedor = models.ForeignKey(Revendedor, verbose_name=_("revendedor"), on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.cod_pedido
    
    
    
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
    
    nivel = models.CharField(choices=opcoes_nivel, max_length=50, primary_key=True)
    valor = models.FloatField(_("valor"))
    recompensa = models.CharField(_("recompensa"), max_length=150)
    
    Revendedor = models.ManyToManyField(Revendedor, verbose_name=_("revendedor"))
    
    def __str__(self):
        return self.nivel
    
class Produto(models.Model):
    codigo = models.IntegerField(_("codigo do pedido"), unique=True, primary_key=True)
    
    descricao = models.CharField(_("descrição"), max_length=200)
    nome = models.CharField(_("nome do produto"), max_length=100, unique=True)
    qtde_estoque = models.IntegerField(_("quantidade em estoque"))
    valor = models.FloatField(_("valor do produto"))
    
    def __str__(self):
        return self.nome

class item_pedido(models.Model):
    pedido = models.ForeignKey(Pedido, verbose_name=_("pedido"), on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, verbose_name=_("produto"), on_delete=models.CASCADE)
    
    quantidade = models.IntegerField(_("quantidade do produto"))
    
    
class Nota_fiscal(models.Model):
    nf = models.IntegerField(_("nota fiscal"), unique=True, primary_key=True)
    
    valor = models.FloatField(_("valor"))
    data_emissao = models.DateTimeField(_("data de emissão"), auto_now_add=True)
    inscricao_estadual = models.CharField(_("inscrição estadual"), max_length=200)
    razao_social = models.CharField(_("razão social"), max_length=150)
    cnpj = models.IntegerField(_("cnpj"))
    nome_fantasia = models.CharField(_("nome fantasia"), max_length=200)
    
    pedido = models.ForeignKey(Pedido, verbose_name=_("pedido"), on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nf

class item_nf(models.Model):
    nf = models.ForeignKey(Nota_fiscal, verbose_name=_("pedido"), on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, verbose_name=_("produto"), on_delete=models.CASCADE)
    
    quantidade = models.IntegerField(_("quantidade do produto"))
    qtde_faturada = models.IntegerField(_("quantidade faturada"))
