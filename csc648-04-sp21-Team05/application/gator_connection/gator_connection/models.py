from django.db import models
from django.db.models.functions import Now
import uuid


# ==============================================================================================================================
# Horizontal Prototype Models
# ==============================================================================================================================
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order (FINISHED: Based it off order of tables in generated SQL from forward engineering)
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior (FINISHED)
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# DELETE ALL MYSQL GENERATED FIELDS


# -------------------------------------------------------------------
# User Model
# -------------------------------------------------------------------
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    createdat = models.DateTimeField(db_column='createdAt', default=Now())

    class Meta:
        managed = False
        db_table = 'User'


# -------------------------------------------------------------------
# Registered User Model
# -------------------------------------------------------------------
class RegisteredUser(models.Model):
    reg_user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user')

    class Meta:
        managed = False
        db_table = 'Registered User'
        unique_together = (('reg_user_id', 'user'),)


# -------------------------------------------------------------------
# Post Model
# -------------------------------------------------------------------
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', default=Now())  # Field name made lowercase.
    registered_user = models.ForeignKey('RegisteredUser', on_delete=models.CASCADE, db_column='registered_user')

    class Meta:
        managed = False
        db_table = 'Post'


# -------------------------------------------------------------------
# Housing Listing Post Model
# -------------------------------------------------------------------
class HousingListingPost(models.Model):
    housing_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    are_pets_allowed = models.CharField(max_length=5)
    post = models.OneToOneField('Post', on_delete=models.CASCADE, db_column='post')
    preferred_pay_type = models.CharField(max_length=45)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, db_column='address')

    class Meta:
        managed = False
        db_table = 'Housing Listing Post'
        unique_together = (('housing_id', 'post', 'address'),)


# -------------------------------------------------------------------
# Housing Listing Request Model
# -------------------------------------------------------------------
class HousingListingRequest(models.Model):
    housing_request_id = models.AutoField(primary_key=True)
    createdat = models.DateTimeField(db_column='createdAt', default=Now())  # Field name made lowercase.
    registered_user = models.ForeignKey('RegisteredUser', on_delete=models.CASCADE, db_column='registered_user')
    housing_listing = models.ForeignKey('HousingListingPost', on_delete=models.CASCADE, db_column='housing_listing')

    class Meta:
        managed = False
        db_table = 'Housing Listing Request'
        unique_together = (('housing_request_id', 'registered_user', 'housing_listing'),)


# -------------------------------------------------------------------
# Housing Listing Form Model
# -------------------------------------------------------------------
class HousingListingForm(models.Model):
    form_id = models.AutoField(primary_key=True)
    about_me = models.TextField(blank=True, null=True)
    move_in = models.DateTimeField()
    phone_number = models.CharField(max_length=20, null=True)
    housing_listing_request = models.ForeignKey('HousingListingRequest', on_delete=models.CASCADE,
                                                db_column='housing_listing_request')
    registered_user = models.ForeignKey('RegisteredUser', on_delete=models.CASCADE, db_column='registered_user')

    class Meta:
        managed = False
        db_table = 'Housing Listing Form'
        unique_together = (('form_id', 'housing_listing_request', 'registered_user'),)


# -------------------------------------------------------------------
# Notification Model
# -------------------------------------------------------------------
class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    message = models.TextField(blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', default=Now())  # Field name made lowercase.
    read = models.BooleanField(default=False)
    registered_user = models.ForeignKey('RegisteredUser', on_delete=models.CASCADE, db_column='registered_user')

    class Meta:
        managed = False
        db_table = 'Notification'
        unique_together = (('notification_id', 'registered_user'),)


# -------------------------------------------------------------------
# Housing Listing Request Notification Model
# -------------------------------------------------------------------
class HousingListingRequestNotification(models.Model):
    housing_request_notification_id = models.AutoField(primary_key=True)
    housing_listing_request = models.OneToOneField(HousingListingRequest, on_delete=models.CASCADE,
                                                   db_column='housing_listing_request')
    notification = models.OneToOneField('Notification', on_delete=models.CASCADE, db_column='notification')

    class Meta:
        managed = False
        db_table = 'Housing Listing Request Notification'
        unique_together = (('housing_request_notification_id', 'housing_listing_request', 'notification'),)


# -------------------------------------------------------------------
# Image Model
# -------------------------------------------------------------------
class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_path = models.ImageField(upload_to="housing/")
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, db_column='post', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Image'


# -------------------------------------------------------------------
# Account Model
# -------------------------------------------------------------------
class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=45)
    password = models.BinaryField(max_length=60)
    createdat = models.DateTimeField(db_column='createdAt', default=Now())  # Field name made lowercase.
    email_verified = models.BooleanField(default=False)
    user = models.OneToOneField('User', on_delete=models.CASCADE, db_column='user')

    class Meta:
        managed = False
        db_table = 'Account'
        unique_together = (('account_id', 'user', 'email'),)


