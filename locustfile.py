from locust import HttpUser, task, between
import random


class ElectionUser(HttpUser):

    wait_time = between(1, 3)

    constituency_ids = list(range(1, 157))

    news_ids = list(range(1, 51))

    @task(40)
    def home_page(self):

        self.client.get(
            "/"
        )

    @task(20)
    def constituencies_page(self):

        self.client.get(
            "/constituencies/"
        )

    @task(15)
    def constituency_detail(self):

        constituency_id = random.choice(
            self.constituency_ids
        )

        self.client.get(
            f"/constituency/{constituency_id}/"
        )

    @task(10)
    def news_list(self):

        self.client.get(
            "/news/"
        )

    @task(10)
    def news_detail(self):

        news_id = random.choice(
            self.news_ids
        )

        self.client.get(
            f"/news/{news_id}/"
        )

    @task(3)
    def react_to_news(self):

        news_id = random.choice(
            self.news_ids
        )

        reaction = random.choice(
            [
                "like",
                "love",
                "wow"
            ]
        )

        self.client.post(
            f"/news/{news_id}/",
            data={
                "reaction_type": reaction
            }
        )

    @task(2)
    def comment_on_news(self):

        news_id = random.choice(
            self.news_ids
        )

        self.client.post(
            f"/news/{news_id}/",
            data={
                "name": "Locust User",
                "content": "Election monitoring stress test."
            }
        )
