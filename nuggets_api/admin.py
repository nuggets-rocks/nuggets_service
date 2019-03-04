from django.contrib import admin
from .models import Nugget, NuggetUser

# Register your models here.
admin.site.register(Nugget)
admin.site.register(NuggetUser)
