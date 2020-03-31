from django.urls import include, path
from django.views.generic import TemplateView

from .views import do_redirect, empty_response

urlpatterns = [
    path('<key>', do_redirect, name='do-redirect'),
    path('', empty_response),
]
