from django.contrib import admin
from bo.models import __all__

for model in __all__:
    admin.site.register(model)

