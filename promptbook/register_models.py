import django
django.setup()

from actstream import registry
from .models import Prompt

registry.register(Prompt)
