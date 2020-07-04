from rest_framework import serializers

class recomm_serializer(serializers.Serializer):
    """ Get recommendations for a Profile"""
    n1 = serializers.IntegerField()
