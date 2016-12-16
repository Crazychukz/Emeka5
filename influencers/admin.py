from django.contrib import admin
from .models import *
from .models import Campaigns


# Register your models here.
class CampaignsAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'base_pay' , 'dummy_tracker', 'approved', 'budget')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'decibel', 'number_of_friends', 'rank', 'escrow')
class TrackerAdmin(admin.ModelAdmin):
    list_display = ('trackers_ID', 'tracking_ID', 'campaign')

class PayoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_requested','date_requested', 'approved', 'paid' )

admin.site.register(NoisemakerProfile, ProfileAdmin)
admin.site.register(Campaigns, CampaignsAdmin)
admin.site.register(Tracker, TrackerAdmin)
admin.site.register(Payouts, PayoutAdmin)
admin.site.register(Requested,)




