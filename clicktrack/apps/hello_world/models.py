from django.db import models

from django.utils.translation import ugettext_lazy as _

class Redirect(models.Model):
    key = models.CharField(unique=True, max_length=128)
    redirect_to = models.CharField(max_length=512)

    unique = models.PositiveIntegerField(default=0)
    sessions = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    non_campaign_unique = models.PositiveIntegerField(default=0)
    non_campaign_sessions = models.PositiveIntegerField(default=0)
    non_campaign_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{} -> {}".format(self.key, self.redirect_to)



class Campaign(models.Model):
    key = models.CharField(unique=True, max_length=128)

    desc = models.TextField(blank=True, default='')

    redirects = models.ManyToManyField(Redirect, related_name='campaigns', through='CampaignCount')

    def __str__(self):
        return self.key


class CampaignCount(models.Model):
    redirect = models.ForeignKey(Redirect, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    unique = models.PositiveIntegerField(default=0)
    sessions = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{}: {}".format(self.redirect, self.campaign)

    class Meta:
        unique_together = ('redirect', 'campaign')
