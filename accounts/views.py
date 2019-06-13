from django.shortcuts import render
from django.contrib import messages
from .forms import UserRegister
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, 'Tài khoản {} được tạo thành công'.format(username))
            return HttpResponse('Đăng ký thành công')
    else:
        form = UserRegister()
    context = {
        'title': 'Đăng Ký Tài Khoản',
        'form': form
    }
    return render(request, 'registration/register.html', context=context)


