from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchResults/', views.SearchResultsView.as_view(), name='search_results'),
    path('home/', views.home, name='home'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path("accounts/", include("allauth.urls")),
    path('logout', LogoutView.as_view(), name='logout'),

    path('deptlist/', views.deptlist, name="deptlist"),
    path('deptdisplay/<str:dept_name>/', views.dept_display_only, name="deptdisplay"),
    path('deptdisplay/<str:dept_name>/classlookup/', views.class_lookup, name="classlookup"),
    
    path('home/<str:room>/', views.room, name='room'),
    path('home/go_to_chat', views.go_to_chat, name='go_to_chat'),
    path('home/checkview', views.checkview, name='checkview'),
    path('home/send', views.send, name='send'),
    path('home/getMessages/<str:room>', views.getMessages, name='getMessages'),
    
    path('user/', views.user, name='user'),
    path('user/edituser/', views.edituser, name='edituser'),

    path('publicProfile/', views.publicProfile, name='publicProfile'),

    path('publicProfile/user_redirect/', views.user_redirect, name='user_redirect'),

    path('publicProfile/<slug:slug>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('publicProfile/<slug:slug>/success', views.ProfileDetailSuccess.as_view(), name="profile-detail-success"),
    path('user/friends/publicProfile/<slug:slug>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('user/friend_request/publicProfile/<slug:slug>/', views.ProfileDetail.as_view(), name='profile-detail'),


    path('publicProfile/<slug:slug>/study_buddy_app/send_friend_request/', views.send_friend_request,name='send friend request'),
    
    #path('user/friends/', views.viewFriends.as_view(), name='new_friends'),
    path('user/friends/', views.viewFriends, name='new_friends'),
    path('user/friends/remove_friend/<str:pk>/', views.remove_friend, name='remove_friend'),

    #path('user/friend_request/', views.viewRequest.as_view(), name='requests'),
    path('user/friend_request/', views.viewRequest, name='requests'),
    path('user/friend_request/delete_request/<str:pk>/', views.delete_request, name='delete_request'),

    path('user/friend_request/accept_friend_request/<str:pk>/', views.accept_friend_request, name='accept friend request'),


    path('user/deptlist/', views.addclass_deptlist, name="addclass_deptlist"),
    path('user/dept/<str:dept_name>/', views.dept, name="dept"),
    path('user/addclass', views.addclass, name="addclass"),
    path('user/deleteclass/', views.myclasses, name="myclasses"),
    path('user/dc', views.deleteclass, name="deleteclass"),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
]

