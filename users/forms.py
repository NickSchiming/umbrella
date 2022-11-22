from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from . import models
from vendas import models


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:4]

    class Meta:
        model = models.User
        fields = ['email','tipo' ]
