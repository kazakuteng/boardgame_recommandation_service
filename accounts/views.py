import re

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from community.models import Article
from games.models import BoardGames, RecommendationFeedback
from .forms import AccountUpdateForm, CustomAuthenticationForm, CustomUserCreationForm, ProfileUpdateForm


def _normalize_game_title(value):
    return re.sub(r'[\W_]+', '', str(value or '')).casefold()


def _tag_search_terms(tag):
    return [
        term
        for term in re.split(r'[\s:：\-–—_/]+', str(tag or ''))
        if len(term.strip()) >= 2
    ]


def _find_favorite_game_for_tag(tag):
    normalized_tag = _normalize_game_title(tag)
    if not normalized_tag:
        return None

    exact_match = (
        BoardGames.objects
        .filter(Q(title__iexact=tag) | Q(korean_title__iexact=tag))
        .order_by('rank')
        .first()
    )
    if exact_match:
        return exact_match

    query = Q(title__icontains=tag) | Q(korean_title__icontains=tag)
    for term in _tag_search_terms(tag):
        query |= Q(title__icontains=term) | Q(korean_title__icontains=term)

    candidates = BoardGames.objects.filter(query).order_by('rank')[:50]
    best_partial = None
    for game in candidates:
        title_key = _normalize_game_title(game.title)
        korean_key = _normalize_game_title(game.korean_title)
        if normalized_tag in {title_key, korean_key}:
            return game
        if (
            normalized_tag
            and not best_partial
            and (
                normalized_tag in title_key
                or normalized_tag in korean_key
                or title_key in normalized_tag
                or korean_key in normalized_tag
            )
        ):
            best_partial = game
    return best_partial


def _favorite_game_cards(user):
    cards = []
    for tag in user.favorite_game_tag_list:
        game = _find_favorite_game_for_tag(tag)
        cards.append({
            'tag': tag,
            'game': game,
            'display_title': (game.korean_title or game.title) if game else tag,
            'image_url': (game.thumbnail_url or game.image_url) if game else '',
        })
    return cards

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
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
    articles = Article.objects.filter(user=person).order_by('-created_at')
    recommendation_feedbacks = RecommendationFeedback.objects.filter(user=person).order_by('-created_at')
    context = {
        'person': person,
        'articles': articles,
        'recommendation_feedbacks': recommendation_feedbacks,
        'favorite_game_cards': _favorite_game_cards(person),
        'is_owner': request.user.is_authenticated and request.user == person,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.pk)
    else:
        form = ProfileUpdateForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/profile_edit.html', context)

@login_required
def account_settings(request):
    account_form = AccountUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    delete_error = ''

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'account':
            account_form = AccountUpdateForm(request.POST, instance=request.user)
            if account_form.is_valid():
                account_form.save()
                return redirect('accounts:account_settings')

        elif action == 'password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('accounts:account_settings')

        elif action == 'delete':
            if request.POST.get('delete_confirm') == request.user.username:
                user = request.user
                auth_logout(request)
                user.delete()
                return redirect('index')
            delete_error = '회원탈퇴를 하려면 아이디를 정확히 입력해주세요.'

    context = {
        'account_form': account_form,
        'password_form': password_form,
        'delete_error': delete_error,
    }
    return render(request, 'accounts/account_settings.html', context)

@ensure_csrf_cookie
def current_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({'is_authenticated': False})

    return JsonResponse({
        'is_authenticated': True,
        'username': request.user.username,
        'profile_url': f'/accounts/{request.user.pk}/profile/',
    })

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

@require_POST
@login_required
def upload_profile_image(request):
    if 'profile_image' in request.FILES:
        request.user.profile_image = request.FILES['profile_image']
        request.user.save(update_fields=['profile_image'])
        return JsonResponse({'success': True, 'url': request.user.profile_image.url})
    return JsonResponse({'success': False, 'error': 'No image provided'}, status=400)