# -------------------------------------------------------------------
# Student Account Model
# -------------------------------------------------------------------
class StudentAccount(models.Model):
    student_id = models.AutoField(primary_key=True)
    graduation_month = models.DateTimeField(blank=True, null=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, db_column='account')

    class Meta:
        managed = False
        db_table = 'Student Account'
        unique_together = (('student_id', 'account'),)


# -------------------------------------------------------------------
# Device Model
# -------------------------------------------------------------------
class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=36)

    class Meta:
        managed = False
        db_table = 'Device'
        unique_together = (('device_id', 'uuid'),)


# -------------------------------------------------------------------
# Device Session Model
# -------------------------------------------------------------------
class DeviceSession(models.Model):
    device_session_id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, db_column='device')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='account')
    logged_in_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'Device Session'
        unique_together = (('device_session_id', 'device', 'account'),)


# -------------------------------------------------------------------
# User Device Model
# -------------------------------------------------------------------
class UserDevice(models.Model):
    registered_user = models.OneToOneField('RegisteredUser', models.DO_NOTHING, db_column='registered_user', primary_key=True)
    device = models.ForeignKey('Device', models.DO_NOTHING)
    used_at = models.DateTimeField(default=Now())

    class Meta:
        managed = False
        db_table = 'User Device'
        unique_together = (('registered_user', 'device'),)


# -------------------------------------------------------------------
# Item Posting Model
# -------------------------------------------------------------------
class ItemListingPost(models.Model):
    item_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    post = models.OneToOneField('Post', on_delete=models.CASCADE, db_column='post')
    condition = models.CharField(max_length=45)
    preferred_pay_type = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Item Listing Post'
        unique_together = (('item_id', 'post'),)


# -------------------------------------------------------------------
# Item Listing Request Model
# -------------------------------------------------------------------
class ItemListingRequest(models.Model):
    item_request_id = models.AutoField(primary_key=True)
    createdat = models.DateTimeField(db_column='createdAt', default=Now())  # Field name made lowercase.
    registered_user = models.ForeignKey('RegisteredUser', on_delete=models.CASCADE, db_column='registered_user')
    item_listing = models.ForeignKey('ItemListingPost', on_delete=models.CASCADE, db_column='item_listing')

    class Meta:
        managed = False
        db_table = 'Item Listing Request'
        unique_together = (('item_request_id', 'registered_user', 'item_listing'),)


# -------------------------------------------------------------------
# Item Listing Form Model
# -------------------------------------------------------------------
class ItemListingForm(models.Model):
    form_id = models.AutoField(primary_key=True)
    item_listing_request = models.ForeignKey('ItemListingRequest', on_delete=models.CASCADE,
                                             db_column='item_listing_request')
    registered_user = models.ForeignKey('RegisteredUser', on_delete=models.CASCADE, db_column='registered_user')

    class Meta:
        managed = False
        db_table = 'Item Listing Form'
        unique_together = (('form_id', 'item_listing_request', 'registered_user'),)


# -------------------------------------------------------------------
# Item Listing Request Notification Model
# -------------------------------------------------------------------
class ItemRequestNotification(models.Model):
    item_request_notification_id = models.AutoField(primary_key=True)
    item_listing_request = models.OneToOneField(ItemListingRequest, on_delete=models.CASCADE,
                                                db_column='item_listing_request')
    notification = models.OneToOneField('Notification', on_delete=models.CASCADE, db_column='notification')

    class Meta:
        managed = False
        db_table = 'Item Request Notification'
        unique_together = (('item_request_notification_id', 'item_listing_request', 'notification'),)


# -------------------------------------------------------------------
# Admin Account Model
# -------------------------------------------------------------------
class AdminAccount(models.Model):
    admin_account_id = models.AutoField(primary_key=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, db_column='account')
    position = models.CharField(max_length=45)
    is_approved = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'Admin Account'
        unique_together = (('admin_account_id', 'account', 'position'),)


# -------------------------------------------------------------------
# Super User Account Model
# -------------------------------------------------------------------
class SuperUserAccount(models.Model):
    super_user_id = models.SmallAutoField(primary_key=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, db_column='account')
    is_approved = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'Super User Account'
        unique_together = (('super_user_id', 'account'),)


# -------------------------------------------------------------------
# Organization Model
# -------------------------------------------------------------------
class OrganizationAccount(models.Model):
    organization_id = models.SmallAutoField(primary_key=True)
    admin_account = models.OneToOneField(AdminAccount, on_delete=models.CASCADE, db_column='admin_account')
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Organization Account'
        unique_together = (('organization_id', 'admin_account', 'name'),)


