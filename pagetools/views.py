from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorations import (
    user_owner_token_user,
    page_belong_to_token_user_profile,
    )
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from .models import (
    TokenUser,
    TokenUserProfile,
    PageOwnerByTokenUser,
    DataUIDOfPage,
    TokenPageManager,
    ContentSendInbox,
)
from django.core import serializers
from .forms import CreateContentSendInbox, UpdateContentSendInbox
import os
import facebook
import requests
import json
import csv

# Create your views here.


# This will show list of token user added
@login_required
def list_token_user_added(request):
    user = request.user
    if user.tokensadded.filter(is_logged_in=True).exists():
        return redirect('home')
    list_token_user_added = user.tokensadded.all()
    context = {
        'title': 'List Token',
        'tokens_user': list_token_user_added
    }
    if request.method == 'POST':
        if request.POST.get('tokenuseradded'):
            token_user_added = request.POST.get('tokenuseradded')
            try:
                graph = facebook.GraphAPI(token_user_added)
                info = graph.get_object('me')
                name = info['name']
                uid = info['id']
                token_user_profile = TokenUserProfile.objects.filter(uid=uid, user=user).first()
                if token_user_profile is None:
                    TokenUser.objects.create(access_token=token_user_added, user=user)
                    messages.success(request, 'Thêm Token {0} - {1} thành  công!!!!!'.format(name, uid))
                else:
                    if token_user_profile.token_user is None:
                        token_user = TokenUser.objects.bulk_create([
                            TokenUser(access_token=token_user_added, user=user)
                        ])
                        token_user_save = TokenUser.objects.get(access_token=token_user_added, user=user)
                        token_user_profile.token_user = token_user_save
                        token_user_profile.save()
                        messages.success(request, 'Thêm Token {0} - {1} thành công!!!!!'.format(name, uid))
                    else:
                        token_user_profile.token_user.delete()
                        token_user = TokenUser.objects.bulk_create([
                            TokenUser(access_token=token_user_added,user=user)
                        ])
                        token_user_save = TokenUser.objects.get(access_token=token_user_added, user=user)
                        token_user_profile.token_user = token_user_save
                        token_user_profile.save()
                        messages.success(request, 'Cập nhật Token {0} - {1} thành công !!!'.format(name, uid))
            except:
                messages.warning(request, 'Token lỗi, hãy thử lại!!')
        if request.POST.get('checklive'):
            list_token_added = TokenUser.objects.filter(user=user)
            for token in list_token_added:
                try:
                    graph = facebook.GraphAPI(token.access_token)
                    info = graph.get_object('me')
                except facebook.GraphAPIError:
                    token_die = TokenUser.objects.get(access_token=token.access_token, user=user)
                    name = token_die.tokenuserprofile.name
                    uid = token_die.tokenuserprofile.uid
                    token_die.delete()
                    messages.success(request, 'Token {0} - {1} Die, xóa thành công!!'.format(name, uid))
        return redirect('token:list-tokenuser')
    return render(request, 'pagetools/list_token_user_added.html', context=context)


@login_required
@user_owner_token_user
def delete_token_user(request, pk):
    token_user = get_object_or_404(TokenUser, pk=pk)
    name = token_user.tokenuserprofile.name
    uid = token_user.tokenuserprofile.uid
    token_user.delete()
    messages.success(request, 'Xóa Token {0} - {1} thành công!'.format(name, uid))
    return redirect('token:list-tokenuser')


@login_required
@user_owner_token_user
def login_token_user(request, pk):
    token_user = get_object_or_404(TokenUser, pk=pk)
    access_token = token_user.access_token
    try:
        graph = facebook.GraphAPI(access_token)
        info = graph.get_object('me')
        name = info['name']
        uid = info['id']
        if request.user.tokensadded.filter(is_logged_in=True).exists():
            return redirect('home')
        else:
            token_user.is_logged_in = True
            token_user.save()
            messages.success(request, 'Đăng nhập Token {0} - {1} thành công'.format(name, uid))
            return redirect('home')
    except facebook.GraphAPIError:
        token_user.delete()
        messages.warning(request, 'Token Die, hãy thử lại!!')
        return redirect('token:list-tokenuser')

