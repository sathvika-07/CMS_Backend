from rest_framework import serializers


def ensure_primary_in_available(primary: str, available: list, field_name: str) -> None:
    """Ensure the primary value is present in the available list."""
    if primary and primary not in available:
        raise serializers.ValidationError({
            field_name: f"{field_name} must include the primary value.",
        })
