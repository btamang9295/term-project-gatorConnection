from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.middleware.csrf import get_token
import logging
from gator_connection.database.search import Search
from gator_connection.database.super_user.super_user_tools import SuperUserTools
from gator_connection.models import *

from gator_connection.database.contact_us import ContactUs
from gator_connection.database.authentication.authentication import Authentication
from gator_connection.database.gator_connection_exceptions import *
from gator_connection.database.authentication.student_authentication import StudentAuthentication
from gator_connection.database.authentication.admin_authentication import AdminAuthentication
from gator_connection.database.authentication.super_user_authentication import SuperUserAuthentication

from gator_connection.database.restaurants.restaurant_request import RestaurantRequests

from gator_connection.database.housing.housing import Housing
from gator_connection.database.housing.housing_request import HousingRequests
from gator_connection.database.item.item import Item
from gator_connection.database.item.item_request import ItemRequests
from gator_connection.database.announcements.announcement import Announcements
from gator_connection.database.restaurants.restaurant import Restaurants
from gator_connection.database.restaurants.restaurant_review import RestaurantReviews
from gator_connection.database.notification.notifications import Notifications

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# PAGES
# -------------------------------------------------------------------
def home_page(request):
    request = Authentication.getSession(request)
    """
    This function takes in a HttpRequest GET object, call the search function to select the data that 
    suit the categories and input from database.
    """
    try:

        if request.method == 'GET':

            search_query = request.GET.get('search')

            # If user hasn't searched anything
            if search_query is None or len(search_query) < 1:
                return render(request, 'home.html', {'searched': False})

            students_search = None

            # Filter what columns the database should search through by getting what the user selected in drop down menu
            if request.GET['post_categories'] == 'all':
                students_search = Search.full_text_search("student", ["first_name", "last_name", "sfsu_email"],
                                                          ["*"], search_query)
            elif request.GET['post_categories'] == 'sfsu_email':
                # filter by sfsu_email
                students_search = Search.full_text_search("student", ["sfsu_email"],
                                                          ["first_name", "last_name", "sfsu_email"], search_query)

            elif request.GET['post_categories'] == 'first_name':
                # filter by first_name``
                students_search = Search.full_text_search("student", ["first_name"],
                                                          ["first_name", "last_name", "sfsu_email"], search_query)

            elif request.GET['post_categories'] == 'last_name':
                # filter by last_name
                students_search = Search.full_text_search("student", ["last_name"],
                                                          ["first_name", "last_name", "sfsu_email"], search_query)
            # Render home page with search results
            return render(request, 'home.html', {'student': students_search, 'searched': True})

    except Exception as ex:
        # try except block necessary because if there is no value, it will return a None error
        return render(request, 'home.html', {'searched': False})


def announcements(request):
    """
    This function takes in a HttpRequest GET object, call the function **getAllAnnouncements**
    to get the list of tuples that store all announcements data with image from database.
    """
    announcement_data = Announcements.getAllAnnouncements()

    return render(request, 'Announcements/announcements_home.html', {'announcement_data': announcement_data})


def announcements_detail(request, announcement_id):
    """
    This function takes in a HttpRequest GET object, call the function **getAnnouncement**
    to get the list of tuple that store specific announcements data with image from database
    according to announcement id.
    """
    try:
        announcement_data = Announcements.getAnnouncement(announcement_id)
        return render(request, 'Announcements/announcements_detail.html', {'announcement_data': announcement_data})
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect('/announcements')


def shop(request):
    """
    This function takes in a HttpRequest to redirect the user page to shop_home.html.
    """
    return render(request, 'Shop/shop_home.html')


def video(request):
    """
    This function takes in a HttpRequest to redirect the user page to Pictures/video.mp4.
    """
    return render(request, 'Pictures/video.mp4')


def housing_post1(request):
    """
    This function takes in a HttpRequest to redirect the user page to Shop/housing_post1.html.
    """
    return render(request, 'Shop/housing_post1.html', {})


def restaurants(request):
    restaurants_data = Restaurants.getRestaurants(request)

    search_query = request.GET.get('search')
    search_category = request.GET.get('post_categories')

    return render(request, 'Restaurants/restaurants_home.html',
                  {'restaurants_data': restaurants_data, 'search_query': search_query,
                   "search_category": search_category})


