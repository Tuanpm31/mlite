from django.shortcuts import get_object_or_404
from pagetools.models import *
import facebook
import random

def get_random_page_access_token(page_pk):
    page = get_object_or_404(PageOwnerByTokenUser, pk=page_pk)
    rd = random.choice(page.tokenspagemanager.all())
    sender = rd.tokenpagemanagerprofile.name
    page_access_token = rd.pageaccesstoken.page_access_token
    return sender, page_access_token

def get_random_content(page_pk):
    page = get_object_or_404(PageOwnerByTokenUser, pk=page_pk)
    rd = random.choice(page.contents.all())
    return rd

def validate_content(content, name):
    icons = ['😍', '😘', '💓', '😂', '🤣', '😚', '🎁', '😽']
    content = content.replace('[[full_name]]', name)
    content = content.replace('[[emo_fun]]', random.choice(icons))
    return content

def send_inbox_helper(conversation_id, page_access_token, content, image):
    graph = facebook.GraphAPI(page_access_token)
    try:
        graph.get_object('me')
        url = '{0}/{1}/messages'.format('v3.1', conversation_id)
        files = {
            'image': ('image', open(image.path, 'rb'), 'image/jpeg')
        }
        args = {
            'message': content
        }
        try:
            response = graph.request(url, args=args, files=files, method='POST')
            return 'success'
        except facebook.GraphAPIError:
            return 'failed'
    except facebook.GraphAPIError:
        return 'tokenerror'