from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Listing,Watchlist,Comment,Bid
from .models import User
from django.contrib.auth.decorators import login_required


def index(request):
    l= Listing.objects.all()
    return render(request, "auctions/index.html",{"listings":l})
@login_required
def get(request,x): 
    B=Bid.objects.all()
    list_for_watchlist=[]
    l=Listing.objects.get(pk=x)
    C= Comment.objects.all()
    list_for_comments=[]
    list_for_bids=[]
    dic={}
    if request.method == "POST":
        # for comments
        curr=request.user
        wanted_auction= request.POST["auc"]
        want=Listing.objects.get(pk= wanted_auction)
        comment_from_form=request.POST["com"]
        listt= Comment.objects.create(person= curr, comment = comment_from_form,auction= want)
        listt.save()
        for y in C:
            if y.auction.id == x:
                list_for_comments.append(y)
        try:
            wanted_watchlist=Watchlist.objects.get(own=curr)
        except Watchlist.DoesNotExist:
            wanted_watchlist= Watchlist.objects.create(own=curr)    
            wanted_watchlist.save()     
        fonka=wanted_watchlist.oneauction.iterator()
        for f in fonka:
            list_for_watchlist.append(f.id)
        message="add"
        if x in list_for_watchlist:
            message="remove"
        return render(request, "auctions/singlepage.html",{"Comments":list_for_comments,"l":l,"message_for_watchlist":message})
    if request.method == "GET":
        curr=request.user
        # Fetching all comments
        for y in C:
            if y.auction.id == x:
                list_for_comments.append(y)
        try:
            wanted_watchlist=Watchlist.objects.get(own=curr)
        except Watchlist.DoesNotExist:
            wanted_watchlist= Watchlist.objects.create(own=curr)    
            wanted_watchlist.save()     
        fonka=wanted_watchlist.oneauction.iterator()
        for f in fonka:
            list_for_watchlist.append(f.id)
        message="add"
        if x in list_for_watchlist:
            message="remove"
        for b in B:
            if b.auctionbided.id==x:
                list_for_bids.append(b)
        if list_for_bids:
            for z in list_for_bids:
                dic.update({z.bidder: z.bid})
            Highest_bidder=max(dic, key= lambda x:dic[x])
            Highest_bid= dic[Highest_bidder]
            min_bid_to_be_placed= Highest_bid + 1
            return render(request,"auctions/singlepage.html",{"min_value":min_bid_to_be_placed,"highest_bidder":Highest_bidder,"highest_bid":Highest_bid,"message":message,"l":l,"message_for_watchlist":message,"Comments":list_for_comments})
        Highest_bid= l.starting_bid
        return render(request,"auctions/singlepage.html",{"highest_bid":Highest_bid,"message":message,"l":l,"message_for_watchlist":message,"Comments":list_for_comments})

       
@login_required
def create(request):
    if request.method == "POST":
        cur=request.user
        list = Listing.objects.create(title=request.POST["title"],starting_bid= request.POST["starting_bid"],description= request.POST["description"], imageUrl= request.POST["imageUrl"],category= request.POST["category"],owner= cur)
        list.save()
        return HttpResponseRedirect(reverse("index"))
    return render (request, "auctions/create.html")

@login_required
def show_watchlist(request):
    curr=request.user
    try:
        wanted_watchlist=Watchlist.objects.get(own=curr)
    except Watchlist.DoesNotExist:
        wanted_watchlist= Watchlist.objects.create(own=curr)    
        wanted_watchlist.save()
    message="No Auction Added Yet."
    return render (request, "auctions/watchlist.html",{"watchlist":wanted_watchlist.oneauction.all,"message":message})
@login_required
def add_to_watchlist(request):
    curr=request.user 
    if request.method == "POST":
        auc_id= request.POST["auc"]
        wanted_auciton=Listing.objects.get(pk= auc_id)
        try:
            wanted_watchlist=Watchlist.objects.get(own=curr)
            wanted_watchlist.oneauction.add(wanted_auciton)
        except Watchlist.DoesNotExist:
            NWL= Watchlist.objects.create(own=curr)    
            NWL.oneauction.add(wanted_auciton)
            NWL.save()
        return HttpResponseRedirect(reverse("get",kwargs={"x":wanted_auciton.id}))   
@login_required
def remove_from_watchlist(request):
    curr=request.user 
    if request.method == "POST":
        auc_id= request.POST["auc"]
        wanted_auciton=Listing.objects.get(pk= auc_id)    
        wanted_watchlist=Watchlist.objects.get(own=curr)
        wanted_watchlist.oneauction.remove(wanted_auciton)
    return HttpResponseRedirect(reverse("get",kwargs={"x":wanted_auciton.id}))
def categories(request):
    l=Listing.objects.all()
    s = set()
    for x in l:
        s.add(x.category)
    return render(request,"auctions/category.html",{"categories": s})
def get_by_category(request, category):
    l=Listing.objects.all()
    a=[]
    for x in l:
        if x.category == category:
            a.append(x.title)
    return render(request,"auctions/categorylist.html",{"categories": a})
def add_bid(request): 
    if request.method == "POST":
        curr=request.user
        w= request.POST["auc"]
        wanted_auciton=Listing.objects.get(pk= w)
        create_bid= Bid.objects.create(bidder=curr,bid=request.POST["bid"],auctionbided=wanted_auciton)
        create_bid.save()
    return HttpResponseRedirect(reverse("get",kwargs={"x":wanted_auciton.id}))    
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
