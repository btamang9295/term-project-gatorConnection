"""
Models.py:

This python script what allows us to connect the MySQL database 
tables. You can connect the tables through the name and the table 
items of that table.
"""

from django.db import models



class AlecTestInsert(models.Model):
    user_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)

    class Meta:
        db_table= "sample_alec_table"




class AngeloTestInsert(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    class Meta:
        db_table="sample_angelo_table"