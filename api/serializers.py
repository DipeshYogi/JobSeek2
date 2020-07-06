from rest_framework import serializers

class RecommSerializer(serializers.Serializer):
    """ Get recommendations for a Profile"""
    n1 = serializers.IntegerField()


class GetConnSerializer(serializers.Serializer):
    """User Id to show jobs posted"""
    u1 = serializers.IntegerField()
