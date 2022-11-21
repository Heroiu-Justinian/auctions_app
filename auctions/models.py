from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.db.models.fields import uuid

class User(AbstractUser):
    pass



class Auction(models.Model):
    """
    Implements auctions.
    Fields:
    - seller: the user who posted the auction
    - title: title of the auction
    - description: description of what is being auctioned
    - current_bid: the current highest bid for the item listed
    - category
    """


    #TODO: upload photos for each listing

    FASHION = 'FSH'  
    OUTDOORS = 'OUT'  
    TOYS = 'TOY'  
    BOOKS = 'BOK'  
    TOOLS = 'TOL'  
    DECORATIONS = 'DEC'
    SERVICES = 'SRV'
    NOT_SPECIFIED = 'NSP'
    ELECTRONICS = 'ELC'
    CATEGORY_TAGS = [
        (FASHION,'fashion'),
        (OUTDOORS,'outdoors'),
        (TOYS,'toys'),
        (BOOKS,'books'),
        (TOOLS,'tools'),
        (DECORATIONS,'decorations'),
        (SERVICES,'services'),
        (ELECTRONICS,'electronics'),
        (NOT_SPECIFIED,'unspecified')
    ]


    id = models.AutoField( primary_key=True )
    seller = models.ForeignKey( User, on_delete=models.CASCADE )
    title = models.CharField( max_length=200,   )
    description = models.TextField()
    image = models.ImageField(upload_to='images/',null=True, blank=True)
        #the bid should be at least one tenth of a monetary unit or another value defined by the user
    minimum_bid = models.DecimalField( default=1.0, max_digits = 12,
      decimal_places=2, validators = [MinValueValidator(0.1)]
    )
    posted = models.DateTimeField( editable=False, auto_now_add=True )
    category = models.CharField( max_length=3, choices=CATEGORY_TAGS, default=NOT_SPECIFIED,   )
    closed = models.BooleanField(default=False)

    
    def __str__(self):
        return f'Auction no: {self.id} submitted by {self.seller} : {self.title} currently {self.minimum_bid}'

        
        
 



class Bid(models.Model):

    id = models.AutoField(primary_key=True, editable=False)
    auction = models.ForeignKey( Auction, on_delete=models.CASCADE )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(editable=False, auto_now_add=True)
    value = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'bid id:{self.id} by {self.user} of value {self.value}'




class Comment(models.Model):

    id = models.AutoField(primary_key=True, editable=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField( 
        help_text = 'Please be respectful in your comment and try to be helpful.' 
    )
    date = models.DateTimeField(editable=False, auto_now_add=True)

    def __str__(self):
        return f'comment no: {self.id} by {self.user} posted on {self.date}; text: {self.body}'


class Watchlist(models.Model):
    
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unique_together = ["auction", "user"]
