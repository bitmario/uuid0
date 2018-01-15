import uuid

import django.db.models as models
import django.db.models.fields as fields
from django.utils.translation import ugettext_lazy as _

import uuid0
from uuid0.django import forms


class UUID0Field(fields.UUIDField):
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return uuid0.UUID(int=value.int)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if not isinstance(value, uuid0.UUID):
            value = self.to_python(value)

        if connection.features.has_native_uuid_field:
            return value
        return value.hex

    def to_python(self, value):
        if value is not None and not isinstance(value, uuid0.UUID):
            if isinstance(value, uuid.UUID):
                return uuid0.UUID(int=value.int)
            else:
                try:
                    return uuid0.UUID(value)
                except (AttributeError, ValueError):
                    raise exceptions.ValidationError(
                        self.error_messages['invalid'],
                        code='invalid',
                        params={'value': value},
                    )
        return value

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.UUID0Field,
        }
        defaults.update(kwargs)
        return super().formfield(**kwargs)


class UUID0Model(models.Model):
    uuid = UUID0Field(_('UUID'), unique=True, editable=False)

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
    uuid = UUID0Field(_('UUID'), primary_key=True, editable=False)

    class Meta:
        abstract = True
