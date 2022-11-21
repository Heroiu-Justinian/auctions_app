from django.contrib import admin
from .models import (Auction,Bid, Comment)
# Register your models here.
admin.site.register([Auction,Bid,Comment])
