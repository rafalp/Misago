from rest_framework import serializers


def test_post_validator(context, data):
    title_match = 'casino' in data.get('title', '').lower()
    post_match = 'casino' in data.get('post', '').lower()

    if title_match or post_match:
        raise serializers.ValidationError("Don't discuss gambling!")
