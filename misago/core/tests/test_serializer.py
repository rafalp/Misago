from django.test import TestCase
from misago.core import serializer


class SerializerTests(TestCase):
    def test_serializer(self):
        """serializer dehydrates and hydrates values"""
        TEST_CASES = (
            'LoremIpsum', 123, [1, 2, '4d'], {'bawww': 'zong', 23: True}
        )

        for wet in TEST_CASES:
            dry = serializer.dumps(wet)
            self.assertEqual(wet, serializer.loads(dry))