@login_required
@user_owner_token_user
def logout_token_user(request, pk):
    token_user = get_object_or_404(TokenUser, pk=pk)
    if token_user.is_logged_in:
        token_user.is_logged_in = False
        token_user.save()
        messages.success(request, 'Đăng xuất khỏi Token thành công!!')
        return redirect('token:list-tokenuser')

def check_is_logged_in(user):
    return user.tokensadded.filter(is_logged_in=True).exists()


@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
def home(request):
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    context = {
        'title': 'Trang Chủ',
        'logged_in_token_user': logged_in_token_user
    }
    return render(request, 'pagetools/home.html', context=context)

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
def list_pages_inbox_tool(request):
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    access_token = logged_in_token_user.access_token
    graph = facebook.GraphAPI(access_token=access_token)
    try:
        info = graph.get_object('me')
        pages = logged_in_token_user.tokenuserprofile.pages.all().order_by('-likes')
        context = {
            'title': 'Danh Sách Trang',
            'logged_in_token_user': logged_in_token_user,
            'pages': pages
        }
        return render(request, 'pagetools/list_pages_inbox_tool.html', context=context)
    except facebook.GraphAPIError:
        logged_in_token_user.delete()
        messages.warning(request, 'Token lỗi hoặc bị checkpoint, hãy thử lại token khác')
        return redirect('token:list-tokenuser')

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
def update_page_belong_to_token_user(request):
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    token_user_profile = logged_in_token_user.tokenuserprofile
    graph = facebook.GraphAPI(logged_in_token_user.access_token)
    list_pages = graph.get_connections(id='me', connection_name='accounts')
    while 'paging' in list_pages:
        for page in list_pages['data']:
            name = page['name']
            uid = page['id']
            likes = int(graph.get_object('{0}?fields=fan_count'.format(uid))['fan_count'])
            if PageOwnerByTokenUser.objects.filter(uid=uid).exists():
                page_exists = PageOwnerByTokenUser.objects.filter(uid=uid).first()
                if token_user_profile in page_exists.token_user_profile.all():
                    page_exists.likes = likes
                    page_exists.save()
                else:
                    page_exists.likes = likes
                    page_exists.save()
                    page_exists.token_user_profile.add(token_user_profile)
            else:
                profile_picture_link = 'https://graph.facebook.com/v3.1/{0}/picture?type=small&amp;redirect=true'.format(uid)
                profile_link = 'https://www.facebook.com/{0}'.format(uid)
                create_page = PageOwnerByTokenUser.objects.create(name=name, uid=uid, likes=likes, profile_picture_link=profile_picture_link, profile_link=profile_link)
                create_page.token_user_profile.add(token_user_profile)
        list_pages = graph.get_connections(id='me', connection_name='accounts', after=list_pages['paging']['cursors']['after'])
    return redirect('page-tools:list-pages-inbox-tool')

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def page_detail(request, pk):
    page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
    data = page.data.all()
    total_uid = data.count()
    male_filter_uid = data.filter(gender='male').count()
    female_filter_uid = data.filter(gender='female').count()
    no_gender_filter_uid = data.filter(gender='').count()
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    context = {
        'title': page.name,
        'logged_in_token_user': logged_in_token_user,
        'page': page,
        'data': data,  
        'total_count': total_uid,
        'male_count': male_filter_uid,
        'female_count': female_filter_uid,
        'nogender_count': no_gender_filter_uid,
    }
    return render(request, 'pagetools/page_detail.html', context=context)


@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def export_file_data_uid(request, pk):
    page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="alluid.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Tên', 'UID', 'Conversation-id', 'Giới tính'])
    data = page.data.all().values_list('name', 'uid', 'conversation_id', 'gender')
    for each_data in data:
        writer.writerow(each_data)
    return response

    

    
@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def page_get_all_uid(request, pk):
    page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    context = {
        'title': '{0} Quét UID'.format(page.name),
        'logged_in_token_user': logged_in_token_user,
        'page': page,
    }
    return render(request, 'pagetools/page_get_all_uid.html', context=context)

