from django.contrib import admin

from mentorat.models import Mentoring, MentoringMessage, Mentor

# Register your models here.
admin.site.register(Mentoring)
admin.site.register(MentoringMessage)
admin.site.register(Mentor)