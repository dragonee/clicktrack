from django.http import HttpResponse, Http404

def empty_response(request):
    raise Http404

def do_redirect(request, key):
    return HttpResponse(key)