from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Category, Bidder

from datetime import datetime



class NewListingForm(forms.Form):

    image_upload = forms.ImageField(label="Image: ")
    name_input = forms.CharField(label="Listing Name: ", widget=forms.TextInput(attrs={"placeholder":"Type in the listing name here."}))
    desc_input = forms.CharField(label="Listing Desc: ", widget=forms.Textarea(attrs={"placeholder":"Type in the listing description here."}))
    bid_input = forms.FloatField(label="Starting Bid: ")
    cate_select = forms.ChoiceField(label="Category: ", choices=tuple((cate.id, cate.category) for cate in Category.objects.all()))


    def __init__(self, *args, **kwargs):

        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['name_input'].initial = ""
        self.fields['desc_input'].initial = ""
        self.fields['bid_input'].initial = 0



def index(request):

    listings_active = Listing.objects.filter(is_active=True)
    listings_inactive = Listing.objects.filter(is_active=False)

    return render(request, "auctions/index.html", {
        "active_items": listings_active,
        "inactive_items": listings_inactive
    })


def category(request):
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all()
    })


def category_listing(request, cate_id):

    cate_listing = Listing.objects.filter(item_category_id=cate_id)

    return render(request, "auctions/category_listing.html", {
        "cate_listing": cate_listing,
        "cate_title": cate_listing.first().item_category
    })


def create_listing(request):

    if_user_login(request)

    if request.method == "POST":
        
        form = NewListingForm(request.POST, request.FILES)
        # print(form)

        if form.is_valid():
            name = form.cleaned_data["name_input"]
            desc = form.cleaned_data["desc_input"]
            bid = form.cleaned_data["bid_input"]
            cate = Category.objects.get(pk=form.cleaned_data["cate_select"])
            img = form.cleaned_data["image_upload"]

            # print(name, desc, type(bid), type(cate), type(img))
            new_listing = Listing(item_name=name, item_desc=desc, starting_bid=bid, item_category=cate, item_image=img)
            new_listing.save()

        return HttpResponseRedirect(reverse("index"))

    else:   
        form = NewListingForm()

        return render(request, "auctions/create_listing.html", {
            "form": form
        })


def detail(request, item_name):

    listing_item = Listing.objects.get(item_name=item_name)
    bidder_obj = Bidder.objects.filter(bidder_item=listing_item.id)

    # By default, both values below are False until they got validated.
    is_creater = False
    any_bidder = False

    # Validates the identity of the request user.
    if listing_item.item_creater_id == request.user.id:
        is_creater = True

    # Validates if any bidder exists.
    if bidder_obj.exists():

        last_bidder = bidder_obj.latest('bid_time').bidder_name
        any_bidder = True

        return render(request, "auctions/listing_detail.html", {
            "item": listing_item,
            "last_bidder": last_bidder,
            "is_creater": is_creater,
            "any_bidder": any_bidder
        })

    else:

        return render(request, "auctions/listing_detail.html", {
            "item": listing_item,
            "is_creater": is_creater,
            "any_bidder": any_bidder
        })


def watchlist(request):

    if_user_login(request)

    user_watchlist = (User.objects.get(id=request.user.id)).favorites.all()

    return render(request, "auctions/watchlist.html", {
        "user_name": request.user,
        "user_watchlist": user_watchlist
    })


def add_2_watchlist(request, item_id):

    if_user_login(request)

    # Get the listing info whose watchlist gonna get updated.
    listing_info = Listing.objects.get(pk=item_id)

    # Get the users ID in this listing's watchlist
    watchlist_users = [user.id for user in listing_info.watchlist.all()]

    # Get the user info who is gonna add an item.
    req_user_id = request.user.id
    user_info = User.objects.get(pk=req_user_id)


    if req_user_id not in watchlist_users:

        # Do the adding of the watchlist
        listing_info.watchlist.add(user_info)

        messages.info(request, "This item has been added to your watchlist.")
        messages.info(request, "You can cancel it by clicking the icon once more.")

    else:

        # Do the removing from the watchlist
        listing_info.watchlist.remove(user_info)        

        messages.info(request, "This item has been removed from your watchlist.")
        messages.info(request, "You can add it by clicking the icon once more.")


    return HttpResponseRedirect(reverse("detail", kwargs={"item_name":listing_info.item_name}))


def bid_update(request, item_id):

    # Get the listing info whose watchlist gonna get updated.
    listing_info = Listing.objects.get(pk=item_id)

    # Get the user info who is gonna add an item.
    req_user_id = request.user.id
    user_info = User.objects.get(pk=req_user_id)

    if request.method == "POST":
        
        # Update the bidding value and bidding count
        listing_info.bid_count += 1
        listing_info.starting_bid = float(request.POST["bid"])
        listing_info.save()
        messages.info(request, "Your bid has been placed.")

        # Update the Bidder Class
        bidder_info = Bidder(bidder_item=listing_info, bid_count=listing_info.bid_count, bidder_name=user_info, bid_time=datetime.now())
        bidder_info.save()

    return HttpResponseRedirect(reverse("detail", kwargs={"item_name":listing_info.item_name}))


def close_bid(request, item_id):

    # Get the listing info which will be closed.
    listing_info = Listing.objects.get(pk=item_id)

    # Get the user info who is gonna close the bid (The Creater).
    req_user_id = request.user.id
    user_info = User.objects.get(pk=req_user_id)

    # Make sure the one who closes the bid must be the item creater.
    assert listing_info.item_creater_id == req_user_id, "You're not allowed to be here, BACK OFF!!!"
    print('the creater ID & req user ID: ', listing_info.item_creater_id, req_user_id)

    # Update the is_active status of the closing bid.
    listing_info.is_active = False
    listing_info.save()

    # Show who is the bid winner.
    bid_winner = Bidder.objects.filter(bidder_item=item_id).latest('bid_time').bidder_name

    messages.info(request, "You've successfully closed this deal. Congratulations!")
    messages.info(request, "The Highest Bidder is {}".format(bid_winner))

    return HttpResponseRedirect(reverse("detail", kwargs={"item_name":listing_info.item_name}))


def if_user_login(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))


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
