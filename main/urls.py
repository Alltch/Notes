from django.contrib import admin
from django.urls import path
from .views import (
    index, login_in, register, logout_user, note_detail, 
    delete_note, note_add, note_edit, other_posts, profile, 
    edit_profile, change_password, search_friends, send_friend_request,
    list_friends, accept_friend_request, reject_friend_request
)



urlpatterns = [
    path('', index, name='home'),
    path('other-posts/', other_posts, name='other-posts'),

    path('login/', login_in, name='login'),
    path('register', register, name='register'),
    path('logout/', logout_user, name='logout'),

    path('note/<int:note_id>/', note_detail, name='note-detail'),
    path('note/<int:note_id>/delete/', delete_note, name='note-delete'),
    path('note-add/', note_add, name='note-add'),
    path('note/<int:note_id>/edit/', note_edit, name='note-edit'),

    path('profile/<str:username>/', profile, name='profile'),
    path('profile/<str:username>/edit/', edit_profile, name='edit-profile'),
    path('profile/<str:username>/change-password/', change_password, name='change-password'),
    path('profile/<str:username>/send-request/', send_friend_request, name='send-friend-request'),
    path('profile/<str:username>/friends/', list_friends, name='list-friends'),
    path('friend-request/<int:request_id>/accept/', accept_friend_request, name='accept-friend-request'),
    path('friend-request/<int:request_id>/reject/', reject_friend_request, name='reject-friend-request'),

    path('search/friends/', search_friends, name='search-friends'),

]

