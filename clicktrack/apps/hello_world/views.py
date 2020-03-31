from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect

from django.db.models import F
from django.db import IntegrityError

from django.conf import settings

from .models import Redirect, Campaign, CampaignCount

from datetime import datetime, timedelta


def empty_response(request):
    raise Http404


def do_redirect(request, key):
    r = get_object_or_404(Redirect, key=key)

    # a cookie that will be set for 3 hours from last click
    # a duration of single browsing session
    session_cookie_name = '_visited_in_session'

    # a cookie that will be set for 30 days from last click
    # a duration of a unique visit
    unique_cookie_name = '_visited'

    if request.COOKIES.get(unique_cookie_name):
        add_unique = 0
    else:
        add_unique = 1

    if request.COOKIES.get(session_cookie_name):
        add_sessions = 0
    else:
        add_sessions = 1

    r.total = F('total') + 1
    r.unique = F('unique') + add_unique
    r.sessions = F('sessions') + add_sessions

    try:
        campaign = Campaign.objects.get(key=request.GET['c'])

        try:
            CampaignCount.objects.create(
                redirect=r,
                campaign=campaign,
                total=1,
                unique=1,
                sessions=1,
            )
        except IntegrityError:
            CampaignCount.objects.filter(
                redirect=r,
                campaign=campaign
            ).update(
                total=F('total') + 1,
                sessions=F('sessions') + add_sessions,
                unique=F('unique') + add_unique
            )

    except (KeyError, Campaign.DoesNotExist):
        r.non_campaign_total = F('non_campaign_total') + 1
        r.non_campaign_unique = F('non_campaign_unique') + add_unique
        r.non_campaign_sessions = F('non_campaign_sessions') + add_sessions

    r.save()

    response = redirect(r.redirect_to)

    response.set_cookie(
        unique_cookie_name,
        value="1",
        expires=datetime.now() + timedelta(days=30),
        path=request.path,
        secure=settings.SECURE_COOKIES
    )

    response.set_cookie(
        session_cookie_name,
        value="1",
        expires=datetime.now() + timedelta(hours=3),
        path=request.path,
        secure=settings.SECURE_COOKIES
    )

    return response
