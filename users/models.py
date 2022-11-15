from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
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

    criado = models.DateTimeField(
        _('criado'),
        default=timezone.now,
    )

    # lista de tipos para dar permissoes especiais

    REVENDEDOR = 'revendedor'
    LOJA = 'loja'
    SUPERVISOR = 'supervisor'
    FRANQUIA = 'franquia'

    opcoes_tipo = [
        (REVENDEDOR, "Revendedor"),
        (LOJA, "Loja"),
        (SUPERVISOR, "Supervisor"),
        (FRANQUIA, "Franquia"),
    ]

    # campo que armazena o tipo
    tipo = models.CharField(
        _("tipo"), max_length=50, choices=opcoes_tipo, default=REVENDEDOR, null = True, blank = True)

    # associação com o criado de objetos user
    objects = UserManager()

    # determina o campo usado como login
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
