from django.urls import path, include
from .views import (
    list_token_user_added,
    delete_token_user,
    login_token_user,
    logout_token_user,
    list_pages_inbox_tool,
    page_detail,
    page_get_all_uid,
    get_all_uid_ajax,
    export_file_data_uid,
    page_setting_send_inbox,
    delete_token_page_manager,
    home,
)

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
        path('inboxpage/<int:pk>/', page_detail, name='page-detail'),
        path('inboxpage/<int:pk>/getalluid/', page_get_all_uid, name='page-get-all-uid'),
        path('inboxpage/<int:pk>/getalluidajax/', get_all_uid_ajax, name='page-get-all-uid-ajax'),
        path('inboxpage/<int:pk>/export/', export_file_data_uid, name='page-export-all-data'),
        path('inboxpage/<int:pk>/content/', page_setting_send_inbox, name='page-setting-send-inbox'),
        path('inboxpage/<int:pk>/deletetokenpagemanager/<int:token_page_manager_pk>/', delete_token_page_manager, name='page-delete-token-page-manager'),
    ], 'pagetools'), namespace='page-tools'))

]

