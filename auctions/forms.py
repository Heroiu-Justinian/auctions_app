from django.forms import ModelForm 
from .models import Auction, Bid, Comment


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title','description','image','minimum_bid','category']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['value']

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields = ['body']
