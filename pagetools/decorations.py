from .models import TokenUser, TokenUserProfile, PageOwnerByTokenUser
from django.http import HttpResponseForbidden

def user_owner_token_user(function):
    def wrap(request, *args, **kwargs):
        token_user = TokenUser.objects.get(pk=kwargs['pk'])
        if token_user.user == request.user:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('Token này không thuộc về bạn.')
    return wrap

def page_belong_to_token_user_profile(function):
    def wrap(request, *args, **kwargs):
        page = PageOwnerByTokenUser.objects.get(pk=kwargs['pk'])
        user = request.user
        logged_in_token_user = user.tokensadded.filter(is_logged_in=True).first()
        token_user_profile = logged_in_token_user.tokenuserprofile
        if token_user_profile in page.token_user_profile.all():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('Page này không thuộc về bạn.')
    return wrap