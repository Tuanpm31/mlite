from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('token/', include(([
        path('listadded/', list_token_user_added, name='list-tokenuser'),
        path('<int:pk>/delete/', delete_token_user, name='delete-tokenuser'),
        path('<int:pk>/login/', login_token_user, name='login-tokenuser'),
        path('<int:pk>/logout/', logout_token_user, name='logout-tokenuser'),
    ], 'pagetools'), namespace='token')),

    path('page-tools/', include(([
        path('inboxpage/list', list_pages_inbox_tool, name='list-pages-inbox-tool'),
        path('inboxpage/updatepage/', update_page_belong_to_token_user, name='update-list-pages'),
        path('inboxpage/<int:pk>/', page_detail, name='page-detail'),
        path('inboxpage/<int:pk>/getalluid/', page_get_all_uid, name='page-get-all-uid'),
        path('inboxpage/<int:pk>/getalluidajax/', get_all_uid_ajax, name='page-get-all-uid-ajax'),
        path('inboxpage/<int:pk>/export/', export_file_data_uid, name='page-export-all-data'),
        path('inboxpage/<int:pk>/content/', page_setting_send_inbox, name='page-setting-send-inbox'),
        path('inboxpage/<int:pk>/deletetokenpagemanager/<int:token_page_manager_pk>/', delete_token_page_manager, name='page-delete-token-page-manager'),
        path('inboxpage/<int:pk>/deletecontent/<int:content_pk>/', delete_content_send_inbox, name='page-delete-content'),
        path('inboxpage/<int:pk>/updatecontent/<int:content_pk>/', update_content_send_inbox, name='page-update-content'),
        path('inboxpage/<int:pk>/deleteimageincontent/<int:content_pk>/', delete_image_in_content_send_inbox, name='page-delete-image-in-content'),
    ], 'pagetools'), namespace='page-tools'))

]

