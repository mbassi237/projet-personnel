from django.contrib import admin

from mentorat.models import Mentoring, MentoringMessage

# Register your models here.
admin.site.register(Mentoring)
admin.site.register(MentoringMessage)