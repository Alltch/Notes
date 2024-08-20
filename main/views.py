from .models import CustomUser, FriendRequest, Friend
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Note, CustomUser, FriendRequest, Friend



@login_required(login_url='login')
def index(request):
    all_notes = Note.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'notes': all_notes
    }
    return render(request, 'index.html', context=context)


@login_required(login_url='login')
def other_posts(request):
    all_notes = Note.objects.filter(is_private=False).order_by('-updated_at')

    context = {
        'notes': all_notes
    }

    return render(request, 'other_posts.html', context=context)


@login_required(login_url='login')
def note_edit(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == "POST":
        # Получаем данные из формы
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_private = request.POST.get(
            'is_private') == 'on'  # Обработка чекбокса

        # Обновляем данные заметки
        note.title = title
        note.content = content
        note.is_private = is_private
        note.save()

        # Редирект на главную или другую страницу после сохранения
        return redirect('note-detail', note_id=note_id)

    # Если GET-запрос, отображаем форму
    return render(request, 'note_edit.html', {'note': note})


def login_in(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('home')  # Перенаправление на главную страницу

    if request.method == 'POST':
        username = request.POST.get('username_html')
        password = request.POST.get('password_html')

        # Проверяем наличие username
        if not username:
            messages.error(request, 'Please enter your username.')
            return redirect('login')

        # Проверяем, существует ли пользователь с таким именем
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Username does not exist.')
            return redirect('login')

        # Проверяем наличие пароля
        if not password:
            messages.error(request, 'Please enter your password.')
            return redirect('login')

        # Проверка пароля
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Успешный вход
            login(request, user)
            # messages.success(request, f'Welcome, {username}! You have successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password. Please try again.')

    return render(request, 'login.html')


def register(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already registered and logged in.')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username_html')
        email = request.POST.get('email_html')
        first_name = request.POST.get('first_name_html')
        last_name = request.POST.get('last_name_html')
        password = request.POST.get('password_html')
        password2 = request.POST.get('password2_html')

        # Проверяем, что все поля заполнены
        if not all([username, email, first_name, last_name, password, password2]):
            messages.error(request, 'Please fill in all the fields.')
            return redirect('register')

        # Проверяем, что пароли совпадают
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Проверяем, существует ли пользователь с таким username или email
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        # Создание нового пользователя
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        # Аутентификация и вход пользователя
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, 'You have successfully registered and logged in.')
            return redirect('home')

    return render(request, 'register.html')


def logout_user(request):
    logout(request)
    # messages.success(request, 'You have successfully logged out.')
    return redirect('home')


@login_required(login_url='login')
def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    context = {
        'note': note
    }
    return render(request, 'note_detail.html', context=context)


@login_required(login_url='login')
def delete_note(request, note_id):
    try:
        note = get_object_or_404(Note, id=note_id, user=request.user)
        note.delete()

    except Note.DoesNotExist:
        pass

    return redirect('home')


@login_required(login_url='login')
def note_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_private = request.POST.get('is_private') == 'on'

        Note.objects.create(user=request.user, title=title,
                            content=content, is_private=is_private)
        return redirect('home')

    return render(request, 'note_add.html')


@login_required(login_url='login')
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    # Determine friend status
    is_friend = Friend.objects.filter(user=request.user, friend=user).exists()
    request_sent = FriendRequest.objects.filter(from_user=request.user, to_user=user, is_active=True).exists()
    request_received = FriendRequest.objects.filter(from_user=user, to_user=request.user, is_active=True).exists()

    context = {
        'user': user,
        'is_friend': is_friend,
        'request_sent': request_sent,
        'request_received': request_received
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def edit_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    # Проверка, что пользователь имеет право редактировать профиль
    if request.user != user:
        messages.error(
            request, 'You do not have permission to edit this profile.')
        return redirect('profile', username=user.username)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Update user information
        if first_name and last_name and email:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile', username=user.username)
        else:
            messages.error(request, 'Please fill out all fields.')

    return render(request, 'edit_profile.html', {'user': user})


@login_required(login_url='login')
def change_password(request, username):
    user = get_object_or_404(CustomUser, username=username)

    # Проверка, что текущий пользователь имеет право менять пароль
    if request.user != user:
        messages.error(
            request, 'You do not have permission to change this password.')
        return redirect('profile', username=user.username)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Проверка правильности старого пароля
        if not user.check_password(old_password):
            messages.error(
                request, 'Your old password was entered incorrectly. Please try again.')
            return redirect('change-password', username=user.username)

        # Проверка совпадения новых паролей
        if new_password1 != new_password2:
            messages.error(
                request, 'The two new password fields didn’t match.')
            return redirect('change-password', username=user.username)

        # Обновление пароля
        user.set_password(new_password1)
        user.save()

        # Оставляем пользователя залогиненным после смены пароля
        update_session_auth_hash(request, user)
        messages.success(request, 'Your password was successfully updated!')
        return redirect('profile', username=user.username)

    return render(request, 'password_change.html', {'user': user})


@login_required(login_url='login')
def search_friends(request):
    query = request.GET.get('q')

    if query:
        users = CustomUser.objects.filter(
            Q(username__icontains=query)).exclude(id=request.user.id)

    else:
        users = CustomUser.objects.none()

    context = {
        'users': users
    }
    return render(request, 'search_friends.html', context=context)


@login_required(login_url='login')
def send_friend_request(request, username):
    to_user = get_object_or_404(CustomUser, username=username)
    from_user = request.user

    if from_user != to_user:
        # Delete any previous inactive friend requests between these two users
        FriendRequest.objects.filter(
            from_user=from_user, to_user=to_user, is_active=False).delete()

        # Create a new friend request
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user)
        if created:
            messages.success(request, 'Friend request sent successfully!')
        else:
            messages.warning(request, 'Friend request already sent!')

    return redirect('profile', username=username)


@login_required(login_url='login')
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.to_user == request.user:
        friend_request.accept()
        messages.success(request, 'Friend request accepted!')

    return redirect('profile', username=friend_request.from_user.username)


@login_required(login_url='login')
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.to_user == request.user:
        friend_request.reject()
        messages.success(request, 'Friend request rejected!')

    return redirect('profile', username=friend_request.from_user.username)


@login_required(login_url='login')
def list_friends(request, username):
    user = get_object_or_404(CustomUser, username=username)
    friends = Friend.objects.filter(user=user)

    return render(request, 'list_friends.html', {'friends': friends, 'user': user})
