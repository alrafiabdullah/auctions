from django.contrib import admin
from .models import (
    User, AuctionListing, Bid, Comment, Category, Watchlist, WinnerList
)

# Register your models here.
admin.site.site_header = "CS50 Project2 Dashboard"
admin.site.site_title = "CS50 Project2 Dashboard"
admin.site.index_title = "Auctions Dashboard"


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name",
                    "email", "is_superuser", )
    list_display_links = ("username", "email",)


class ListAdmin(admin.ModelAdmin):
    list_display = ("owner", "title", "category",
                    "price", "is_active", "post_time")
    list_display_links = ("title",)
    list_filter = ("is_active", "owner", "category",)


class BidAdmin(admin.ModelAdmin):
    list_display = ("bid_price", "bid_user", "bid_count", "of_product",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post_comment", "comment_user", "of_product",)


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("product", "watcher",)


class WinnerAdmin(admin.ModelAdmin):
    list_display = ("winner", "won_product")


admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing, ListAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(WinnerList, WinnerAdmin)
