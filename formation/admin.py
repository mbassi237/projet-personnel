from django.contrib import admin

from formation.models import Ressources, Formation, Formation_Content

# Register your models here.
admin.site.register(Ressources)
admin.site.register(Formation)
admin.site.register(Formation_Content)