def restaurant_detail(request, restaurant_id):
    """
    This function takes in a HttpRequest and restaurant_id, to redirect the user to
    visit the specific restaurant page and show the data that get from database by
    calling function **getRestaurant**.
    """
    restaurant_data = Restaurants.getRestaurant(restaurant_id)

    return render(request, 'Restaurants/restaurant_detail.html', {'restaurant_data': restaurant_data})


def maps(request):
    """
    This function takes in a HttpRequest to redirect the user page to maps.html.
    """
    return render(request, 'Maps/maps.html', {})


def restaurant_post1(request):
    """
    This function takes in a HttpRequest to redirect the user page to restaurant_post1.html.
    """
    return render(request, 'Restaurants/restaurant_post1.html')


def restaurant_post2(request):
    """
    This function takes in a HttpRequest to redirect the user page to restaurant_post2.html.
    """
    return render(request, 'Restaurants/restaurant_post2.html')


def restaurant_post3(request):
    """
    This function takes in a HttpRequest to redirect the user page to restaurant_post3.html.
    """
    return render(request, 'Restaurants/restaurant_post3.html')


def announcements_post1(request):
    """
    This function takes in a HttpRequest to redirect the user page to announcements_post1.html.
    """
    return render(request, 'Announcements/announcements_post1.html')


def announcements_post2(request):
    """
    This function takes in a HttpRequest to redirect the user page to announcements_post2.html.
    """
    return render(request, 'Announcements/announcements_post2.html')


def announcements_post3(request):
    """
    This function takes in a HttpRequest to redirect the user page to announcements_post3.html.
    """
    return render(request, 'Announcements/announcements_post3.html')


def housing(request):
    """
    This function takes in a HttpRequest to redirect the user page to housing.html,
    then show the result of searching that suit the input in search bar by calling
    the function **getHousingPosts**.Then, the page will only display the housings that
    selected from database.
    """
    housing_data = Housing.getHousingPosts(request)

    search_query = request.GET.get('search')
    search_category = request.GET.get('post_categories')

    return render(request, 'Shop/housing.html',
                  {'housing_data': housing_data, 'search_query': search_query, 'search_category': search_category})


def listingadd(request):
    """
    This function takes in a HttpRequest to redirect the user page to listingadd.html,
    then let user to fill the form and save the information into database.
    """
    return render(request, 'Shop/listingadd.html', {})


def item(request):
    """
    This function takes in a HttpRequest to redirect the user page to item.html,
    then show the result of searching that suit the input in search bar by calling
    the function **getItemPosts**.Then, the page will only display the items that
    selected from database.
    """
    item_data = Item.getItemPosts(request)

    search_query = request.GET.get('search')
    search_category = request.GET.get('post_categories')

    return render(request, 'Shop/item.html',
                  {'item_data': item_data, 'search_query': search_query, 'search_category': search_category})


def item_detail(request, item_id):
    """
    This function takes in a HttpRequest and item_id, to redirect the user to
    visit the specific item page and show the data that get from database by
    calling function **getItemPost**.
    """
    try:
        item_data = Item.getItemPost(item_id)

        if ItemRequests.checkIfRequested(request, item_data.get('item')):
            return render(request, 'Shop/item_detail.html', {'item_data': item_data, 'hasRequested': True})

        return render(request, 'Shop/item_detail.html', {'item_data': item_data})
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect('/item')


def item_post1(request):
    """
    This function takes in a HttpRequest to redirect the user page to item_post1.html.
    """
    return render(request, 'Shop/item_post1.html', {})


def housing_post1(request):
    """
    This function takes in a HttpRequest to redirect the user page to housing_post1.html.
    """
    return render(request, 'Shop/housing_post1.html', {})


def housing_detail(request, housing_id):
    """
    This function takes in a HttpRequest and housing_id, to redirect the user to
    visit the specific housing page and show the data that get from database by
    calling function **getHousingPost**.
    """
    try:
        housing_data = Housing.getHousingPost(housing_id)

        if HousingRequests.checkIfRequested(request, housing_data.get('housing')):
            return render(request, 'Shop/housing_detail.html', {'housing_data': housing_data, 'hasRequested': True})
        return render(request, 'Shop/housing_detail.html', {'housing_data': housing_data})
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect('/housing')


