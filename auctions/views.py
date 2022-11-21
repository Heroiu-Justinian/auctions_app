from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Comment, User, Auction
from .forms import AuctionForm, BidForm, CommentForm



def index(request):
    listings = Auction.objects.all()
    context = {'listings' : listings}
    return render(request, "auctions/index.html", context)


@login_required(login_url='login')
def add_auction(request):
    if request.method == "POST":
        form = AuctionForm(request.POST,request.FILES)
        if form.is_valid():

            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data['image']

            auction = Auction(
                seller = User.objects.get(pk=request.user.id),
                title = title,
                description = description,
                category = category,
                image = image            ) 
            auction.save()
            return HttpResponseRedirect(reverse("index"))

    context = {
        'form' : AuctionForm()
    }
    return render(request,'auctions/add_auction.html',context)



def listing(request, pk):
    try:
        listing = Auction.objects.get(pk = pk)
    except Auction.DoesNotExist:
        return HttpResponse("The auction does no exist")


    if request.method == "POST":

        if 'place_bid' in request.POST:
            bid_form = BidForm(request.POST)
            print("FUUUUUUCK") 
            if bid_form.is_valid():
                auction = listing
                user = User.objects.get(pk=request.user.id)
                value = bid_form.cleaned_data['value']
                bid = Bid(
                    auction=auction,
                    user=user,
                    value=value,
                )
                bid.save()

        if 'post_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            
            if comment_form.is_valid():
                auction = listing
                user = User.objects.get(pk=request.user.id)
                body = comment_form.cleaned_data['body']
                comment = Comment(
                    auction=auction,
                    user=user,
                    body=body
                )
                comment.save()

    try:
        highest_bid = Bid.objects.select_related().filter(auction = pk).order_by('-value').first()
        comments = list(Comment.objects.filter(auction=pk).order_by('date'))
    except Bid.DoesNotExist:
        highest_bid = "No bids placed"
    except Comment.DoesNotExist:
        comments = "No comments posted yet"

    context = {
        'listing' : listing,
        'highest_bid' : highest_bid,
        'bid_form': BidForm(),
        'comment_form' : CommentForm(),
        'comments' : comments
    }
    



    return render(request,'auctions/listing.html', context)
    


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

