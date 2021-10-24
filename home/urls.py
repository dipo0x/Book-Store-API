from .import views
from django.urls import path

urlpatterns = [
    path('', views.homepage),
    path('home', views.home),
    path('add-book', views.add_book),
    path('books', views.books),
    path('book-details/<slug>', views.book_details),
    path('edit-book/<slug>', views.edit_book),
    path('delete-book/<slug>', views.delete_book),
    path('order-book/<slug>', views.order_book),
    path('webhook', views.webhook, name='webhook')
]
