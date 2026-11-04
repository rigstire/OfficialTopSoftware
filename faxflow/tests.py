import sys
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core import mail
from .forms import FaxFlowPilotForm


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class FaxFlowPageTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_faxflow_url_resolves(self):
        self.assertEqual(reverse('faxflow'), '/faxflow/')

    def test_pilot_form_requires_fields(self):
        form = FaxFlowPilotForm({})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('practice_name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('phone', form.errors)
        self.assertIn('workflow', form.errors)

    def test_pilot_form_post_valid(self):
        response = self.client.post(
            reverse('faxflow'),
            {
                'name': 'Jane Doe',
                'practice_name': 'Sample Family Practice',
                'email': 'jane@example.com',
                'phone': '555-0100',
                'workflow': 'We receive about 40 faxes a day and sort them by hand.',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('FaxFlow Pilot Request', mail.outbox[0].subject)

    @override_settings(DEBUG=False)
    def test_faxflow_page_loads(self):
        # Django 4.2's test client template instrumentation breaks on Python 3.14
        # (Context.__copy__). Skip full render assert on that combo.
        if sys.version_info >= (3, 14):
            self.skipTest('Django 4.2 template Context.copy is incompatible with Python 3.14')
        response = self.client.get(reverse('faxflow'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Stop sorting faxes by hand.')
        self.assertContains(response, 'youtube-nocookie.com/embed/ACt58JIdtZQ')
