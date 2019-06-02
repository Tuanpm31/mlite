from django.db import models
from accounts.models import User
from PIL import Image
import facebook


# Create your models here.


class TokenUser(models.Model):
    user = models.ForeignKey(User, related_name='tokensadded', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    is_logged_in = models.BooleanField(default=False)
    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.access_token)
    

class TokenUserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile_token', on_delete=models.CASCADE)
    token_user = models.OneToOneField(TokenUser, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=80)
    uid = models.CharField(max_length=50)
    profile_picture_link = models.CharField(max_length=255)
    profile_link = models.CharField(max_length=255)
    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.uid)
    
    

class PageOwnerByTokenUser(models.Model):
    token_user_profile = models.ManyToManyField(TokenUserProfile, related_name='pages', blank=True)
    name = models.CharField(max_length=255)
    uid = models.CharField(max_length=50)
    likes = models.IntegerField()
    profile_picture_link = models.CharField(max_length=255)
    profile_link = models.CharField(max_length=255)
    def __str__(self):
        return '{0} - {1}'.format(self.name, self.uid)


class TokenPageManager(models.Model):
    token_user_profile = models.ForeignKey(TokenUserProfile, related_name='tokenspagemanager', on_delete=models.CASCADE)
    page = models.ForeignKey(PageOwnerByTokenUser, related_name='tokenspagemanager', on_delete=models.CASCADE)
    token_page_manager = models.CharField(max_length=255)
    def __str__(self):
        return '{0} - {1}'.format(self.page.name, self.token_page_manager)
    
    
class TokenPageManagerProfile(models.Model):
    token_page_manager = models.OneToOneField(TokenPageManager, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    uid = models.CharField(max_length=50)
    profile_picture_link = models.CharField(max_length=255)
    profile_link = models.CharField(max_length=255)

class DataUIDOfPage(models.Model):
    page = models.ForeignKey(PageOwnerByTokenUser, related_name='data', on_delete=models.CASCADE)
    conversation_id = models.CharField(max_length=100)
    uid = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    last_updated = models.DateField(auto_now=False, auto_now_add=False)
    def __str__(self):
        return '{0} - {1}'.format(self.page.name, self.uid)


class PageAccessToken(models.Model):
    token_page_manager = models.OneToOneField(TokenPageManager, on_delete=models.CASCADE)
    page_access_token = models.CharField(max_length=255)


class ContentSendInbox(models.Model):
    page = models.ForeignKey(PageOwnerByTokenUser, related_name='contents', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='image_send_inbox', blank=True, null=True)
