from django.contrib import admin
from .models import Book, BookSlug

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Book, BookAdmin)
admin.site.register(BookSlug)