from django.core.urlresolvers import reverse

from misago.acl.testutils import override_acl
from misago.forums.models import Forum
from misago.users.testutils import AuthenticatedUserTestCase

from misago.threads.models import Thread, Event
from misago.threads.testutils import post_thread, reply_thread


class EventsViewTestCase(AuthenticatedUserTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def setUp(self):
        super(EventsViewTestCase, self).setUp()

        self.forum = Forum.objects.all_forums().filter(role="forum")[:1][0]
        self.forum.labels = []

        self.thread = post_thread(self.forum)

    def override_acl(self, new_acl):
        new_acl.update({
            'can_see': True,
            'can_browse': True,
            'can_see_all_threads': True,
            'can_see_own_threads': False,
            'can_pin_threads': True
        })

        forums_acl = self.user.acl
        forums_acl['visible_forums'].append(self.forum.pk)
        forums_acl['forums'][self.forum.pk] = new_acl
        override_acl(self.user, forums_acl)

    def test_hide_event(self):
        """its possible to hide event"""
        self.override_acl({'can_hide_events': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'pin'})
        self.assertEqual(response.status_code, 302)

        event = self.thread.event_set.all()[0]
        self.override_acl({'can_hide_events': 0})
        response = self.client.post(
            reverse('misago:edit_event', kwargs={'event_id': event.id}),
            data={'action': 'toggle'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 403)

        self.override_acl({'can_hide_events': 1})
        response = self.client.post(
            reverse('misago:edit_event', kwargs={'event_id': event.id}),
            data={'action': 'toggle'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        event = Event.objects.get(id=event.id)
        self.assertTrue(event.is_hidden)

    def test_show_event(self):
        """its possible to unhide event"""
        self.override_acl({'can_hide_events': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'pin'})
        self.assertEqual(response.status_code, 302)

        event = self.thread.event_set.all()[0]
        event.is_hidden = True
        event.save()

        self.override_acl({'can_hide_events': 0})
        response = self.client.post(
            reverse('misago:edit_event', kwargs={'event_id': event.id}),
            data={'action': 'toggle'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 403)

        self.override_acl({'can_hide_events': 1})
        response = self.client.post(
            reverse('misago:edit_event', kwargs={'event_id': event.id}),
            data={'action': 'toggle'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        event = Event.objects.get(id=event.id)
        self.assertFalse(event.is_hidden)

    def test_delete_event(self):
        """its possible to delete event"""
        self.override_acl({'can_hide_events': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'pin'})
        self.assertEqual(response.status_code, 302)

        self.override_acl({'can_hide_events': 0})
        response = self.client.post(self.thread.get_absolute_url(),
                                    data={'thread_action': 'unpin'})
        self.assertEqual(response.status_code, 302)

        event = self.thread.event_set.all()[0]

        self.override_acl({'can_hide_events': 0})
        response = self.client.post(
            reverse('misago:edit_event', kwargs={'event_id': event.id}),
            data={'action': 'delete'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 403)

        self.override_acl({'can_hide_events': 1})
        response = self.client.post(
            reverse('misago:edit_event', kwargs={'event_id': event.id}),
            data={'action': 'delete'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 403)

        self.override_acl({'can_hide_events': 2})
        response = self.client.post(
            reverse('misago:edit_event', kwargs={'event_id': event.id}),
            data={'action': 'delete'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertTrue(thread.has_events)
        self.assertTrue(thread.event_set.exists())

        event = self.thread.event_set.all()[0]
        self.override_acl({'can_hide_events': 2})
        response = self.client.post(
            reverse('misago:edit_event', kwargs={'event_id': event.id}),
            data={'action': 'delete'},
            **self.ajax_header)
        self.assertEqual(response.status_code, 200)

        thread = Thread.objects.get(id=self.thread.id)
        self.assertFalse(thread.has_events)
        self.assertFalse(thread.event_set.exists())
