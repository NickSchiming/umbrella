from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    # n sei o que é
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('O email não pode ficar em branco')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # define um create user para não usar username que sera usado no formulario
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    # define um create superuser para não usar username
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    # campo extra customizado
    email = models.EmailField(_('email'), unique=True)

    # campos do AbstractUser que serão utilizados

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
    )

    """criado = models.DateTimeField(
        _('criado'),
        default=timezone.now,
    )
    
    atualizado = models.DateTimeField(
        _('atualizado'),
        default=timezone.now,
    ) """

    # lista de tipos para dar permissoes especiais
    class Types(models.TextChoices):
        REVENDEDOR = "REVENDEDOR", 'Revendedor'
        LOJA = "LOJA", 'Loja'
        SUPERVISOR = "SUPERVISOR", 'Supervisor'
        FRANQUIA = "FRANQUIA", 'Franquia'

    # tipo padrão sempre que um user é criado
    base_type = Types.REVENDEDOR

    # campo que armazena o tipo
    type = models.CharField(
        _("type"), max_length=50, choices=Types.choices, default=base_type
    )

    # associação com o criado de objetos user
    objects = UserManager()

    # determina o campo usado como login
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"

    def __str__(self):
        return self.email

    # override no save para colocar o tipo padrão na cração do objeto
    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = self.base_type
            
        return super().save(*args, **kwargs)

