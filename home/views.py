from re import template
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookSerializer, BookUpdateSerializer
from .models import Book, BookSlug
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import random, requests, math, environ
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from fpdf import FPDF
import requests, mimetypes
from django.http.response import HttpResponse
from pathlib import Path

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()
 
# Create your views here.
@api_view(['GET', 'POST'])
def home(request):
    i = Book.objects.all().order_by('-date_added')[:1]
    the_books = BookSerializer(i, many=True)
    template_name = "payment.html"
    return render({'data' : the_books.data}, template_name)

@api_view(['GET'])
def books(request):
        book = Book.objects.all()
        the_books = BookSerializer(book, many=True)
        return Response(the_books.data)

@api_view(['POST', 'GET'])
def add_book(request):
    permission_classes = (IsAuthenticated)
    if request.method == "POST":
        user= request.user
        name = request.data.get("name")
        price = request.data.get("price")
        text = request.data.get("text")
        image = request.data.get("image")
        slug = str(random.randint(1, 99999))[:16]
        book_name = Book.objects.filter(Q(name=name))
        #To check if the user is logged in
        user = User.objects.filter(Q(username=user))
        if user.exists():
            #To check if that book already exist
            if book_name.exists():
                response = {
                "Book with that name already exist"
                }
                return Response(response)
            save = Book.objects.get_or_create(user=request.user, name=name, price=price, text=text, slug=" '' "+ slug, slug2 = slug, image=image)
            return redirect("book-details"+"/"+slug)     
        else:
            response = {
            "Login to add a book"
                }
            return Response(response)
    else:
        response = {
            "Add new book"
        }
        return Response(response)

@api_view(['GET'])
def book_details(request, slug):
    book_name = Book.objects.get(slug=slug)
    the_books = BookSerializer(book_name)
    return Response(the_books.data)

@api_view(['GET', 'PATCH'])
def edit_book(request, slug):
    if request.method == "PATCH":
            if request.user == Book.objects.get(Q(slug=slug)).user:
                book = Book.objects.get(Q(user = request.user.id, slug=slug))
                the_books = BookUpdateSerializer(book, data=request.data)
                if the_books.is_valid():
                    the_books.save()
                    return Response(the_books.data)
            else:
                return redirect("/profile")
    else:
        if request.user.is_authenticated:
            if request.user == Book.objects.get(Q(slug=slug)).user:
                book = Book.objects.get(Q(user = request.user.id, slug=slug))
                the_books = BookUpdateSerializer(book)
                return Response(the_books.data)
            return redirect("/profile")
        return Response("Log in to make an attempt to edit this post")
        
@api_view(['GET'])
@login_required
def delete_book(request, slug):
    if request.user == Book.objects.get(Q(slug=slug)).user:
        book = Book.objects.get(user=request.user.id, slug=slug)
        book.delete()
        return redirect("/profile")
    return redirect("/")

@api_view(['POST', 'GET'])
@login_required
def order_book(request, slug):
    book = Book.objects.get(slug=slug)
    name = request.user.profile.name
    email = request.user.email
    amount = book.price
    title= book.name

    #Saving the book the folk is paying for
    s = BookSlug.objects.get(user=request.user)
    s.delete()
    iew = BookSlug.objects.create(
                    user=request.user,
                    slug=slug,
               )
    iew.save()
    #EVERYTHING FLUTTERWAVE AND PAYMENT
    auth_token= env('SECRET_KEY')
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
        "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
        "amount":amount,
        "currency":"NGN",
        "redirect_url":"https://b271-102-89-0-58.ngrok.io/webhook",
        "payment_options":"card",
        "meta":{
            "consumer_id":request.user.id,
            "consumer_mac":"92a3-912ba-1192a"
        },
        "customer":{
            "email":email,
            "name":name,
        },
        "customizations":{
            "title":"Yre Paying N" + str(amount) + " " + "for" + " " + title,
            "logo":"https://avatars.githubusercontent.com/u/63419117?v=4"
        }
        }
    url = 'https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    link=response['data']['link']   
    return render(request,'payment.html', {'link':link})

@csrf_exempt
@api_view(["GET", "POST"])
def webhook(request):
    if request.method == "POST":
        request_json = request.body.decode("UTF-8")#converting webhook from byte to string
        
        #Without the post method, the get method wont work so leave it
    else:
        stuff = BookSlug.objects.get(Q(user=request.user.id)).slug
        code = Book.objects.get(Q(slug=str(stuff))).name
        codeName = Book.objects.get(Q(slug=str(stuff))).text

        #Everthing about converting the book name and text to pdf
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        pdf.cell(200, 10, txt = code,
                ln = 1, align = 'C')
        pdf.cell(200, 10, txt = codeName,
                ln = 2, align = 'C')
        pdf.output("pdfs/" + code + ".pdf")

        #Everthing about downloading the pdf
        BASE_DIR = Path(__file__).resolve().parent.parent
        filepath = str(BASE_DIR) + '/pdfs/' + code + '.pdf'
        path = open(filepath, 'rb')
        mime_type, _ = mimetypes.guess_type(filepath)
        filename = code
        response = HttpResponse(path, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename + ".pdf"
        return response
    return HttpResponse("")
    #Why I used two methods is that the endpoint redirect views the redirect page twice and drops the webhook only the first time
    #so we have to create a post medthhod which will trigger the get response. This wont work if a webhook is not sent so as
    #to give response the second time
