from django.shortcuts import redirect
from django.contrib import messages


class RestrictDjangoAdminMiddleware:
    """
    Block access to /admin/ for anyone who is not a superuser.
    Staff users (is_staff=True, is_superuser=False) are redirected
    to the custom admin dashboard instead.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated:
                return redirect(f'/login/?next={request.path}')
            if not request.user.is_superuser:
                messages.error(
                    request,
                    'Access denied. The Django admin panel is restricted to master administrators only.'
                )
                return redirect('admin_dashboard')
        return self.get_response(request)