def search_housing_listing(request, search_query):
    """
    This function takes in a HttpRequest to redirect the user page to housing.html,
    then call the function **searchHousingPosts** to search the housing listing that
    get list of tuple from database by using query.
    """
    try:
        housing_data = Housing.searchHousingPosts(request)
        return render(request, 'Shop/housing.html', {'housing_data': housing_data})
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect('/housing')


def posting(request):
    """
    This function takes in a HttpRequest to redirect the user page to posting.html.
    """
    return render(request, 'Shop/posting.html', {})


def authentication_popup_box(request):
    """
    This function takes in a HttpRequest to redirect the user page to login_register_popup_box.html,
    """
    return render(request, 'Login_Register/login_register_popup_box.html')


def user_posts(request):
    """
    This function takes in a HttpRequest to redirect the user to profile.html.
    Then get the data of post that create by user from database.
    """
    try:
        housing_listings = Housing.getHousingPostsByUser(request)
        item_listings = Item.getItemPostsByUser(request)

        return render(request, 'Login_Register/profile.html',
                      {'housing_listings': housing_listings, 'item_listings': item_listings})
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())

        return render(request, 'Login_Register/profile.html')
    except Exception as e:
        messages.error(request, "Something went wrong while loading this page.")
        return render(request, 'Login_Register/profile.html')






# -------------------------------------------------------------------
# AUTHENTICATION
# -------------------------------------------------------------------
def student_registration(request):
    """
    This function takes in a HttpRequest to make the user fill the form of
    registered by calling **StudentAuthentication.registerStudent**, and
    send the message about register to user page.
    """
    try:
        request = StudentAuthentication.registerStudent(request)

        messages.success(request,
                         f'Thank you for registering {request.session["first_name"]} {request.session["last_name"]}!')
        messages.success(request, "Please verify your account using the link sent to your email.")
        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)

        return redirect('/')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)
        return redirect('/')


def admin_registration(request):
    """
    This function takes in a HttpRequest to make the user fill the form of
    registered by calling **AdminAuthentication.registerAdmin**, and
    send the message about register to user page.
    """
    try:
        request = AdminAuthentication.registerAdmin(request)

        messages.success(request,
                         f'Thank you for registering {request.session["admin_position"]} {request.session["first_name"]} {request.session["last_name"]}!')
        messages.success(request, "Please verify your account using the link sent to your email.")
        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)

        return redirect('/')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)
    return redirect('/')


def super_user_registration(request):
    """
    This function takes in a HttpRequest to make the user fill the form of
    registered by calling **SuperUserAuthentication.registerSuperUser**, and
    send the message about register to user page.
    """
    try:
        request = SuperUserAuthentication.registerSuperUser(request)

        messages.success(request,
                         f'Thank you for registering {request.session["first_name"]} {request.session["last_name"]}!')
        messages.success(request, "Please verify your account using the link sent to your email.")

        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)

        return redirect('/')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)
    return redirect('/')


def login_student(request):
    """
    This function takes in a HttpRequest POST object, to call the API of authentication
    to compare the data from form filling with the data from Student Account table on
    Gator-Connection Database. if pass the comparing, user login success.
    """
    try:
        if request.method == 'POST':
            request = StudentAuthentication.authenticateStudent(request)

            messages.success(request, f'Hello {request.session["first_name"]} {request.session["last_name"]}!')
            url = request.META.get('HTTP_REFERER')

            if url is not None:
                return redirect(url)

            return redirect('/')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)
        return redirect('/')


def login_admin(request):
    """
    This function takes in a HttpRequest POST object, to call the API of authentication
    to compare the data from form filling with the data from Admin Account table on
    Gator-Connection Database. if pass the comparing, the user login success.
    """
    try:
        if request.method == 'POST':
            request = AdminAuthentication.authenticateAdmin(request)

            messages.success(request, f'Hello {request.session["first_name"]} {request.session["last_name"]}!')
            url = request.META.get('HTTP_REFERER')

            if url is not None:
                return redirect(url)

            return redirect('/')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())

        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)
        return redirect('/')


