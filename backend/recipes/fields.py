from django.db import models
from django.core import validators


class HexColorField(models.CharField):
    """Поле для хранения HTML-кода цвета"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        super().__init__(*args, **kwargs)
        self.validators.append(
            validators.RegexValidator(r'#([a-fA-F0-9]{6})')
        )


