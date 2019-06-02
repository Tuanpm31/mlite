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


def ajax_test(request):
    return render(request, 'ajax.html')


from pagetools.models import TokenUser

@login_required
def ajaxresponse(request):
    data = {}
    token_user = TokenUser.objects.all()
    access_token = token_user[0].access_token
    if request.method == 'POST':
        name = request.POST.get('list')
        data['total'] = 3
        temp = {
            'name': name.split('\n'),
            'i': int(request.POST.get('i'))
        }
        data['order'] = temp
    return JsonResponse(data)

import time
def sendinbox(request):
    time.sleep(2)
    data = {}
    if request.method == 'POST':
        name = request.POST.getlist('name[]')
        data['mess'] = '<h1>Hello {0}</h1>'.format(name[0])
        del name[0]
        temp = {
            'name': name,
            'i': (int(request.POST.get('i')) + 1)
        }
        data['order'] = temp
        return JsonResponse(data)