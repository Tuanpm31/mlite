from django.contrib import admin
from .models import(
    TokenUser,
    TokenUserProfile,
    PageOwnerByTokenUser,
    TokenPageManager,
    TokenPageManagerProfile,
    PageAccessToken,
    ContentSendInbox,
    DataUIDOfPage,
)
# Register your models here.

admin.site.register(TokenUser)
admin.site.register(TokenUserProfile)
admin.site.register(PageOwnerByTokenUser)
admin.site.register(TokenPageManager)
admin.site.register(TokenPageManagerProfile)
admin.site.register(PageAccessToken)
admin.site.register(ContentSendInbox)
admin.site.register(DataUIDOfPage)