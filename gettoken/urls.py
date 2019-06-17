from django.urls import path
from .views import *

app_name = 'gettoken'
urlpatterns = [
    path('get-token-android/', get_token_android, name='get-token-android'),
    path('convert-token/', convert_token, name='convert-token'),
    path('convert-token-ajax/', convert_token_ajax, name='convert-token-ajax'),
]
