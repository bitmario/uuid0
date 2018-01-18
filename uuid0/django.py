import uuid
from django.forms import fields
from django.db import models
import django.core.exceptions as exceptions
from django.utils.translation import ugettext_lazy as _

from .core import UUID, generate


class UUID0FormField(fields.CharField):
    default_error_messages = {
        'invalid': _('Enter a valid UUID.'),
    }

    def prepare_value(self, value):
        if isinstance(value, UUID):
            return value.base62
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        if not isinstance(value, UUID):
            if isinstance(value, uuid.UUID):
                value = UUID(int=value.int)
            else:
                try:
                    value = UUID(base62=value)
                except ValueError:
                    raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value


class UUID0Field(models.UUIDField):
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return UUID(int=value.int)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if not isinstance(value, UUID):
            value = self.to_python(value)

        if connection.features.has_native_uuid_field:
            return value
        return value.hex

    def to_python(self, value):
        if value is not None and not isinstance(value, UUID):
            if isinstance(value, uuid.UUID):
                return UUID(int=value.int)
            else:
                try:
                    return UUID(value)
                except (AttributeError, ValueError):
                    raise exceptions.ValidationError(
                        self.error_messages['invalid'],
                        code='invalid',
                        params={'value': value},
                    )
        return value

    def formfield(self, **kwargs):
        defaults = {
            'form_class': UUID0FormField,
        }
        defaults.update(kwargs)
        return super().formfield(**kwargs)


class UUID0Model(models.Model):
    uuid = UUID0Field(_('UUID'), default=generate, unique=True, editable=False)

    @property
    def uuid_base62(self):
        return self.uuid.base62

    @property
    def uuid_datetime(self):
        return self.uuid.datetime

    def __str__(self):
        return self.uuid_base62

    class Meta:
        abstract = True


class UUID0PKModel(UUID0Model):
    uuid = UUID0Field(_('UUID'), default=generate, primary_key=True, editable=False)

    class Meta:
        abstract = True
