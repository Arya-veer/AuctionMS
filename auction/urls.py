from django.contrib import admin
from .views import *
from django.urls import path,include

urlpatterns = [
    path('register/',RegisterUser.as_view(),name = 'register'),
    path('items/',AllItemsListView.as_view(),name = 'items-list'),
    path('bid_items/',BidItemsView.as_view(),name = 'bid-items-list'),
    path('item_bids/<int:pk>',ItemBidsView.as_view(),name = 'item-bids-list'),
    path('start_bidding/',StartBiddingOnItemView.as_view(),name = 'start-bidding'),
    path('stop_bidding/<int:pk>',StopBiddingOnItemView.as_view(),name = 'stop-bidding'),
    path('bid_items_admin/',BidItemsAdminView.as_view(),name = 'bid-items-admin-list'),

]