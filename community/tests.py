from datetime import datetime, timezone as dt_timezone

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Article


class CommunityTimeDisplayTests(TestCase):
    def test_article_created_at_uses_korean_time(self):
        User = get_user_model()
        user = User.objects.create_user(username='kst_user', password='pass12345!')
        article = Article.objects.create(user=user, content='KST check')
        Article.objects.filter(pk=article.pk).update(
            created_at=datetime(2026, 1, 1, 15, 30, tzinfo=dt_timezone.utc)
        )

        response = self.client.get(reverse('community:index'))

        self.assertContains(response, '2026.01.02')
        self.assertNotContains(response, '2026.01.01')