# @login_required
# @user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
# @page_belong_to_token_user_profile
# def get_all_uid_ajax(request, pk):
#     logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
#     page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
#     graph = facebook.GraphAPI(logged_in_token_user.access_token)
#     data = {}
#     try:
#         if request.method == 'POST':
#             page_access_token = graph.get_object('{0}?fields=access_token'.format(page.uid))['access_token']
#             graph_page = facebook.GraphAPI(page_access_token)
#             conversations = graph_page.get_connections(id='me', connection_name='conversations')
#             total = 0
#             while 'paging' in conversations:
#                 for conversation in conversations['data']:
#                     conversation_id = conversation['id']
#                     name = conversation['participants']['data'][0]['name']
#                     uid = conversation['participants']['data'][0]['id']
#                     last_updated = conversation['updated_time'][0:10]
#                     gender = ''
#                     try:
#                         gender = graph.get_object('{0}?fields=name,gender'.format(uid))['gender']
#                     except:
#                         gender = ''
#                     defaults = {
#                         'page': page,
#                         'uid': uid
#                     }
#                     obj, created = DataUIDOfPage.objects.update_or_create(
#                         page=page, conversation_id=conversation_id, name=name, uid=uid, last_updated=last_updated, gender=gender,
#                         defaults=defaults,
#                     )
#                     total += 1
#                 conversations = graph_page.get_connections(id='me', connection_name='conversations', after=conversations['paging']['cursors']['after'])
#             data['mess_success'] = '<h4> Quét thành công {0} UID</h4>'.format(total)
#     except facebook.GraphAPIError:
#         data['error'] = 'Có lỗi, hãy thử kiểm tra lại Token!'
#     return JsonResponse(data)

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def get_all_uid_ajax(request, pk):
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
    graph = facebook.GraphAPI(logged_in_token_user.access_token)
    data = {}
    try:
        if request.method == 'POST' and request.is_ajax():
            page_access_token = graph.get_object('{0}?fields=access_token'.format(page.uid))['access_token']
            graph_page = facebook.GraphAPI(page_access_token)
            conversations = graph_page.get_connections(id='me', connection_name='conversations')
            added = 0
            for conversation in conversations['data']:
                conversation_id = conversation['id']
                name = conversation['participants']['data'][0]['name']
                uid = conversation['participants']['data'][0]['id']
                last_updated = conversation['updated_time'][0:10]
                gender = ''
                try:
                    gender = graph.get_object('{0}?fields=name,gender'.format(uid))['gender']
                except:
                    gender = ''
                defaults = {
                    'page': page,
                    'uid': uid
                }
                obj, created = DataUIDOfPage.objects.update_or_create(
                    page=page, conversation_id=conversation_id, name=name, uid=uid, last_updated=last_updated, gender=gender,
                    defaults=defaults,
                )
                added += 1
            data['added'] = added
            if 'paging' in conversations:
                data['after'] = conversations['paging']['cursors']['after']
    except facebook.GraphAPIError:
        data['error'] = 'Có lỗi, hãy thử kiểm tra lại Token!'
    return JsonResponse(data)

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def get_uid_each_page_ajax(request, pk):
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
    graph = facebook.GraphAPI(logged_in_token_user.access_token)
    data = {}
    try:
        if request.method == 'POST' and request.is_ajax():
            after = request.POST.get('after')
            page_access_token = graph.get_object('{0}?fields=access_token'.format(page.uid))['access_token']
            graph_page = facebook.GraphAPI(page_access_token)
            conversations = graph_page.get_connections(id='me', connection_name='conversations', after=after)
            added = 0
            for conversation in conversations['data']:
                conversation_id = conversation['id']
                name = conversation['participants']['data'][0]['name']
                uid = conversation['participants']['data'][0]['id']
                last_updated = conversation['updated_time'][0:10]
                gender = ''
                try:
                    gender = graph.get_object('{0}?fields=name,gender'.format(uid))['gender']
                except:
                    gender = ''
                defaults = {
                    'page': page,
                    'uid': uid
                }
                obj, created = DataUIDOfPage.objects.update_or_create(
                    page=page, conversation_id=conversation_id, name=name, uid=uid, last_updated=last_updated, gender=gender,
                    defaults=defaults,
                )
                added += 1
            data['added'] = added
            if 'paging' in conversations:
                data['after'] = conversations['paging']['cursors']['after']
    except facebook.GraphAPIError:
        data['error'] = 'Có lỗi, hãy thử kiểm tra lại Token!'
    return JsonResponse(data)

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def page_setting_send_inbox(request, pk):
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    token_user_profile = logged_in_token_user.tokenuserprofile
    page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
    tokens_page_manager = TokenPageManager.objects.filter(token_user_profile=token_user_profile, page=page)
    contents = page.contents.all()
    for token_page_manager in tokens_page_manager:
        page_access_token = token_page_manager.pageaccesstoken.page_access_token
        try:
            graph = facebook.GraphAPI(page_access_token)
            info = graph.get_object('me')
        except:
            token_page_manager.delete()
    if request.method == 'POST':
        if request.POST.get('tokenpagemanageradded'):
            token_page_manager_added = request.POST.get('tokenpagemanageradded')
            try:
                graph = facebook.GraphAPI(token_page_manager_added)
                info = graph.get_object('me')
                response = requests.get('https://graph.facebook.com/app?access_token={0}'.format(token_page_manager_added))
                if not 'error' in response.json():
                    type = response.json()['name']
                    if type == 'Pages Manager for Android':
                        if 'access_token' in graph.get_object('{0}?fields=access_token'.format(page.uid)):
                            token_page_manger_created = TokenPageManager.objects.create(token_user_profile=token_user_profile, page=page, token_page_manager=token_page_manager_added)
                            messages.success(request, 'Thêm Token Page Manager Thành công')
                    else:
                        messages.warning('Không Phải Token Page Manager, Hãy thử lại Token khác nhé!!')
            except:
                messages.warning(request, 'Token Lỗi, Hãy Thử Lại!')
        create_content_form = CreateContentSendInbox(request.POST, request.FILES)
        if create_content_form.is_valid():
            create_content = create_content_form.save(commit=False)
            create_content.page = page
            create_content.save()
            messages.success(request, 'Thêm Content Thành Công!')
        return HttpResponseRedirect(request.path_info)
    else:
        create_content_form = CreateContentSendInbox()
        
    context = {
        'title': '{0} Setting'.format(page.name),
        'logged_in_token_user': logged_in_token_user,
        'page': page,
        'tokens_page_manager': tokens_page_manager,
        'form': create_content_form,
        'contents': contents
    }
    return render(request, 'pagetools/page_setting_send_inbox.html', context=context)