# -------------------------------------------------------------------
# Deaprtment Model
# -------------------------------------------------------------------
class DepartmentAccount(models.Model):
    department_account_id = models.SmallAutoField(primary_key=True)
    admin_account = models.ForeignKey(AdminAccount, on_delete=models.CASCADE, db_column='admin_account')
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Department Account'
        unique_together = (('department_account_id', 'admin_account', 'name'),)


# -------------------------------------------------------------------
# Athletics Model
# -------------------------------------------------------------------
class AthleticsAccount(models.Model):
    athletic_account_id = models.SmallAutoField(primary_key=True)
    admin_account = models.OneToOneField(AdminAccount, on_delete=models.CASCADE, db_column='admin_account')
    sport = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Athletics Account'
        unique_together = (('athletic_account_id', 'admin_account', 'sport'),)


# -------------------------------------------------------------------
# Announcement Model
# -------------------------------------------------------------------
class Announcement(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(AdminAccount, on_delete=models.CASCADE, db_column='admin')
    post = models.OneToOneField(Post, on_delete=models.CASCADE, db_column='post')
    category = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Announcement'
        unique_together = (('announcement_id', 'admin'),)


# -------------------------------------------------------------------
# Address Model
# -------------------------------------------------------------------
class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    zipcode = models.IntegerField()
    street = models.CharField(max_length=90)
    number = models.IntegerField()
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Address'


# -------------------------------------------------------------------
# Restaurant Model
# -------------------------------------------------------------------
class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=60)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, db_column='address', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    open = models.TimeField(blank=True, null=True)
    close = models.TimeField(blank=True, null=True)
    takeout = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'Restaurant'
        unique_together = (('restaurant_id', 'name'),)

# -------------------------------------------------------------------
# Restaurant Model
# -------------------------------------------------------------------
class RestaurantImage(models.Model):
    restauarant_image_id = models.AutoField(primary_key=True)
    image_path = models.CharField(max_length=255)
    restaurant = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='restaurant')

    class Meta:
        managed = False
        db_table = 'Restaurant Image'
        unique_together = (('restauarant_image_id', 'restaurant'),)




# -------------------------------------------------------------------
# Restaurant Request Model
# -------------------------------------------------------------------
class RestaurantRequest(models.Model):
    restaurant_request_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, db_column='address', blank=True, null=True)
    post = models.OneToOneField('Post', on_delete=models.CASCADE, db_column='post')
    open = models.TimeField(blank=True, null=True)
    close = models.TimeField(blank=True, null=True)
    takeout = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'Restaurant Request'
        unique_together = (('restaurant_request_id', 'post'),)


# -------------------------------------------------------------------
# Restaurant Request Notification Model
# -------------------------------------------------------------------
class RestaurantRequestNotification(models.Model):
    restaurant_request_notification = models.AutoField(primary_key=True)
    restaurant_request = models.ForeignKey(RestaurantRequest, on_delete=models.CASCADE, db_column='restaurant_request')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, db_column='notification')

    class Meta:
        managed = False
        db_table = 'Restaurant Request Notification'
        unique_together = (('restaurant_request_notification', 'restaurant_request', 'notification'),)


# ===================================================================
# Restaurant Review Model
# ===================================================================
class RestaurantReview(models.Model):
    restaurant_review_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='restaurant')
    rating = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=60)
    registered_user = models.ForeignKey('RegisteredUser', on_delete=models.CASCADE, db_column='registered_user')

    class Meta:
        managed = False
        db_table = 'Restaurant Review'
        unique_together = (('restaurant_review_id', 'restaurant'),)


# ===================================================================
# Email Verification Model
# ===================================================================
class EmailVerification(models.Model):
    email_verification_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, db_column='account')
    createdat = models.DateTimeField(db_column='createdAt', default=Now())  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Email Verification'
        unique_together = (('email_verification_id', 'account'),)

# ===================================================================
# Vertical Prototype Models
# ===================================================================
# class StudentModel(models.Model):
#     s_id = models.BigAutoField(primary_key=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     sfsu_email = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)
#     datetime = models.DateField(auto_now_add=True)

#     class Meta:
#         db_table = "student"


# class ItemForSaleModel(models.Model):
#     is_id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     item_img = models.ImageField(upload_to='images/')
#     price = models.IntegerField()
#     datetime = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = "item_for_sale"


# class Post(models.Model):
#     title = models.CharField(max_length=70)
#     body = models.TextField()

#     def __str__(self):
#         return self.title