def login_super_user(request):
    """
    This function takes in a HttpRequest POST object, to call the API of authentication
    to compare the data from form filling with the data from SuperUser Account table on
    Gator-Connection Database. if pass the comparing, the user login success.
    """
    try:
        if request.method == 'POST':
            request = SuperUserAuthentication.authenticateSuperUser(request)

            messages.success(request, f'Hello {request.session["first_name"]} {request.session["last_name"]}!')
            url = request.META.get('HTTP_REFERER')

            if url is not None:
                return redirect(url)

            return redirect('/')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())

        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)
        return redirect('/')


def logout_user(request):
    """
    This function takes in a HttpRequest to call the API of authentication
    to delete all data of session of the user.
    """
    try:
        request = Authentication.logout(request)

        messages.success(request, 'You have succesfully logged out!')

        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)

        return redirect('/')
    except:
        # try except for logging out user who is not in logged in table
        messages.error(request, 'Something went wrong while logging out')
        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)

        return redirect('/')





def notifications(request):
    """
    This function takes in a HttpRequest to get multiple notification by calling
    different type notifications base on the user role(Normal, Admin, SuperUser)
    """
    if 'is_loggedin' in request.session.keys():

        # Get Notifications for user
        notifications = Notifications.getNotifications(request)

        # Get Housing Requests for user
        housing_requests = HousingRequests.getHousingRequests(request)

        # Get Item Requests for user
        item_requests = ItemRequests.getItemRequests(request)

        # Create template_data dictionary with notifications and empty requests dictionary
        template_data = {
            "notifications": notifications,
            "requests": {}
        }

        # Add housing requests and item requests if they have length greater than 0
        if len(housing_requests) > 0:
            template_data["requests"]["housing_requests"] = housing_requests

        if len(item_requests) > 0:
            template_data["requests"]["item_requests"] = item_requests

        if request.session.get('isSuperUser'):
            try:
                restaurant_requests = RestaurantRequests.getAllRequests()

                super_user_requests = SuperUserAuthentication.getAllSuperUserAccountRequests(request)
                admin_user_requests = AdminAuthentication.getAllAdminAccountRequests(request)

                # Create empty account_requests dictionary
                account_requests = {}

                # Add super user and admin user requests if there are any to account_requests
                if len(super_user_requests) > 0:
                    account_requests["super_users"] = super_user_requests

                if len(admin_user_requests) > 0:
                    account_requests["admin_users"] = admin_user_requests

                # If there are any account_requests, add to template_data["requests"]

                # Add Super User Specific Requests if there are any
                if len(restaurant_requests) > 0:
                    template_data["requests"]["restaurant_requests"] = restaurant_requests

                if bool(account_requests):
                    template_data["requests"]["account_requests"] = account_requests
            except GatorConnectionError as e:
                messages.error(request, e.getMessage())


        return render(request, 'Login_Register/notifications.html', {"data": template_data})

    else:
        messages.error(request, "You are forbidden from seeing the notification page without logging in.")
        return redirect('/')


def faq(request):
    """
    This function takes in a HttpRequest to redirect the user page to faq.html.
    """
    return render(request, 'Misc/faq.html')


def about(request):
    """
    This function takes in a HttpRequest to redirect the user page to about.html.
    """
    return render(request, 'Misc/about.html')


def contact(request):
    """
    This function takes in a HttpRequest to redirect the user to contact.html.
    Then get the data from the user filling and send email to our team by
    calling the function **sendContactUsFormEmail**
    """
    if request.method == "POST":
        # Send all of the contact us post information to the main gator connection email
        try:
            ContactUs.sendContactUsFormEmail(request)
            messages.success(request, "Successfully sent form.")
        except GatorConnectionError as e:
            messages.error(request, e.getMessage())

    return render(request, 'Misc/contact.html')


def terms_and_conditions(request):
    """
    This function takes in a HttpRequest to redirect the user page to terms_and_conditions.html.
    """
    return render(request, 'Misc/terms_and_conditions.html')


