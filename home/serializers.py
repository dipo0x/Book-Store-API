from rest_framework import serializers
from .models import Book
from accounts.models import Profile

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["name", "price", "text", "image"]

class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["price", "text"]
