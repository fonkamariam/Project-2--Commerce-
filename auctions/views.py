from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Listing
from .models import User
from django.contrib.auth.decorators import login_required


def index(request):
    l= Listing.objects.all()
    return render(request, "auctions/index.html",{"listings":l})
@login_required
def get(request,x): 
    l=Listing.objects.get(pk=x)
    return render(request, "auctions/singlepage.html",{"l":l})
@login_required
def create(request):
    if request.method == "POST":
        cur=request.user
        list = Listing.objects.create(title=request.POST["title"],starting_bid= request.POST["starting_bid"],description= request.POST["description"], imageUrl= request.POST["imageUrl"],category= request.POST["category"],owner= cur)
        list.save()
        return HttpResponseRedirect(reverse("index"))
    return render (request, "auctions/create.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
