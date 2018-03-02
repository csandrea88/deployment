from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import datetime 
from datetime import date
from datetime import datetime



class UsersManager(models.Manager):
    
    def register_validator(self, postData):
    
        # create a regular expression object that we can use run operations on
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        errors = []
    
        fname = postData['fname']
        lname = postData['lname']
        email = postData['email']
        bday = postData['bday']
        password = postData['password']
        cpassword = postData['cpassword']

        #print "here is the form data: {}".format(name)

        #Users Table Validations

        #First name
        if len(fname) < 1:
            errors.append("Registration: First Name is required!")
                
        if len(fname) < 2:
            errors.append("Registration: First Name must have at least 2 letters!")
                
        if not fname.isalpha():
            errors.append("Registration: First Name must be alphabetic!")
                

        #Last Name
        if len(lname) < 1:
            errors.append("Registration: Last Name is required!")
                
        if len(lname) < 3:
            errors.append("Registration: Last Name must have at least 2 letters!")
                
        if not lname.isalpha():
            errors.append("Registration: Last Name must be alphabetic!")
                

        #Email
        if len(email) < 1:
            errors.append("Registration: Email is required!")
            
        if not EMAIL_REGEX.match(email):
            errors.append("Registration: Email is not a valid email!")
            
        #Bday
        if len(bday) < 1:
            errors.append("Registration: Birthday is required!")
        
        #Password
        if len(password) < 1:
            errors.append("Registration: Password is required!")
            
        if len(password) < 8:
            errors.append("Registration: Password must be at least 8 characters long!")
            

        #Confirm Password
        if len(cpassword) < 1:
            errors.append("Registration: Confim password is required!")
            
        if cpassword != password:
            errors.append("Registration: Confim password does not match Password!")
            
        reg_passhash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        if Users.objects.filter(email = postData['email']).count() > 0:
        
            errors.append("Registration: Your email already exists")

        print "len(errors): {}".format(len(errors))
        if len(errors) == 0: 
            newuser = Users.objects.create(
                first_name=postData['fname'], 
                last_name=postData['lname'],
                email=postData['email'],
                Bday =postData['bday'],
                Password = reg_passhash1
            )
            return newuser

        print "Users table dump: {}".format (Users.objects.all())
        return errors

    def login_validator(self, postData):
        print postData
        
        
        # create a regular expression object that we can use run operations on
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        errors = []
        print(postData)
        email = postData['email']
        password = postData['password']
        
        #Email
        if len(email) < 1:
            errors.append("Login: Email is required!")
            
        if not EMAIL_REGEX.match(email):
            errors.append("Login: Email is not a valid email!")
        
        #Password
        if len(password) < 1:
            errors.append("Login: Password is required!")
            
        if len(password) < 8:
            errors.append("Login: Password must be at least 8 characters long!")

        return errors


class QuotesManager(models.Manager):
    def Quotes_validator(self, postData): 
        print "in quootes manager"
        errors = []
    
        addmessage = postData['addmessage']
        addby = postData['addby']

        #adddate_dateobj = datetime.strptime(adddate, '%Y-%m-%d')
        
        print "addmessage length:", len(addmessage)
        if len(addmessage) < 1:
            errors.append("Quote message is required!")
        if len(addmessage) < 11:
            errors.append("Quote message must be at least 10 charachters!")
        
        # print adddate_dateobj, date.today()
        # if adddate < date.today():
        #     errors.append("Appts: Appointment date must be current day or later!")
        # print "after add date len check" 
 
        if len(addby) < 1:
            errors.append("quoted by is required")
        if len(addby) < 3:
            errors.append("quoted by must be at least 3 charachters")
        
#         #appt_date = datetime.strptime(adddate, '%Y-%m-%d').date() 
#         #appt_time = datetime.strptime(addtime, "%H:%M").time() 

#         #print "appt_date and type:", appt_date, type(appt_date)
#         #print "appt_time and type", appt_time, type(appt_time) 

#         #if appt_date < date.today():
#         #    print "appt_date is less than current date"
#         #    errors.append("Appts: Appointment date must be current day or later!")
            
        return errors   
        

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    Bday = models.DateField('%Y-%m-%d', auto_now=False, auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UsersManager()

class Quotes(models.Model):
    message = models.CharField(max_length=255)
    by = models.CharField(max_length=255)
    #date = models.CharField(max_length=255)
    #date = models.DateField('%Y-%m-%d', auto_now=False, auto_now_add=False)
    #time = models.TimeField('%H:%M', auto_now=False, auto_now_add=False)
    #user = models.ForeignKey(Users, related_name="appts",null=True)
    myList = models.ManyToManyField(Users, related_name="Quotes_Listed")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuotesManager()


 
