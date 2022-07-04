def test_register(client, app):
    assert client.post(
        '/APIv1/auth/user-register',
        json={
            "name": "Volodymyr",
            "username": "vova",
            "email": "vova@mail.com",
            "password": "testpass",
        }
    ).json["message"] == 'User vova was created'

