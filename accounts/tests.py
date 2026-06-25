from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
