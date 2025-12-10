from django.utils.deprecation import MiddlewareMixin

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.school = None
        # If user is logged in, attach their school to the request
        if request.user.is_authenticated and hasattr(request.user, 'school'):
            request.school = request.user.school