from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Note


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
        is_private = request.POST.get('is_private') == 'on'  # Обработка чекбокса
        
        # Обновляем данные заметки
        note.title = title
        note.content = content
        note.is_private = is_private
        note.save()
        
        return redirect('note-detail', note_id=note_id)  # Редирект на главную или другую страницу после сохранения
    
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
            user = User.objects.get(username=username)
        except User.DoesNotExist:
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
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        # Создание нового пользователя
        user = User.objects.create_user(
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

        Note.objects.create(user=request.user, title=title, content=content, is_private=is_private)
        return redirect('home')

    return render(request, 'note_add.html')


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User

@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Update user information
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()

        messages.success(request, 'Your profile was successfully updated!')
        return redirect('profile')

    return render(request, 'edit_profile.html', {
        'user': request.user,
    })



@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Check if old password is correct
        if not request.user.check_password(old_password):
            messages.error(request, 'Your old password was entered incorrectly. Please try again.')
            return redirect('password_change')

        # Check if new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'The two new password fields didn’t match.')
            return redirect('password_change')

        # Update the password
        request.user.set_password(new_password1)
        request.user.save()

        # Keep the user logged in after changing the password
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Your password was successfully updated!')
        return redirect('profile')

    return render(request, 'password_change.html')
