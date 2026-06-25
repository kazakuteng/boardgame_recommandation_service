import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from games.models import BoardGames

from .forms import ProfileUpdateForm


class FollowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='follower', password='pass12345!')
        self.person = User.objects.create_user(username='target', password='pass12345!')

    def test_follow_requires_login(self):
        response = self.client.post(reverse('accounts:follow', args=[self.person.pk]))

        self.assertEqual(response.status_code, 302)

    def test_follow_toggle(self):
        self.client.login(username='follower', password='pass12345!')

        follow_response = self.client.post(reverse('accounts:follow', args=[self.person.pk]))
        self.assertEqual(follow_response.status_code, 200)
        self.assertEqual(follow_response.json()['is_followed'], True)
        self.assertTrue(self.user.followings.filter(pk=self.person.pk).exists())
        self.assertTrue(self.person.followers.filter(pk=self.user.pk).exists())

        unfollow_response = self.client.post(reverse('accounts:follow', args=[self.person.pk]))
        self.assertEqual(unfollow_response.status_code, 200)
        self.assertEqual(unfollow_response.json()['is_followed'], False)
        self.assertFalse(self.user.followings.filter(pk=self.person.pk).exists())

    def test_cannot_follow_self(self):
        self.client.login(username='follower', password='pass12345!')

        response = self.client.post(reverse('accounts:follow', args=[self.user.pk]))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'You cannot follow yourself.')

    def test_profile_renders_follow_script(self):
        self.client.login(username='follower', password='pass12345!')

        response = self.client.get(reverse('accounts:profile', args=[self.person.pk]))

        self.assertContains(response, 'id="followForm"')
        self.assertContains(response, 'fetch(`/accounts/${userId}/follow/`')


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ProfileCustomizationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='profile_user', password='pass12345!')

    def test_favorite_game_tags_preserve_spaces(self):
        form = ProfileUpdateForm(data={
            'favorite_game_tags': '#Ark Nova #Brass: Birmingham, Azul',
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data['favorite_game_tags'],
            'Ark Nova,Brass: Birmingham,Azul',
        )

    def test_profile_renders_favorite_game_images_from_tags(self):
        BoardGames.objects.create(
            game_id=342942,
            title='Ark Nova',
            korean_title='아크 노바',
            rank=4,
            released_year=2021,
            thumbnail_url='https://example.com/ark.jpg',
        )
        BoardGames.objects.create(
            game_id=224517,
            title='Brass: Birmingham',
            korean_title='브라스: 버밍엄',
            rank=1,
            released_year=2018,
            thumbnail_url='https://example.com/brass.jpg',
        )
        self.user.favorite_game_tags = 'Ark Nova,브라스 버밍엄'
        self.user.save(update_fields=['favorite_game_tags'])

        response = self.client.get(reverse('accounts:profile', args=[self.user.pk]))

        self.assertContains(response, 'https://example.com/ark.jpg')
        self.assertContains(response, 'https://example.com/brass.jpg')
        self.assertContains(response, '#Ark Nova')
        self.assertContains(response, '#브라스 버밍엄')

    def test_profile_image_upload_renders_media_url(self):
        self.client.login(username='profile_user', password='pass12345!')
        image = SimpleUploadedFile(
            'avatar.png',
            b'\x89PNG\r\n\x1a\n',
            content_type='image/png',
        )

        response = self.client.post(
            reverse('accounts:profile_edit'),
            {'favorite_game_tags': '', 'profile_image': image},
        )
        self.assertEqual(response.status_code, 302)

        profile_response = self.client.get(reverse('accounts:profile', args=[self.user.pk]))

        self.assertContains(profile_response, '/media/profiles/')
        self.assertContains(profile_response, 'profile image')
