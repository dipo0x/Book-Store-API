from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["name", "price", "text", "image"]

class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["name", "price", "text"]

class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["image"]