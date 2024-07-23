from django.conf import settings
from django.utils import timezone


class SteinDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.site = None
        self.website = {'url': 'https://codewithdi.com',
                        'debug': settings.DEBUG,
                        'response_time': None}

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.start_time = timezone.now()

    def process_template_response(self, request, response):
        if settings.DEBUG:
            response.context_data['website'] = self.website
            response.context_data['website']['response_time'] = timezone.now() - self.start_time
        return response
