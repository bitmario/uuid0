import django.forms.fields as fields
from django.utils.translation import ugettext_lazy as _

import uuid0

class UUID0Field(fields.CharField):
    default_error_messages = {
        'invalid': _('Enter a valid UUID.'),
    }

    def prepare_value(self, value):
        if isinstance(value, uuid0.UUID):
            return value.base62
        return value

    def to_python(self, value):
        value = super().to_python(value)
        if value in self.empty_values:
            return None
        if not isinstance(value, uuid0.UUID):
            try:
                value = uuid0.UUID(base62=value)
            except ValueError:
                raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value
