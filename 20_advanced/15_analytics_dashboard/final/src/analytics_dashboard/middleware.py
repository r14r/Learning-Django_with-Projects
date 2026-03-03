from .models import PageView

SKIP_PREFIXES = ('/admin', '/static', '/media', '/__debug__')


class PageViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (response.status_code == 200 and
                not any(request.path.startswith(p) for p in SKIP_PREFIXES)):
            try:
                PageView.objects.create(
                    path        = request.path[:500],
                    method      = request.method,
                    user        = request.user if request.user.is_authenticated else None,
                    session_key = (request.session.session_key or '')[:40],
                    user_agent  = request.META.get('HTTP_USER_AGENT', '')[:500],
                    referer     = request.META.get('HTTP_REFERER', '')[:2000],
                    ip_address  = request.META.get('REMOTE_ADDR'),
                )
            except Exception:
                pass
        return response
