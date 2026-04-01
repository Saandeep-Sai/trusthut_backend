from rest_framework import serializers
from apps.core.config import ACCESSIBILITY_TYPES, RISK_LEVELS, POST_TYPES, RISK_CATEGORIES


class PostCreateSerializer(serializers.Serializer):
    """Validates post creation data."""
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=2000)
    location_name = serializers.CharField(max_length=300)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    accessibility_type = serializers.ChoiceField(choices=ACCESSIBILITY_TYPES)
    risk_level = serializers.ChoiceField(choices=RISK_LEVELS)
    media_url = serializers.CharField(required=False, allow_blank=True)
    media_type = serializers.ChoiceField(
        choices=[('image', 'Image'), ('video', 'Video')],
        required=False, default='image'
    )
    # Highway safety fields (optional — backward compatible)
    post_type = serializers.ChoiceField(choices=['place', 'highway'], required=False, default='place')
    risk_category = serializers.ChoiceField(choices=RISK_CATEGORIES, required=False, allow_blank=True)
    route_name = serializers.CharField(max_length=300, required=False, allow_blank=True)


class PostUpdateSerializer(serializers.Serializer):
    """Validates post update data — all fields optional."""
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(max_length=2000, required=False)
    location_name = serializers.CharField(max_length=300, required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    accessibility_type = serializers.ChoiceField(choices=ACCESSIBILITY_TYPES, required=False)
    risk_level = serializers.ChoiceField(choices=RISK_LEVELS, required=False)
    media_url = serializers.CharField(required=False, allow_blank=True)
    media_type = serializers.ChoiceField(
        choices=[('image', 'Image'), ('video', 'Video')],
        required=False
    )
    post_type = serializers.ChoiceField(choices=POST_TYPES, required=False)
    risk_category = serializers.ChoiceField(choices=RISK_CATEGORIES, required=False, allow_blank=True)
    route_name = serializers.CharField(max_length=300, required=False, allow_blank=True)
