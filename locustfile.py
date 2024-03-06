from locust import HttpUser, task


class User(HttpUser):
    host = 'http://127.0.0.1:8000'

    def on_start(self):
        self.client.headers = {'X-API-VERSION': '0.1.0'}

    @task
    def login(self):
        self.client.post(
            url='/api/auth/login/',
            data={'email': 'admin@gmail.com', 'password': '1234'},
        )
