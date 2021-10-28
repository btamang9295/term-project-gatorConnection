"""gator_connection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django import urls
from . import views

urlpatterns = [

    ### PAGES ###
    path('', views.home_page, name="home", ),
    path('announcements', views.announcements, name='announcements'),
    path('announcements/<int:announcement_id>', views.announcements_detail, name='announcements_detail'),
    path('shop', views.shop, name='shop'),
    path('restaurants', views.restaurants, name='restaurants'),
    path('restaurants/<int:restaurant_id>', views.restaurant_detail, name='restaurant_detail'),
    path('housing', views.housing, name='housing'),
    path('housing/<int:housing_id>', views.housing_detail, name='housing_detail'),
    path('item', views.item, name='item'),
    path('item/<int:item_id>', views.item_detail, name='item_detail'),
    path('authentication_popup_box', views.authentication_popup_box, name='authentication_popup_box'),
    path('search', views.search, name='search'),
    path('faq', views.faq, name='faq'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('terms_and_conditions', views.terms_and_conditions, name='terms_and_conditions'),
    path('listingadd', views.listingadd, name='listingadd'),
    path('housing_post1', views.housing_post1, name='housing_post1'),
    path('item_post1', views.item_post1, name='item_post1'),
    path('maps', views.maps, name='maps'),
    path('restaurant_post1', views.restaurant_post1, name='restaurant_post1'),
    path('restaurant_post2', views.restaurant_post2, name='restaurant_post2'),
    path('restaurant_post3', views.restaurant_post3, name='restaurant_post3'),
    path('announcements_post1', views.announcements_post1, name='announcements_post1'),
    path('announcements_post2', views.announcements_post2, name='announcements_post2'),
    path('announcements_post3', views.announcements_post3, name='announcements_post3'),
    path('video', views.video, name='video'),

    ### AUTHENTICATION ###
    path('student_registration', views.student_registration, name='student_registration'),
    path('admin_registration', views.admin_registration, name='admin_registration'),
    path('super_user_registration', views.super_user_registration, name='super_user_registration'),
    path('login_student', views.login_student, name='login_student'),
    path('login_admin', views.login_admin, name='login_admin'),
    path('login_super_user', views.login_super_user, name='login_super_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('notifications', views.notifications, name='notifications'),
    path('profile_page', views.user_posts, name='profile_page'),
    path('confirm', views.user_confirm, name='confirm_page'),

    ### UPLOADS ###
    path('housing_listing', views.post_housing_listing, name='housing_listing'),
    path('edit_housing_listing/<int:housing_id>', views.edit_housing_listing, name='edit_housing_listing'),
    path('delete_housing_listing/<int:housing_id>', views.delete_housing_listing, name='delete_housing_listing'),
    path('item_listing', views.post_item_listing, name='item_listing'),
    path('edit_item_listing/<int:item_id>', views.edit_item_listing, name='edit_item_listing'),
    path('delete_item_listing/<int:item_id>', views.delete_item_listing, name='delete_item_listing'),

    path('post_announcement/<slug:category>', views.post_announcement, name='announcement_post'),
    path('edit_announcement/<int:announcement_id>', views.edit_announcement, name='edit_announcement'),
    path('delete_announcement/<int:announcement_id>', views.delete_announcement, name='delete_announcement'),

    ### REQUESTS ###
    path('housing_request/<int:housing_id>', views.request_housing_listing, name="housing_request"),
    path('delete_housing_request/<int:housing_id>', views.delete_housing_request, name="delete_housing_request"),
    path('item_request/<int:item_id>', views.request_item_listing, name="item_request"),
    path('delete_item_request/<int:item_id>', views.delete_item_request, name="delete_item_request"),
    path('request_restaurant', views.request_add_restaurant, name="request_restaurant"),

    ### RATING ###
    path('restaurants/rate/<int:restaurant_id>', views.post_restaurant_review, name='review_restaurant'),
    path('restaurants/post-image/<int:restaurant_id>', views.post_restaurant_image, name='post_restaurant_image'),

    #### SEARCH ###
    path('housing', views.search_housing_listing, name="search_housing_listing"),

    ### SUPER USER TOOLS ###
    path('super-user-tools/super-user-requests/accept/<int:super_user_id>', views.accept_super_user_request,
         name="accept_super_user"),
    path('super-user-tools/super-user-requests/reject/<int:super_user_id>', views.reject_super_user_request,
         name="reject_super_user"),
    path('super-user-tools/admin-requests/accept/<int:admin_id>', views.accept_admin_request, name="accept_admin"),
    path('super-user-tools/admin-requests/reject/<int:admin_id>', views.reject_admin_request, name="reject_admin"),
    path('super-user-tools/restaurant-requests/accept/<int:restaurant_request_id>', views.accept_restaurant_request,
         name="accept_restaurant"),
    path('super-user-tools/restaurant-requests/reject/<int:restaurant_request_id>', views.reject_restaurant_request,
         name="reject_restaurant"),

    ### API ###
    path('notifications/user', views.check_notifications, name="check_notifications"),
    path('contact-us', views.contact, name="contact_us")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
