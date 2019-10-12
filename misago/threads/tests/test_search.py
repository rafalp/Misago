from django.urls import reverse

from .. import test
from ...categories.models import Category
from ...users.test import AuthenticatedUserTestCase


def index_post(post):
    if post.id == post.thread.first_post_id:
        post.set_search_document(post.thread.title)
    else:
        post.set_search_document()
    post.save(update_fields=["search_document"])

    post.update_search_vector()
    post.save(update_fields=["search_vector"])


class SearchApiTests(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.category = Category.objects.get(slug="first-category")

        self.api_link = reverse("misago:api:search")

    def test_no_query(self):
        """api handles no search query"""
        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                self.assertEqual(provider["results"]["results"], [])

    def test_empty_query(self):
        """api handles empty search query"""
        response = self.client.get("%s?q=" % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                self.assertEqual(provider["results"]["results"], [])

    def test_short_query(self):
        """api handles short search query"""
        thread = test.post_thread(self.category)
        post = test.reply_thread(thread, message="Lorem ipsum dolor.")
        index_post(post)

        response = self.client.get("%s?q=ip" % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                self.assertEqual(provider["results"]["results"], [])

    def test_wrong_query(self):
        """api handles query miss"""
        thread = test.post_thread(self.category)
        post = test.reply_thread(thread, message="Lorem ipsum dolor.")
        index_post(post)

        response = self.client.get("%s?q=elit" % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                self.assertEqual(provider["results"]["results"], [])

    def test_hidden_post(self):
        """hidden posts are extempt from search"""
        thread = test.post_thread(self.category)
        post = test.reply_thread(thread, message="Lorem ipsum dolor.", is_hidden=True)
        index_post(post)

        response = self.client.get("%s?q=ipsum" % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                self.assertEqual(provider["results"]["results"], [])

    def test_unapproved_post(self):
        """unapproves posts are extempt from search"""
        thread = test.post_thread(self.category)
        post = test.reply_thread(
            thread, message="Lorem ipsum dolor.", is_unapproved=True
        )
        index_post(post)

        response = self.client.get("%s?q=ipsum" % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                self.assertEqual(provider["results"]["results"], [])

    def test_query(self):
        """api handles search query"""
        thread = test.post_thread(self.category)
        post = test.reply_thread(thread, message="Lorem ipsum dolor.")
        index_post(post)

        response = self.client.get("%s?q=ipsum" % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], post.id)

    def test_thread_title_search(self):
        """api searches threads by title"""
        thread = test.post_thread(self.category, title="Atmosphere of mars")
        index_post(thread.first_post)

        post = test.reply_thread(thread, message="Lorem ipsum dolor.")
        index_post(post)

        response = self.client.get("%s?q=mars atmosphere" % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], thread.first_post_id)

    def test_complex_query(self):
        """api handles complex query that uses fulltext search facilities"""
        thread = test.post_thread(self.category)
        post = test.reply_thread(thread, message="Atmosphere of Mars")
        index_post(post)

        response = self.client.get("%s?q=Mars atmosphere" % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], post.id)

    def test_filtered_query(self):
        """search filters are used by search system"""
        thread = test.post_thread(self.category)
        post = test.reply_thread(
            thread, message="You just do MMM in 4th minute and its pwnt"
        )

        index_post(post)

        response = self.client.get("%s?q=MMM" % self.api_link)
        self.assertEqual(response.status_code, 200)

        reponse_json = response.json()
        self.assertIn("threads", [p["id"] for p in reponse_json])

        for provider in reponse_json:
            if provider["id"] == "threads":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], post.id)

        response = self.client.get("%s?q=Marines Medics" % self.api_link)
        self.assertEqual(response.status_code, 200)

        for provider in reponse_json:
            if provider["id"] == "threads":
                results = provider["results"]["results"]
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["id"], post.id)


class SearchProviderApiTests(SearchApiTests):
    def setUp(self):
        super().setUp()

        self.api_link = reverse(
            "misago:api:search", kwargs={"search_provider": "threads"}
        )


def test_post_search_filters_hook_is_used_by_threads_search(
    db, user_client, mocker, thread
):
    def search_filter(search):
        return search.replace("apple phone", "iphone")

    mocker.patch(
        "misago.threads.filtersearch.hooks.post_search_filters", [search_filter]
    )

    post = test.reply_thread(thread, message="Lorem ipsum iphone dolor met.")
    index_post(post)

    response = user_client.get("/api/search/?q=apple phone")

    reponse_json = response.json()
    assert "threads" in [p["id"] for p in reponse_json]
    for provider in reponse_json:
        if provider["id"] == "threads":
            results = provider["results"]["results"]
            assert len(results) == 1
            assert results[0]["id"] == post.id
