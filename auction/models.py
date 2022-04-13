from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import auth
from django.utils import timezone
# Create your models here.

from django.core.exceptions import ValidationError

def validate_range(value):
    if value < BidItem.base_price:
        raise ValidationError('Min value should be %s' % BidItem.base_price
        )


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null = True)

    class Meta:
        db_table = "category"

class Item(models.Model):
    name = models.CharField(max_length= 50)
    description = models.TextField(null = True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    class Meta:
        db_table = 'item'

class Address(models.Model):
    house_number = models.PositiveIntegerField(null=True)
    street = models.CharField(max_length=30)
    locality = models.CharField(max_length=30,null=True)
    home_town = models.CharField(max_length=40,null=True)
    district = models.CharField(max_length=30,null=True)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    postal_code = models.IntegerField(validators=[MaxValueValidator(1000000),MinValueValidator(99999)])

    class Meta:
        db_table = "address"

class User(models.Model):
    first_name = models.CharField(max_length=40,default = "John")
    last_name = models.CharField(max_length=40,default = "Doe")
    email = models.EmailField(max_length=50,default = "JohnDoe@gmail.com")
    phone_number = models.PositiveBigIntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(100000000)], null=True)
    age = models.PositiveSmallIntegerField()
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    password = models.CharField(max_length=500,null = True)

    class Meta:
        db_table = "user"

    def name(self):
        return self.first_name + " " + self.last_name

    name = property(name)

class BidItem(models.Model):
    item = models.OneToOneField(Item,on_delete=models.CASCADE)
    base_price = models.PositiveIntegerField()
    is_sold = models.BooleanField(default=False)

    class Meta:
        db_table = "biditem"

    def current_bid(self):
        bids = Bid.objects.filter(bid_item = self).values_list('amount',flat=True)
        return  max(bids)

    current_bid = property(current_bid)

class Bid(models.Model):
    bid_item = models.ForeignKey(BidItem,on_delete=models.CASCADE)

    def min_bid(self):
        return self.bid_item.base_price

    amount = models.PositiveIntegerField(validators=[validate_range])
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time_of_bid = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bid"

