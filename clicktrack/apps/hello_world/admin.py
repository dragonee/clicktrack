from django.contrib import admin
from .models import Campaign, CampaignCount, Redirect

class CampaignAdmin(admin.ModelAdmin):
    class Meta:
        model = Campaign

admin.site.register(Campaign, CampaignAdmin)

class CampaignCountAdmin(admin.ModelAdmin):
    class Meta:
        model = CampaignCount

admin.site.register(CampaignCount, CampaignCountAdmin)

class RedirectAdmin(admin.ModelAdmin):
    class Meta:
        model = Redirect

admin.site.register(Redirect, RedirectAdmin)