# -------------------------------------------------------------------
# SEARCH UTILITIES
# -------------------------------------------------------------------
def search(request):
    """
    This function takes in a HttpRequest to redirect search categories according to user choices.
    Then we get different query to select the object in database.
    """
    csrf_token = get_token(request)

    if request.GET['post_categories'] == "housing":
        return redirect(f'/housing?csrfmiddlewaretoken={csrf_token}&search={request.GET.get("search")}')
    elif request.GET['post_categories'] == "item":
        return redirect(f'/item?csrfmiddlewaretoken={csrf_token}&search={request.GET.get("search")}')
    elif request.GET['post_categories'] == "restaurant":
        return redirect(f'/restaurants?csrfmiddlewaretoken={csrf_token}&search={request.GET.get("search")}')




# -------------------------------------------------------------------
# POSTING
# -------------------------------------------------------------------
def post_housing_listing(request):
    """
    This function takes in a HttpRequest POST object, to call the saveHousingFormInformation
    to save the data from form filling into Housing Listing Post and Post in database.
    """
    # saving information in housing listing post, post, and image tables
    if request.method == 'POST':
        try:
            Housing.saveHousingFormInformation(request)
            messages.success(request, "Successfully posted housing listing")
            return redirect('/housing')
        except GatorConnectionError as e:
            messages.error(request, e.getMessage())
            return redirect('/housing')

        #  return render(request, 'Shop/housing.html')
    return redirect('/housing')


def edit_housing_listing(request, housing_id):
    """
    This function takes in a HttpRequest POST object, to call the editHousingListing
    to edit the data from form filling into Housing Listing Post and Post in database.
    """
    if request.method == 'POST':
        try:
            Housing.editHousingListing(request, housing_id)

            messages.success(request, "Successfully edited housing listing post.")
            return redirect(f'/housing/{housing_id}')
        except GatorConnectionError as e:
            messages.error(request, e.getMessage())
            return redirect(f'/housing/{housing_id}')

    messages.error(request, "This feature is currently undergoing maintenance, please try again later.")
    return redirect('/housing')


def delete_housing_listing(request, housing_id):
    """
    This function takes in a HttpRequest POST object, to call the deleteHousingListing
    to delete post. It will check the owner of post then deleted the post if pass the
    comparing part.
    """
    if request.method == 'POST':
        try:
            Housing.deleteHousingListing(request, housing_id)

            messages.success(request, "Successfully deleted housing listing post.")
            return redirect('/housing')
        except GatorConnectionError as e:
            messages.error(request, e.getMessage())
            return redirect('/housing')

    messages.error(request, "This feature is currently undergoing maintenance, please try again later.")
    return redirect('/housing')


def post_item_listing(request):
    """
    This function takes in a HttpRequest POST object, to call the saveItemFormInformation
    to save the data from form filling into Item Listing Post and Post in database.
    """
    # saving information in item listing post, post, and item_image tables
    if request.method == 'POST':
        try:
            Item.saveItemFormInformation(request)
            messages.success(request, "Successfully posted item listing")
            return redirect('/item')
        except GatorConnectionError as e:
            messages.error(request, e.getMessage())

    messages.error(request, "This feature is currently undergoing maintenance, please try again later.")
    return redirect('/item')


def edit_item_listing(request, item_id):
    """
    This function takes in a HttpRequest POST object, to call the editHousingListing
    to edit the data from form filling into Item Listing Post and Post in database.
    """
    if request.method == 'POST':
        try:
            Item.editItemListing(request, item_id)
            messages.success(request, "Successfully edited housing listing post.")
            return redirect(f'/item/{item_id}')
        except GatorConnectionError as e:
            messages.error(request, e.getMessage())
            return redirect(f'/item/{item_id}')

    messages.error(request, "This feature is currently undergoing maintenance, please try again later.")
    return redirect('/item')


def delete_item_listing(request, item_id):
    """
    This function takes in a HttpRequest POST object, to call the deleteItemListing
    to delete post. It will check the owner of post then deleted the post if pass the
    comparing part.
    """
    if request.method == 'POST':
        try:
            Item.deleteItemListing(request, item_id)
            messages.success(request, "Successfully deleted item listing post.")
            return redirect('/item')
        except GatorConnectionError as e:
            messages.error(request, e.getMessage())
            return redirect('/item')

    messages.error(request, "This feature is currently undergoing maintenance, please try again later.")
    return redirect('/item')


