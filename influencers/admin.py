from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(NoisemakerProfile)
admin.site.register(Campaigns)
admin.site.register(Tracker)
admin.site.register(Payouts)
admin.site.register(Requested)