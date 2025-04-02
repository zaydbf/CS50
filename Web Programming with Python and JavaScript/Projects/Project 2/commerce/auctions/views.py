from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User , Category, Listing, Comment, Bid

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user == listingData.owner
    return render(request, "auctions/listing.html", {
        "listing" : listingData,
        "isListingInWatchlist" : isListingInWatchlist,
        "allComments" : allComments,
        "isOwner" : isOwner
    })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.is_active = False
    listingData.save()
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user == listingData.owner
    return render(request, "auctions/listing.html", {
        "listing" : listingData,
        "isListingInWatchlist" : isListingInWatchlist,
        "allComments" : allComments,
        "isOwner" : isOwner,
        "update" : True,
        "message" : "Nice !! Your Auction is closed."
    })
    

def addBid(request,id):
    newBid = request.POST["newBid"]
    listingData = Listing.objects.get(pk=id)
    currentuser = request.user
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user == listingData.owner
    if float(newBid) > float(listingData.price.bid):
        updateBid = Bid(bid=newBid, user=currentuser)
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing" : listingData,
            "message" : "Bid updated Successfully",
            "update" : True,
            "isListingInWatchlist" : isListingInWatchlist,
            "isOwner" : isOwner,
            "allComments" : allComments
        })
    else: 
        return render(request, "auctions/listing.html", {
            "listing" : listingData,
            "message" : "Bid was not updated (current bid is higher than your bid) !! ",
            "update" : False,
            "isListingInWatchlist" : isListingInWatchlist,
            "isOwner" : isOwner,
            "allComments" : allComments
        })


def addComment(request, id):
    if request.method == "POST":
        currentuser = request.user
        listingData = Listing.objects.get(pk=id)
        message = request.POST["newComment"]
        newComment = Comment(
            author=currentuser,
            listing=listingData,
            message=message
        )
        newComment.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))
def addWatchlist(request, id):
    currentuser = request.user
    listingData = Listing.objects.get(pk=id)
    listingData.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def removeWatchlist(request, id):
    currentuser = request.user
    listingData = Listing.objects.get(pk=id)
    listingData.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def displayWatchlist(request):
    currentuser = request.user
    listings = currentuser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings" : listings
    })


def index(request):
    activeListings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings" : activeListings,
        "categories" : Category.objects.all()
    })


def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(is_active=True,category=category)
        return render(request, "auctions/index.html", {
            "listings" : activeListings,
            "categories" : Category.objects.all()
        })

def createListing(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories" : Category.objects.all()
        })
    else: 
        # Get data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        categoryName = request.POST["category"]
        # Who is the User
        currentUser = request.user
        # Get all content about the particular category
        category = Category.objects.get(categoryName=categoryName)
        # Create a new bid object
        bid = Bid(bid=float(price),
            user=currentUser       
        )
        bid.save()                                                                                                       
        # Create a new listing object
        newListing = Listing(title = title,
            description=description, 
            image_url=imageurl, 
            price=bid,
            owner=currentUser,
            category=category
            )
        # insert the object in db
        newListing.save()
        # redirect to index page
        return HttpResponseRedirect(reverse("index"))


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
