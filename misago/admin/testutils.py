from django.core.urlresolvers import reverse


def admin_login(client, username, password):
    client.post(reverse('misago:admin:index'),
                data={'username': username, 'password': password})