@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def delete_token_page_manager(request, pk, token_page_manager_pk):
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    token_user_profile = logged_in_token_user.tokenuserprofile
    token_page_manager = get_object_or_404(TokenPageManager, pk=token_page_manager_pk)
    token_page_manager.delete()
    messages.success(request, 'Xóa Token Page Manager thành công !!')
    return redirect('page-tools:page-setting-send-inbox', pk=pk)
    
@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def delete_content_send_inbox(request, pk, content_pk):
    content = get_object_or_404(ContentSendInbox, pk=content_pk)
    content.delete()
    messages.success(request, 'Xóa Tin Nhắn Thành Công!!!')
    return redirect('page-tools:page-setting-send-inbox', pk=pk)

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def update_content_send_inbox(request, pk, content_pk):
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
    content = get_object_or_404(ContentSendInbox, pk=content_pk)
    if request.method == 'POST':
        form = UpdateContentSendInbox(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập Nhật Content Thành Công!!')
            return redirect('page-tools:page-setting-send-inbox', pk=pk)
    else:
        form = UpdateContentSendInbox(instance=content)
    context = {
        'title': 'Update Content {0}'.format(page.name),
        'logged_in_token_user': logged_in_token_user,
        'page': page,
        'content': content,
        'form': form
    }
    return render(request, 'pagetools/page_update_content.html', context=context)

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def delete_image_in_content_send_inbox(request, pk, content_pk):
    content = get_object_or_404(ContentSendInbox, pk=content_pk)
    content.image.delete()
    messages.success(request, 'Xóa Hình Ảnh Thành Công!')
    return redirect('page-tools:page-setting-send-inbox', pk=pk)

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def send_inbox(request, pk):
    logged_in_token_user = TokenUser.objects.get(user=request.user, is_logged_in=True)
    access_token = logged_in_token_user.access_token
    graph = facebook.GraphAPI(access_token=access_token)
    try:
        graph.get_object('me')
    except facebook.GraphAPIError:
        logged_in_token_user.delete()
        messages.warning(request, 'Token đã Die, vui lòng chọn Token Khác nhé')
        return redirect('token:list-tokenuser')
    page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
    contents = page.contents.all()
    tokens_page_manager = page.tokenspagemanager.all()
    for token_page_manager in tokens_page_manager:
        page_access_token = token_page_manager.pageaccesstoken.page_access_token
        try:
            graph = facebook.GraphAPI(page_access_token)
            graph.get_object('me')
        except facebook.GraphAPIError:
            token_page_manager.delete()
    context = {
        'title': '{0} Send Inbox'.format(page.name),
        'logged_in_token_user': logged_in_token_user,
        'page': page,
        'contents': contents,
        'tokens_page_manager': tokens_page_manager,
    }
    return render(request, 'pagetools/send_inbox.html', context=context)

REMOTE_SERVER = 'https://www.google.com/'
TIME_OUT = 5

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def settings_send_inbox_ajax(request, pk):
    page = get_object_or_404(PageOwnerByTokenUser, pk=pk)
    tokens_page_manager = page.tokenspagemanager.all()
    data = {}
    for token_page_manager in tokens_page_manager:
        page_access_token = token_page_manager.pageaccesstoken.page_access_token
        try:
            graph = facebook.GraphAPI(page_access_token)
            graph.get_object('me')
        except facebook.GraphAPIError:
            token_page_manager.delete()
            data['error_token'] = 'Token Lỗi, Có Token bị die, load lại page bạn nhé!!'
            break
    if request.method == "POST" and request.is_ajax():
        try:
            _ = requests.get(REMOTE_SERVER, timeout=TIME_OUT)
            list_conversations = request.POST.get('list_conversations_id').split("\n")
            list_conversations = list(filter(None, list_conversations))
            list_conversations = [i.strip() for i in list_conversations]
            settings = {
                'delay_time': int(request.POST.get('delaytime')),
                'day_between': int(request.POST.get('daybetween')),
                'list_conversations': list_conversations
            }
            data['settings'] = settings
        except requests.ConnectionError:
            data['error_connection'] = 'Lỗi kết nối'
    return JsonResponse(data)

import time
import datetime
from .helper import *

@login_required
@user_passes_test(check_is_logged_in, login_url='token:list-tokenuser')
@page_belong_to_token_user_profile
def sendinbox_ajax(request, pk):
    data = {}
    if request.method == "POST" and request.is_ajax():
        try:
            _ = requests.get(REMOTE_SERVER, timeout=TIME_OUT)      
        except requests.ConnectionError:
            data['error_connection'] = 'Lỗi Kết Nối Mạng'
            return JsonResponseO(data)
        delay_time = int(request.POST.get('delay_time'))
        day_between = int(request.POST.get('day_between'))
        if delay_time > 4:
            time.sleep(delay_time - 4)
        else :
            time.sleep(1)
        list_conversations = request.POST.getlist('list_conversations[]')
        conversation_id = list_conversations[0]
        data['conversation_id'] = conversation_id
        del list_conversations[0]
        try:
            info = DataUIDOfPage.objects.get(conversation_id=conversation_id)
            data['name'] = info.name
            data['uid'] = info.uid
            current_date = datetime.datetime.now().date()
            info_date = info.last_updated
            data['days'] = (current_date - info_date).days
            if (current_date - info_date).days < day_between:
                data['error_date'] = 'người này mới nhận tin nhắn cách đây {0} ngày'.format((current_date - info_date).days)
            else: 
                sender, page_access_token = get_random_page_access_token(pk)
                data['sender'] = sender
                content = get_random_content(pk)
                validated_content = content.content
                validated_content = validate_content(content.content, info.name)
                data['content'] = validated_content
                data['status'] = send_inbox_helper(conversation_id, page_access_token, validated_content, content.image)
        except DataUIDOfPage.DoesNotExist:
            data['error_notfound'] = 'Not Found'
        settings = {
            'delay_time': delay_time,
            'day_between': day_between,
            'list_conversations': list_conversations
        }
        data['settings'] = settings
    return JsonResponse(data)

