from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    User, AuctionListing, Comment, Category, Bid, Watchlist, WinnerList
)


def index(request):
    product_title = AuctionListing.objects.all().order_by('-post_time',)
    return render(request, "auctions/index.html", {
        "products": product_title
    })


def product_view(request, product_id):
    product_title = AuctionListing.objects.get(id=product_id)
    wishlist_checker = Watchlist.objects.all().filter(
        product_id=product_id, watcher_id=request.user.id)

    product_owner = User.objects.get(id=product_title.owner_id)
    owner = False
    try:
        if int(product_title.owner_id) == int(request.user.id):
            owner = True
        else:
            owner = False
    except:
        pass

    if str(wishlist_checker) == "<QuerySet []>":
        wish = True
    else:
        wish = False

    try:
        latest = WinnerList.objects.all().filter(won_product_id=product_id).last()
        if str(latest) == str(request.user.username):
            done = False
        else:
            done = True

        bid_state = Bid.objects.all().filter(of_product_id=product_id).last()
        int_bid_state = int(bid_state.bid_count)
        bid_try = False
    except:
        bid_try = True
        int_bid_state = 0

    if int_bid_state == 0:
        change = True
    else:
        change = False

    comments = Comment.objects.all().filter(of_product_id=product_id)
    size = len(comments)
    csize = False
    if size > 0:
        csize = True
    return render(request, "auctions/view.html", {
        "product_id": product_id,
        "product": product_title,
        "bid_state": latest,
        "bid": bid_try,
        "wish": wish,
        "done": done,
        "size": csize,
        "comments": comments,
        "count": int_bid_state,
        "product_owner": product_owner,
        "owner": owner,
        "change": change
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def add_listing(request):
    category_list = Category.objects.all()
    order = category_list.order_by('name',)

    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        for category_item in category_list:
            if str(category) == str(category_item):
                final = category_item
        description = request.POST.get('description')
        price = request.POST.get('price')
        photo = request.POST.get('photo')
        auctionlisting_obj = AuctionListing(
            owner=request.user,
            title=title,
            category=final,
            description=description,
            price=price,
            photo=photo
        )
        auctionlisting_obj.save()
        return render(request, "auctions/add.html", {
            "submission": True,
            "title": title,
            "category": category,
        })

    return render(request, "auctions/add.html", {
        "categories": order
    })


@login_required
def show_listing(request):
    product_title = AuctionListing.objects.all().filter(
        owner_id=int(request.user.pk)).order_by('-is_active', 'title')
    latest_list = []
    bid_state_list = []

    found = False
    for product in product_title:
        try:
            latest = WinnerList.objects.get(won_product_id=product.id)
            bid_state = Bid.objects.all().filter(of_product_id=product.id).last()
            latest_list.append(latest)
            bid_state_list.append(bid_state)
            found = True
        except:
            found = False

    all_product = AuctionListing.objects.all()
    winning_list = []
    for prod in all_product:
        try:
            extra = WinnerList.objects.get(
                won_product_id=prod.id, winner_id=request.user.id)
            if int(extra.winner_id) == int(request.user.id):
                winning_list.append(extra)
            won = True
            print("Here")
        except:
            won = False

    print(winning_list)
    size = len(product_title)
    empty = False
    if size == 0:
        empty = True

    print(str(won))
    return render(request, "auctions/listing.html", {
        "products": product_title,
        "size": size,
        "empty": empty,
        "latest": latest_list,
        "count": bid_state_list,
        "found": found,
        "won": won,
        "winning": winning_list
    })


@login_required
def categories(request):
    set_categories = Category.objects.all()
    order = set_categories.order_by('name',)
    size = len(set_categories)
    return render(request, "auctions/categories.html", {
        "categories": order,
        "size": size
    })


def show_category(request, category_id):
    specific = AuctionListing.objects.all().filter(
        category=category_id, is_active=True)
    category_name = Category.objects.get(id=category_id)
    size = len(specific)
    amount = False
    if size == 0:
        amount = True
    return render(request, "auctions/show_category.html", {
        "products": specific,
        "size": size,
        "category": category_name,
        "amount": amount
    })


@login_required
def watchlist(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = AuctionListing.objects.get(id=product_id)
        watchlist_obj = Watchlist(
            product=product,
            watcher=request.user
        )
        bid_details = Bid.objects.all().filter(of_product_id=product_id)
        watchlist_obj.save()
        return render(request, "auctions/watchlist.html", {
            "product": product,
            "first": True,
            "bid_details": bid_details
        })

    product_id = request.POST.get('product_id')
    product_watchlist = Watchlist.objects.all().filter(watcher_id=request.user.pk)
    size = len(product_watchlist)
    empty = True
    if size == 0:
        empty = False

    return render(request, "auctions/watchlist.html", {
        "size": size,
        "all_product": product_watchlist,
        "empty": empty
    })


def bid(request):
    if request.method == "POST":
        placed_bid = request.POST.get('bid')
        product_id = request.POST.get('of_product')
        listing = AuctionListing.objects.get(id=product_id)
        try:
            bid_state = Bid.objects.all().filter(of_product_id=product_id).last()
            int_bid_state = int(bid_state.bid_count)
            int_bid_state = int_bid_state + 1
        except:
            int_bid_state = 1

        bid_obj = Bid(
            bid_price=placed_bid,
            bid_count=int_bid_state,
            of_product=listing,
            bid_user=request.user
        )
        bid_obj.save()

        if int_bid_state == 1:
            winner_obj = WinnerList(
                winner=request.user,
                won_product=listing,
                latest_bid=placed_bid
            )
            winner_obj.save()
        else:
            WinnerList.objects.all().filter(won_product_id=product_id).last().delete()
            winner_obj = WinnerList(
                winner=request.user,
                won_product=listing,
                latest_bid=placed_bid
            )
            winner_obj.save()

    all_product = AuctionListing.objects.all().order_by('-post_time')
    return render(request, "auctions/index.html", {
        "products": all_product,
        "user": request.user
    })


def remove(request):
    if request.method == "POST":
        remove_id = request.POST.get('remove')
        product = request.POST.get('rem_product')
        Watchlist.objects.all().filter(product_id=product,
                                       watcher_id=request.user.id).delete()
    return HttpResponseRedirect(reverse("auctions:watchlist"))


def rem(request):
    if request.method == "POST":
        remove_id = request.POST.get('remove')
        product = request.POST.get('rem_product')
        AuctionListing.objects.all().filter(id=product, owner_id=request.user.id).delete()
    return HttpResponseRedirect(reverse("auctions:show_listing"))


def sold(request):
    if request.method == "POST":
        sold_item = request.POST.get('sold_product')
        sold_value = False

        product = AuctionListing.objects.get(
            id=sold_item, owner_id=request.user.id)

        try:
            bid_state = Bid.objects.all().filter(of_product_id=product.id).last()
            winner = bid_state.bid_user
            latest_bid = bid_state.bid_price
        except:
            return HttpResponseRedirect(reverse("auctions:show_listing"))

        obj = AuctionListing(
            owner=request.user,
            title=product.title,
            category=product.category,
            description=product.description,
            price=product.price,
            photo=product.photo,
            post_time=product.post_time,
            is_active=sold_value,
        )
        obj.save()
        product.delete()

        win_obj = WinnerList(
            winner=winner,
            won_product=obj,
            latest_bid=latest_bid
        )
        win_obj.save()
    return HttpResponseRedirect(reverse("auctions:show_listing"))


def user_comments(request):
    if request.method == "POST":
        post_comment = request.POST.get('comment')
        product_id = request.POST.get('cproduct')
        of_product = AuctionListing.objects.get(id=product_id)
        comment_obj = Comment(
            post_comment=post_comment,
            comment_user=request.user,
            of_product=of_product
        )
        comment_obj.save()
        return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, "auctions/index.html")
