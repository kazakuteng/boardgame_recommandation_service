from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('index')

def profile(request, user_pk):
    User = get_user_model()
    person = get_object_or_404(User, pk=user_pk)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)

@require_POST
@login_required
def follow(request, user_pk):
    User = get_user_model()
    person = get_object_or_404(User, pk=user_pk)
    
    if person != request.user:
        if request.user in person.followers.all():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followers_count': person.followers.count(),
            'followings_count': person.followings.count(),
        }
        return JsonResponse(context)
    return JsonResponse({'error': 'You cannot follow yourself.'}, status=400)
