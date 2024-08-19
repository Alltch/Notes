from django.contrib import admin
from django.urls import path
from .views import index, login_in, register, logout_user, note_detail, delete_note, note_add, note_edit, other_posts, profile, edit_profile, change_password, friends_list, add_friend, search_friends, other_profile_view



urlpatterns = [
    path('other-posts/', other_posts, name='other-posts'),
    path('', index, name='home'),
    path('login/', login_in, name='login'),
    path('register', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('note/<int:note_id>/', note_detail, name='note-detail'),
    path('note/<int:note_id>/delete/', delete_note, name='note-delete'),
    path('note-add/', note_add, name='note-add'),
    path('note/<int:note_id>/edit/', note_edit, name='note-edit'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='profile-edit'),
    path('profile/change-password/', change_password, name='change-password'),
    path('friends/', friends_list, name='friends'),
    path('add-friend/', add_friend, name='add-friend'),
    path('search-friends/', search_friends, name='search_friends'),
    path('profile/<int:user_id>/', other_profile_view, name='other-profile'),
]

