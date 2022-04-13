from django.shortcuts import render,redirect
from .mysql import cursor
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from .mixins import *

from django.contrib.auth.hashers import make_password
from django.contrib import messages
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials,auth
from rest_framework.response import Response as Drf_Response
from rest_framework.renderers import TemplateHTMLRenderer
# Create your views here.


class AllItemsListView(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "auction/items.html"

    def get(self,request):
        cursor.execute("select I.id as item_id ,I.name as item_name,I.description as item_description,C.name as category_name from Item as I , category as C where C.id = I.category_id;")
        items = cursor.fetchall()
        print(items)
        context = {
            "items" : items
        }
        print(context['items'][0])
        context['is_admin'] = False
        return render(request,self.template_name,context = context)

class BidItemsView(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "auction/biditems.html"

    def get(self,request):
        cursor.execute("select BI.id as id, I.id as item_code, I.name as item_name,I.description item_description,BI.base_price as base_price,BI.is_sold from Item as I , BidItem as BI where BI.item_id = I.id;")
        bid_items = cursor.fetchall()
        print(bid_items)
        for bid_item in bid_items:
            bid_item_id = bid_item['id']
            cursor.execute(f"call getCurrentBid({bid_item_id});")
            max_bid_amount = cursor.fetchone()['maxBidAmount']
            bid_item["last_bid"] = max_bid_amount
        context = {
            "bid_items" : bid_items
        }
        print(context['bid_items'])
        context['is_admin'] = False
        return render(request,self.template_name,context = context)

class ItemBidsView(LoginRequiredMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "auction/itembids.html"

    def get(self,request,pk):
        cursor.execute(f"call getBids({pk});")
        bids = cursor.fetchall()
        context = {
            "bids":bids
        }

        cursor.execute(
            f"select BI.id as id, I.id as item_code, I.name as item_name,I.description item_description,BI.base_price as base_price,BI.is_sold from Item as I , BidItem as BI where BI.item_id = I.id and BI.id = {pk};")
        biditem = cursor.fetchone()
        context['bid_item'] = biditem
        context['is_admin'] = False
        return render(request,self.template_name,context=context)

    def post(self,request,pk):
        bid_amount = int(request.POST.get('amount'))
        user_email = request.user.email
        print(user_email)
        cursor.execute(f"SELECT id from user where email = '{user_email}';")
        user_id = cursor.fetchone()['id']
        cursor.execute(f"call getCurrentBid({pk});")
        max_bid_amount = cursor.fetchone()['maxBidAmount']
        print(100,max_bid_amount)
        if max_bid_amount and (bid_amount <= max_bid_amount):
            messages.error(request, 'You can not bid less than the previous bid')
        else:
            cursor.execute(f"INSERT INTO bid ( `amount`, `bid_item_id`, `user_id`) VALUES ({bid_amount}, {pk}, {user_id});")
            messages.success(request,"Bid placed successfully")
        return redirect('./' + str(pk))


""" Below All are Auctioner's views """

class StartBiddingOnItemView(SuperuserMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "auction/startBidItems.html"

    def get(self,request):
        query = "select I.id as item_id from Item as I , BidItem as BI where BI.item_id = I.id"
        cursor.execute(f"select I.id as item_id ,I.name as item_name,I.description as item_description,C.name as category_name from Item as I , category as C where C.id = I.category_id and I.id not in ({query});")
        context = {
            "items" : cursor.fetchall()
        }
        print(context['items'][0])
        context['is_admin'] = True
        return render(request,self.template_name,context = context)

    def post(self,request):
        print(request.POST)
        base_price = request.POST.get('base_price')
        pk = request.POST.get('pk')
        print(pk)
        cursor.execute(f'call startBid({pk},{base_price})')
        return redirect("../stop_bidding/" + str(pk))

class StopBiddingOnItemView(SuperuserMixin,APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "auction/stopBidItems.html"

    def get(self, request, pk):
        cursor.execute(f"Select id from BidItem where item_id = {pk};")
        pki = cursor.fetchone()['id']
        cursor.execute(f"call getBids({pki});")
        bids = cursor.fetchall()
        context = {
            "bids": bids
        }
        print(bids)
        print(pk)
        cursor.execute(
            f"select BI.id as id, I.id as item_code, I.name as item_name,I.description item_description,BI.base_price as base_price,BI.is_sold from Item as I , BidItem as BI where BI.item_id = I.id and I.id = {pk};")
        biditem = cursor.fetchone()
        context['bid_item'] = biditem
        print(context)
        context['is_admin'] = True
        return render(request, self.template_name, context=context)

    def post(self,request,pk):
        if "pk" in request.POST.keys():
            print(pk)
            cursor.execute(f"Select id from BidItem where item_id = {pk};")
            pk = cursor.fetchone()['id']
            cursor.execute(f'call stopBid({pk})')
            return redirect('start-bidding')
        else:
            print(request.POST)
            status = request.POST.get("status")
            bid_id = request.POST.get("bid_id")
            query = f"Update bid set status = '{status}' where id = {bid_id};"
            cursor.execute(query)
            return redirect("./" +str(pk))


class RegisterUser(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "auction/register.html"

    def post(self,request):
        phone_number = request.POST.get("phone_number")
        age = request.POST.get('age')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        query = f"insert into user (phone_number, age, first_name, last_name,email, password) values ({phone_number},{age},'{first_name}','{last_name}','{email}','{password}');"

        # request.POST['username'] = email


        cursor.execute(query)
        user = User.objects.create_user(username=email.split("@")[0],password=password,email=email)
        return redirect('login')


    def get(self,request):
        context = {}
        context['is_admin'] = False
        return render(request,self.template_name,context=context)

class BidItemsAdminView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "auction/biditemsadmin.html"

    def get(self,request):
        cursor.execute("select BI.id as id, I.id as item_code, I.name as item_name,I.description item_description,BI.base_price as base_price,BI.is_sold from Item as I , BidItem as BI where BI.item_id = I.id;")
        bid_items = cursor.fetchall()
        print(bid_items)
        for bid_item in bid_items:
            bid_item_id = bid_item['id']
            cursor.execute(f"call getCurrentBid({bid_item_id});")
            max_bid_amount = cursor.fetchone()['maxBidAmount']
            bid_item["last_bid"] = max_bid_amount
        context = {
            "bid_items" : bid_items
        }
        print(context['bid_items'])
        context['is_admin'] = True
        return render(request,self.template_name,context = context)

class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "auction/login.html"

    def post(self,request):
        email = request.POST.get("email")
        password = request.POST.get("password1")

        query = f"SELECT count(*) as count from user where email = '{email}' and password = '{password}';"
        cursor.execute(query)
        count = cursor.fetchone()['count']
        username = email.split("@")[0]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('start-bidding')
            return redirect('items-list')
        messages.error(request,"No such user! Register yourself")
        return redirect('register')

    def get(self,request):
        context = {}
        context['is_admin'] = False
        return render(request, self.template_name, context=context)

def logout_view(request):
    logout(request)
    return redirect('login')