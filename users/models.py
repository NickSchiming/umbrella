from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

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

    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

    # All these field declarations are copied as-is
    # from `AbstractUser`

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    class Types(models.TextChoices):
        REVENDEDOR = "REVENDEDOR", 'Revendedor'
        LOJA = "LOJA", 'Loja'
        SUPERVISOR = "SUPERVISOR", 'Supervisor'
        FRANQUIA = "FRANQUIA", 'Franquia'

    base_type = Types.REVENDEDOR

    type = models.CharField(
        _("type"), max_length=50, choices=Types.choices, default=base_type
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def save(self, *arg, **kwargs):
        if not self.pk:
            self.type = self.base_type
            return super().save(*arg, **kwargs)
