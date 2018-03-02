from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
import datetime 
from datetime import date
from datetime import datetime


def index(request):
    return render(request,'belt2/index.html')

def register(request):

    reg_errors = Users.objects.register_validator(request.POST)
    # print "Are there any errors: {}".format(reg_errors)
    # print "TYPE OF THING IS {}".format(type(reg_errors))
    if type(reg_errors) == list:
        for error in reg_errors:
            messages.error(request,error)
        return redirect ("/")
    else:
        request.session['userid'] = reg_errors.id 
        request.session['first_name'] = reg_errors.first_name

        return redirect ("/belt2")

def login(request):  
    print "in login"
    login_errors = Users.objects.login_validator(request.POST)

    if len(login_errors) > 0:
        for error in login_errors:
           messages.error(request,error)
        return redirect("/")

    login = Users.objects.filter(email = request.POST['email'])

    if len(login) == 0:
        login_errors.append("Login: Email does not exist, invalid login")
        for error in login_errors:
            messages.error(request,error)
        return redirect("/") 

    elif len(login) == 1:
        User_Password = login[0].Password

        User_id = login[0].id
        first_name = login[0].first_name

        print User_id, User_Password, request.POST['password']
        if bcrypt.checkpw(request.POST['password'].encode(), User_Password.encode()) == True:
            request.session['userid'] = User_id
            request.session['first_name'] = first_name
            return redirect("/belt2")

        else:
            login_errors.append("Login: Invalid Password")
            if login_errors > 0:
                for error in login_errors:
                    messages.error(request,error)
                return redirect("/")     

def logout(request):
    del request.session['userid'] 
    del request.session['first_name'] 
    return redirect ("/index") 



# appt Routes
def belt2(request):
    print "i am  in appts route"
    
    context = {
        #"quotes": Quotes.objects.all(),
        "quotes": Quotes.objects.all().exclude(myList=Users.objects.get(id = request.session['userid'])),
        "myquotes": Quotes.objects.filter(myList=Users.objects.get(id=request.session['userid']))
    }
    return render(request,'belt2/belt2.html', context)


def add(request):
    print "in add view"

    add_errors = Quotes.objects.Quotes_validator(request.POST)

    #appt_date = datetime.strptime(request.POST['adddate'], '%Y-%m-%d').date()
    #print "appt_date and its type: ", appt_date, type(appt_date)

    #verification that appot info is not on the database
    
    if len(add_errors) == 0: 
        newquote = Quotes.objects.create(
            message=request.POST['addmessage'], 
            by=request.POST['addby']
        )
    # print "newquote:", newquote, len(add_errors)
    if len(add_errors) > 0:
        for error in add_errors:
            messages.error(request,error)

    print "about to redirect to belt2"   
    return redirect("/belt2")

def show(request,id):
    quote = Quotes.objects.get(id=id)
    #request.session['quote']

    context = {
        "quotes": Quotes.objects.filter(by=quote.by),
        "quoteby": quote.by
    }
    return render(request,'belt2/show.html', context)    

def listadd(request, id):
    
    print "in listadd"

    user = Users.objects.get(id=request.session['userid'])
    
    quote = Quotes.objects.get(id=id)
    
    quote.myList.add(user)
    quote.save()

    return redirect("/belt2")


def listadd(request, id):
    
    print "in listadd"

    user = Users.objects.get(id=request.session['userid'])
    
    quote = Quotes.objects.get(id=id)
    
    quote.myList.add(user)
    quote.save()

    return redirect("/belt2")


def listremove(request, id):
    
    print "in listadd"

    user = Users.objects.get(id=request.session['userid'])
    
    quote = Quotes.objects.get(id=id)
    
    quote.myList.remove(user)
    #quote.save()

    return redirect("/belt2")