def post_announcement(request, category):
    """
    This function takes in a HttpRequest  to call the postAnnouncement
    to save the data from form filling into Announcement and Post in database.
    """
    try:
        Announcements.postAnnouncement(request, category)
        messages.success(request, f"Successfully posted {category} announcement.")
        return redirect('/announcements')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect('/announcements')


def edit_announcement(request, announcement_id):
    """
    This function takes in a HttpRequest to call the editAnnouncement
    to edit the data from form filling into Announcement Post and Post in database.
    """
    try:
        Announcements.editAnnouncement(request, announcement_id)
        messages.success(request, "Successfully edited announcement")
        return redirect(f'/announcements/{announcement_id}')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect(f'/announcements/{announcement_id}')


def delete_announcement(request, announcement_id):
    """
    This function takes in a HttpRequest to call the deleteAnnouncement
    to delete post. It will check the owner of post then deleted the post if pass the
    comparing part.
    """
    try:
        Announcements.deleteAnnouncement(request, announcement_id)
        messages.success(request, "Successfully deleted announcement.")
        return redirect('/announcements')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect('/announcements')


# -------------------------------------------------------------------
# REQUESTING
# -------------------------------------------------------------------
def request_add_restaurant(request):
    """
    This function takes in a HttpRequest to call the postRestaurantRequest
    to post the data from form filling into Restaurant Request in database.
    """
    try:
        if request.method == 'POST':
            RestaurantRequests.postRestaurantRequest(request)

            messages.success(request, f"Successfully requested to add {request.POST.get('name')}")
            return redirect('/restaurants')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect('/restaurants')


def request_housing_listing(request, housing_id):
    """
    This function takes in a HttpRequest to call the postHousingRequest
    to post the data from form filling into Housing Listing Request in database.
    """
    try:
        HousingRequests.postHousingRequest(request, housing_id)
        messages.success(request, "Your housing request has successfully been sent.")

        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)

        return redirect('/housing')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())

        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)
        return redirect('/housing')


def delete_housing_request(request, housing_id):
    """
    This function takes in a HttpRequest to call the deleteHousingRequest
    to delete post. It will check the owner of post then deleted the post if pass the
    comparing part.
    """
    try:
        HousingRequests.deleteHousingRequest(request, housing_id)
        messages.success(request, "Your housing request has successfully been deleted.")
        return redirect('/housing')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect('/housing')


def request_item_listing(request, item_id):
    """
    This function takes in a HttpRequest to call the postItemRequest
    to post the data from form filling into Item Listing Request in database.
    """
    try:
        ItemRequests.postItemRequest(request, item_id)
        messages.success(request, "Your item request has successfully been sent.")

        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)
        return redirect('/item')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())

        url = request.META.get('HTTP_REFERER')

        if url is not None:
            return redirect(url)
        return redirect('/item')


def delete_item_request(request, item_id):
    """
    This function takes in a HttpRequest to call the deleteItemRequest
    to delete post. It will check the owner of post then deleted the post if pass the
    comparing part.
    """
    try:
        ItemRequests.deleteItemRequest(request, item_id)
        messages.success(request, "Your item request has been successfully been deleted.")
        return redirect('/item')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect('/item')


def post_restaurant_review(request, restaurant_id):
    """
    This function takes in a HttpRequest to call the postRestaurantReview
    to save the data from form filling into Restaurant Reviews in database.
    """
    try:
        RestaurantReviews.postRestaurantReview(request, restaurant_id)
        messages.success(request, 'Your restaurant review has been successfully posted.')
        return redirect(f'/restaurants/{restaurant_id}')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect(f'/restaurants/{restaurant_id}')


def post_restaurant_image(request, restaurant_id):
    """
    This function takes in a HttpRequest to call the postRestaurantReview
    to save the data from form filling into Image in database.
    """
    try:
        Restaurants.postImage(request, restaurant_id)
        messages.success(request, "Your restaurant image has been successfully posted.")
        return redirect(f'/restaurants/{restaurant_id}')
    except GatorConnectionError as e:
        messages.error(request, e.getMessage())
        return redirect(f'/restaurants/{restaurant_id}')


