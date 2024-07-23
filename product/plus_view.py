from django.shortcuts import render
from django.template.response import TemplateResponse


def middleware_view(request):
    return TemplateResponse(request, 'test.html', {'title': 'Testing middleware'})
