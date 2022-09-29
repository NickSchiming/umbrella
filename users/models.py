from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UsuarioManager(BaseUserManager):
    def create_superuser(self, email, password, telefone, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        usuario = self.create_user(
            email=self.normalize_email(email),
            password=password,
            telefone=telefone,
            **extra_fields
        )
        return usuario


class Usuario(AbstractUser):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        REVENDEDOR = "REVENDEDOR", 'Revendedor'
        LOJA = "LOJA", 'Loja'
        SUPERVISOR = "SUPERVISOR", 'Supervisor'
        FRANQUIA = "FRANQUIA", 'Franquia'

    base_type = Types.ADMIN

    type = models.CharField(
        _("type"), max_length=50, choices=Types.choices, default=base_type
    )

    username = None

    email = models.EmailField(_("email"),
                              max_length=100, unique=True)
    telefone = models.BigIntegerField()

    USERNAME_FIELD = 'email'

    def save(self, *arg, **kwargs):
        if not self.pk:
            self.type = self.base_type
            return super().save(*arg, **kwargs)


class RevendedorManager(BaseUserManager):

    def create_user(self, email, password, nome, cpf, telefone, endereco, datanasc, **extra_fields):

        if not email:
            raise ValueError("O email não pode ficar em branco")
        if not nome:
            raise ValueError("O nome não pode ficar em branco")
        if not cpf:
            raise ValueError("O cpf não pode ficar em branco")
        if not telefone:
            raise ValueError("O telefone não pode ficar em branco")
        if not endereco:
            raise ValueError("O endereço não pode ficar em branco")
        if not datanasc:
            raise ValueError("A data de nascimento não pode ficar em branco")

        usuario = self.model(
            email=self.normalize_email(email),
            password=password,
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            endereco=endereco,
            datanasc=datanasc,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

        def get_queryset(self, *args, **kwargs):

            results = super().get_queryset(*args, **kwargs)
            return results.filter(role=Usuario.Role.STUDENT)


class Revendedor(Usuario):

    base_type = Usuario.Types.REVENDEDOR

    nome = models.CharField("nome", max_length=150, blank=False)
    cpf = models.IntegerField()

    endereco = models.CharField(max_length=150)
    datanasc = models.DateField(auto_now=False, auto_now_add=False)
    REQUIRED_FIELDS = ['password',
                       'cpf', 'nome', 'telefone', 'endereco', 'datanasc']

    objects = RevendedorManager()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Revendedores"


class Supervisor(Usuario):

    base_type = Usuario.Types.SUPERVISOR

    nome = models.CharField("nome", max_length=150, blank=False)
    cpf = models.IntegerField(unique=True)
    REQUIRED_FIELDS = ['password',
                       'cpf', 'nome', 'telefone']

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Supervisores"


class Loja(Usuario):

    base_type = Usuario.Types.LOJA

    cnpj = models.IntegerField(unique=True)
    razaosocial = models.CharField("Razão social", max_length=150)
    endereco = models.CharField(max_length=150)
    REQUIRED_FIELDS = ['password',
                       'cpf', 'telefone', 'endereco', 'razaosocial']

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Lojas"


class FranquiaManager(BaseUserManager):

    def create_user(self, email, password, cnpj, telefone, endereco, razaosocial, **extra_fields):

        if not email:
            raise ValueError("O email não pode ficar em branco")
        if not cnpj:
            raise ValueError("O cnpj não pode ficar em branco")
        if not telefone:
            raise ValueError("O telefone não pode ficar em branco")
        if not endereco:
            raise ValueError("O endereço não pode ficar em branco")
        if not razaosocial:
            raise ValueError("A razão social não pode ficar em branco")

        usuario = self.model(
            email=self.normalize_email(email),
            password=password,
            cnpj=cnpj,
            telefone=telefone,
            endereco=endereco,
            razaosocial=razaosocial,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario


class Franquia(Usuario):

    base_type = Usuario.Types.FRANQUIA

    cnpj = models.IntegerField(unique=True)
    endereco = models.CharField(max_length=150)
    razaosocial = models.CharField("Razão social", max_length=150)
    REQUIRED_FIELDS = ['password',
                       'cpf', 'telefone', 'endereco']

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Supervisores"
