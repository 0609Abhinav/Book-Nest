from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.cache import cache

def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user'):
            messages.warning(request, "Please sign in to access this page.")
            return redirect('/senior/signin/')
        return view_func(request, *args, **kwargs)
    return wrapper

def rate_limit(key_prefix, limit, timeout):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR')
            key = f"{key_prefix}_{ip}"
            requests = cache.get(key, 0)
            if requests >= limit:
                messages.error(request, "Too many requests. Please try again later.")
                return redirect('/senior/home/')
            cache.set(key, requests + 1, timeout)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
