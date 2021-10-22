from django.shortcuts import redirect
from django.contrib.auth import logout, login, authenticate
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import api_view
from home.models import Book
from home.serializers import BookSerializer
from accounts.serializers import UserSerializer, ProfileSerializer
from .models import Profile
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# Create your views here.
@api_view(['GET'])
def profile(request):
    user = request.user
    #To get the books of the logged in user
    if request.user.is_authenticated:
        check_user = User.objects.filter(Q(username=user))
        check_profile = Profile.objects.filter(Q(username=user))
        filter_books = Book.objects.filter(Q(user=user)).order_by('-date_added')
        the_user = UserSerializer(check_user, many=True)
        the_profile = ProfileSerializer(check_profile, many=True)
        the_books = BookSerializer(filter_books, many=True)
        response = the_user.data, the_profile.data, the_books.data
        return Response(response)
    else:
        return redirect("/login")

@api_view(['GET','POST'])
def register(request):
    if request.method == "POST":
        #Getting the data of the user
        username = request.data.get("username")
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        your_country = request.data.get("country")
        check_user = User.objects.filter(Q(username=username))
        if check_user.exists():
            return Response({"That username is taken"})
        else:
            user = User.objects.create(username=username, password = password, email=email)
            user.set_password(password)
            user.save()
            log_user_in = authenticate(username=username, password=password)
            login(request, log_user_in)
            #Getting the new user id to attach it to his/her profile
            check_stuff = User.objects.get(username=username)
            Profile.objects.create(username=check_stuff, name=name, country=your_country)
            return redirect("/profile")
    else:
        return Response({"Page":"Registration Page"})

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

def logout_user(request):
    logout(request)
    return redirect("/login")