def user_confirm(request):
    """
    This function takes in a HttpRequest to call the Notification and
    save the data into Notification into database according to the user
    and the post owner. Also,to check and set the email verification of user.
    """
    code = request.GET.get('code', None)
    try:
        confirm = EmailVerification.objects.get(code=code)
        confirm.account.email_verified = True
        confirm.account.save()

        try:
            registered_user = RegisteredUser.objects.get(user=confirm.account.user)

            notification = Notification()
            notification.registered_user = registered_user
            notification.message = "You have successfully verified your account."
            notification.save()
        except RegisteredUser.DoesNotExist:
            print("Cannot send notification. Cannot find Registered User for corresponding account.")

        confirm.delete()

        # If user is logged in, add email_verified to request.sessions object
        if 'is_loggedin' in request.session.keys():
            request.session['email_verified'] = True

        return render(request, 'home.html')
    except:
        message = 'No valid request'
        return render(request, 'home.html')


# ============================================================
# Super User Tools
# ============================================================

def accept_super_user_request(request, super_user_id):
    """
    This function takes in a HttpRequest to call the SuperUserTools
    for SuperUser. Then update the attribute of  "is_approved" to True
    in Super User Account table on database.
    """
    try:
        SuperUserTools.approveSuperUser(super_user_id)

        return JsonResponse({
            'status': 'success',
            'message': 'Approved Super User Request'

        })
    except GatorConnectionError as e:
        return JsonResponse({
            'status': 'failure',
            'message': e.getMessage(),
        })


def reject_super_user_request(request, super_user_id):
    """
    This function takes in a HttpRequest to call the SuperUserTools
    for SuperUser. Then keep the attribute of  "is_approved" like False
    in Super User Account table on database.
    """
    try:
        SuperUserTools.rejectSuperUser(super_user_id)

        return JsonResponse({
            'status': 'success',
            'message': 'Rejected Super User Request'

        })
    except GatorConnectionError as e:
        return JsonResponse({
            'status': 'failure',
            'message': e.getMessage(),
        })


def accept_admin_request(request, admin_id):
    """
    This function takes in a HttpRequest to call the SuperUserTools
    for Admin. Then update the attribute of  "is_approved" to True
    in Admin Account table on database.
    """
    try:
        SuperUserTools.approveAdmin(admin_id)

        return JsonResponse({
            'status': 'success',
            'message': 'Approved Admin Request'

        })
    except GatorConnectionError as e:
        return JsonResponse({
            'status': 'failure',
            'message': e.getMessage(),
        })


def reject_admin_request(request, admin_id):
    """
    This function takes in a HttpRequest to call the SuperUserTools
    for Admin. Then keep the attribute of  "is_approved" like False
    in Admin Account table on database.
    """
    try:
        SuperUserTools.rejectAdmin(admin_id)

        return JsonResponse({
            'status': 'success',
            'message': 'Rejected Admin Request'

        })

    except GatorConnectionError as e:
        return JsonResponse({
            'status': 'failure',
            'message': e.getMessage(),
        })


def accept_restaurant_request(request, restaurant_request_id):
    """
    This function takes in a HttpRequest to call the SuperUserTools
    to check the user permission. Restaurant post will save into database
    if user account belong the super user account.
    """
    try:
        SuperUserTools.approveRestaurantRequest(restaurant_request_id)

        return JsonResponse({
            'status': 'success',
            'message': 'Approved Restaurant Request'
        })
    except GatorConnectionError as e:
        return JsonResponse({
            'status': 'failure',
            'message': e.getMessage()
        })


def reject_restaurant_request(request, restaurant_request_id):
    """
    This function takes in a HttpRequest to call the SuperUserTools
    to check the user permission. Restaurant post will not save into
    database if user account not belong the super user account.
    """
    try:
        SuperUserTools.rejectRestaurantRequest(restaurant_request_id)

        return JsonResponse({
            'status': 'success',
            'message': 'Rejected Restaurant Request'
        })
    except GatorConnectionError as e:
        return JsonResponse({
            'status': 'failure',
            'message': e.getMessage()
        })

# ============================================================
# API
# ============================================================


def check_notifications(request):
    """
    This function takes in a HttpRequest to call the checkNotifications
    to check the 'read' attribute of Notifications for the user.
    """
    try:
        has_notifications = Notifications.checkNotifications(request)
    except GatorConnectionError as e:
        has_notifications = False

    return JsonResponse({
        'hasNotifications': has_notifications
    })
