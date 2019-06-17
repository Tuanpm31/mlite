from django.shortcuts import render
from django.http import JsonResponse
import requests
# Create your views here.
def get_token_android(request):
    context = {
        'title': 'Get Token Android',
    }
    return render(request, 'gettoken/get_token_android.html', context=context)

def convert_token(request):
    context = {
        'title': 'Đổi Token',
    }
    return render(request, 'gettoken/convert_token.html', context=context)

def convert_token_ajax(request):
    data = {}
    if request.method == 'POST' and request.is_ajax():
        data['ok'] = 'success'
    return JsonResponse(data)