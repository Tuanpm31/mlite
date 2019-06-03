from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import (
    TokenUser,
    TokenUserProfile,
    PageOwnerByTokenUser,
    TokenPageManager,
    TokenPageManagerProfile,
    PageAccessToken,
    ContentSendInbox,
)
import facebook
import os

@receiver(post_save, sender=TokenUser)
def create_token_user_profile(sender, instance, created, **kwargs):
    if created:
        access_token = instance.access_token
        graph = facebook.GraphAPI(access_token=access_token)
        info = graph.get_object('me')
        name = info['name']
        uid = info['id']
        profile_picture_link = 'https://graph.facebook.com/v3.1/{0}/picture?type=small&amp;redirect=true'.format(uid)
        profile_link = 'https://www.facebook.com/{0}'.format(uid)
        token_user_profile = TokenUserProfile.objects.create(user=instance.user, token_user=instance, name=name, uid=uid, profile_picture_link=profile_picture_link, profile_link=profile_link)



@receiver(post_save, sender=TokenUserProfile)
def create_page_owner_by_token(sender, instance, created, **kwargs):
    if created:
        token_user_profile = instance
        access_token = instance.token_user.access_token
        graph = facebook.GraphAPI(access_token=access_token)
        list_pages = graph.get_connections(id='me', connection_name='accounts')
        while 'paging' in list_pages:
            for page in list_pages['data']:
                name = page['name']
                uid = page['id']
                if PageOwnerByTokenUser.objects.filter(uid=uid).exists():
                    page_exists = PageOwnerByTokenUser.objects.filter(uid=uid).first()
                    page_exists.token_user_profile.add(token_user_profile)
                else:
                    likes = int(graph.get_object('{0}?fields=fan_count'.format(uid))['fan_count'])
                    profile_picture_link = 'https://graph.facebook.com/v3.1/{0}/picture?type=small&amp;redirect=true'.format(uid)
                    profile_link = 'https://www.facebook.com/{0}'.format(uid)
                    create_page = PageOwnerByTokenUser.objects.create(name=name, uid=uid, likes=likes, profile_picture_link=profile_picture_link, profile_link=profile_link)
                    create_page.token_user_profile.add(token_user_profile)            
            list_pages = graph.get_connections(id='me', connection_name='accounts', after=list_pages['paging']['cursors']['after'])

@receiver(post_save, sender=TokenPageManager)
def create_token_page_manager_profile_and_page_access_token(sender, instance, created, **kwargs):
    if created:
        page = instance.page
        token_user_profile = instance.token_user_profile
        token_page_manager = instance.token_page_manager
        graph = facebook.GraphAPI(token_page_manager)
        info = graph.get_object('me')
        name = info['name']
        uid = info['id']
        profile_picture_link = 'https://graph.facebook.com/v3.1/{0}/picture?type=small&amp;redirect=true'.format(uid)
        profile_link = 'https://www.facebook.com/{0}'.format(uid)
        token_page_manager_profile = TokenPageManagerProfile.objects.create(token_page_manager=instance, name=name, uid=uid, profile_picture_link=profile_picture_link, profile_link=profile_link)
        page_access_token = graph.get_object('{0}?fields=access_token'.format(page.uid))['access_token']
        page_access_token_create = PageAccessToken.objects.create(token_page_manager=instance, page_access_token=page_access_token)

@receiver(post_delete, sender=ContentSendInbox)
def delete_content_send_inbox(sender, instance, **kwargs):
    instance.image.delete(False)
