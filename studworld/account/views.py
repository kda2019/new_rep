from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,  UserRegistrationForm, UserEditForm, ProfileEditForm, NewPost, EventUserForm

from .models import Profile, UserPost, EventUser


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Аутентификация успешна')
                else:
                    return HttpResponse('Аккаунт отключен')
            else:
                return HttpResponse('Неверный логин или пароль')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            # Создание профиля пользователя.
            Profile.objects.create(user=new_user).save()

            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def profile(request):
    if request.method == 'POST':
        my_post = NewPost(request.POST)
        my_post = my_post.save(commit=False)
        my_post.user = request.user
        my_post.save()
    M_posts = UserPost.objects.all().filter(user=request.user).order_by('-pk')
    M_profile = Profile.objects.get(user=request.user)
    return render(request, 'account/profile.html', {'section': 'profile', 'profile': M_profile, 'posts':  M_posts, 'post_form': NewPost()})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def post_delete(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(UserPost, pk=pk, user=request.user)
        post.delete()
        return redirect('/account')

@login_required
def new_user_event(request):
    if request.method == 'POST':
        my_event = EventUserForm(request.POST)
        if my_event.is_valid():
            my_event = my_event.save(commit=False)
            my_event.user = request.user
            my_event.save()