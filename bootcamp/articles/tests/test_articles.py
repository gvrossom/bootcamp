from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from bootcamp.articles.models import Article, Tag
from django.contrib.auth.models import User

from bootcamp.articles.views import articles

class ArticleViewsTest(TestCase):

    def test_only_published_articles_are_shown(self):
        c = Client()
        user1 = User.objects.create_user(username="teste1234",
                                         email="reallynice@gmail.com",
                                         password="supersecret123")
                                         
        article1 = Article()
        article1.title = "nicetitle"
        article1.content = "nicecontent"
        article1.status = "P" # Published
        article1.create_user = user1
        article1.create_user.id = user1.id
        article1.save()
        
        article2 = Article()
        article2.title = "secondnicetitle"
        article2.content = "secondnicecontent"
        article2.status = "D" # Draft
        article2.create_user = user1
        article2.create_user.id = user1.id
        article2.save()
                                         
        # user1 logs in
        self.client.login(username="teste1234", password="supersecret123")
        
        response = self.client.get(reverse('articles'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('articles' in response.context)
        # make sure that the only (published) Article we have in our database is in that list 
        self.assertEqual([article.pk for article in response.context['articles']], [1])
        article_1 = response.context['articles'][0]
        self.assertEqual(article_1.title, 'nicetitle')
        
        
    def test_article_renders_template_and_slug(self):
        c = Client()
        user1 = User.objects.create_user(username="teste1234",
                                         email="reallynice@gmail.com",
                                         password="supersecret123")
                                         
        article1 = Article()
        article1.title = "nicetitle"
        article1.content = "nicecontent"
        article1.status = 'P'
        article1.slug = 'nice-title'
        article1.create_user = user1
        article1.create_user.id = user1.id
        article1.save()
        
        # user1 logs in
        self.client.login(username="teste1234", password="supersecret123")
        
        response = self.client.get(reverse('article', kwargs={'slug': 'nice-title'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article.html')
        # check we've passed the right article into the context
        self.assertEquals(response.context['article'], article1)

        # check the article's title appears on the page
        self.assertIn(article1.title, response.content)


    def test_validate_article_edition(self):
        c = Client()
        user1 = User.objects.create_user(username="teste1234",
                                         email="reallynice@gmail.com",
                                         password="supersecret123")
        user2 = User.objects.create_user(username="teste12345",
                                         email="reallynice2@gmail.com",
                                         password="supersecret123")

        article_1 = Article()
        article_1.title = "nicetitle"
        article_1.content = "nicecontent"
        article_1.create_user = user2
        article_1.create_user.id = user2.id
        article_1.save()
        
        # user1 logs in
        self.client.login(username="teste1234", password="supersecret123")
        # tries to get to edit article
        response = self.client.get(reverse('edit_article', kwargs={'id': '1'}))
        self.assertEqual(response.status_code, 302)
        # tries to post to edit article
        response = self.client.post(reverse('edit_article',
                                            kwargs={'id': '1'}))
        self.assertEqual(response.status_code, 302)
        
        # user2 logs in
        self.client.login(username="teste12345", password="supersecret123")
        # tries the get
        response = self.client.get(reverse('edit_article', kwargs={'id': '1'}), user=user2)
        self.assertEqual(response.status_code, 200)
        # tries the post
        response = self.client.post(reverse('edit_article',
                                            kwargs={'id': '1'}))
        self.assertEqual(response.status_code, 200)
