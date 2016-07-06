from django.test import TestCase

from misago.core import serializer


class SerializerTests(TestCase):
    def test_serializer(self):
        """serializer dehydrates and hydrates values of different types"""
        TEST_CASES = (
            'LoremIpsum', 123, [1, 2, '4d'], {'bawww': 'zong', 23: True}
        )

        for wet in TEST_CASES:
            dry = serializer.dumps(wet)
            self.assertFalse(dry.endswith('='))
            self.assertEqual(wet, serializer.loads(dry))

    def test_serializer_handles_paddings(self):
        """serializer handles missing paddings"""
        for i in xrange(100):
            wet = 'Lorem ipsum %s' % ('a' * i)
            dry = serializer.dumps(wet)
            self.assertFalse(dry.endswith('='))
            self.assertEqual(wet, serializer.loads(dry))
