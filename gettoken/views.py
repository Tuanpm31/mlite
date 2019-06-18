from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
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
        token = request.POST.get('token')
        payload = {
            'access_token': token,
            'format': 'json',
            'generate_session_cookies': '1',
            'new_app_id': '121876164619130',
        }
        url = 'https://api.facebook.com/method/auth.getSessionforApp'
        r = requests.get(url, params=payload)
        r = r.json()
        if 'access_token' in r:
            data['result'] = r['access_token']
        else:
            data['error'] = 'Token lỗi, thử Token khác'
    return JsonResponse(data)