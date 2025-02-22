from django.shortcuts import redirect

class EnforceDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.get_host().endswith(".herokuapp.com"):
            return redirect("https://topsoftware.tech" + request.get_full_path(), permanent=True)
        return self.get_response(request)