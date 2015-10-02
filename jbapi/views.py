from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from models import Book
from models import User
from serializers import BookSerializer
from serializers import UserSerializer
import json
import traceback
import re
from django.http import StreamingHttpResponse
from oauth2client import client, crypt
from django.http import HttpResponse

@csrf_exempt
@api_view(['GET','POST'])

####LISTBOOKS FUNCTION######
#GET will list all paopular books according to pagenation
#POST the user_name and you will get the books added by that user

def listbooks(request):
    #connect to our local mongodb
    books = []
    print "About to request Connection"
    db = MongoClient('urkk30b07ae8.ravitejabadisa.koding.io',27017)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']

    if request.method == 'GET':
        #get all books collection
        print "Inside GET"
        required_page= int(request.GET.get('required_page', '1'))
        books_per_page = int(request.GET.get('books_per_page', '4'))
        print required_page
        print books_per_page
        print required_page-1*books_per_page
        
        print "Going into for loop"
        for r in bookCollection.find().skip((required_page-1)*books_per_page).limit(books_per_page):
            #book = Book(r["_id"],r["name"],r["author"],r["image"],r["users"],r,r["sell_price"])
            if(r["status"] == "OK")
                book = Book(r["_id"],r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],[],[])
                books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print request.body

        received_json_data=json.loads(request.body)
        user_name = received_json_data.get("user_name",False)
        required_page = received_json_data.get("required_page",False)
        books_per_page = received_json_data.get("books_per_page",False)
        print "After parsing"
        print user_name
        print required_page
        book_list = userCollection.find({"user_name":user_name})
        print "Array of books is"
        #print  book_list["user_name"]
        #for index in range(len(book_list["books"])):
        for r in book_list :
            print r
            for index in range(len(r["books"])):
                try:
                    if(r["books"][index]["status"] =="OK")
                        book = Book(r["_id"],r["books"][index]["name"],r["books"][index]["description"],r["books"][index]["published_date"],r["books"][index]["status"],r["books"][index]["author"],r["books"][index]["image"],[],r["books"][index]["rent_price"],r["books"][index]["sell_price"])
                    #print r["books"][index]["author"]
                    #print book_list["books"][index]["author"]
                except Exception as e:
                    print "Exception is"
                    print(e)
            books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
        
        
##SEARCHBOOK FUNCTION#####
#GET for a serach_parameter it can be anythiong like book name or author or description
#If user clicks on one of the results from the above get then POST the book name and you will get the list of users having that book
@api_view(['GET','POST'])
def searchbook(request):
    #connect to our local mongodb
    books = []
    users = []
    
    print "About to request Connection"
    db = MongoClient('urkk30b07ae8.ravitejabadisa.koding.io',27017)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']

    if request.method == 'GET':
        #get all books collection
        print "Inside GET"
        search_parameter = request.GET.get('search_parameter', '')
        required_page= int(request.GET.get('required_page', '1'))
        books_per_page = int(request.GET.get('books_per_page', '4'))
        
        print search_parameter
        print required_page
        print books_per_page
        print "Going into for loop"
        #temp =*
        new_search_parameter = "/"+search_parameter+"/"
        print "REGEX IS"
        regex = re.compile(r'.*'+search_parameter+'.*')
        print regex
        #for r in bookCollection.find({"name":{'$regex':new_search_parameter}}):#.skip((required_page-1)*books_per_page).limit(books_per_page):
        #print bookCollection.find({"name":{'$regex':'/C/'}})
        #for r in bookCollection.find({"name":{"$regex":new_search_parameter}}):#.skip((required_page-1)*books_per_page).limit(books_per_page):
        for r in bookCollection.find({"name":regex}).skip((required_page-1)*books_per_page).limit(books_per_page):
            print r
            if(r["status"] =="OK")
                book = Book(r["_id"],r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],r["rent_price"],r["sell_price"])
                books.append(book)
            
        for r in bookCollection.find({"author":regex}).skip((required_page-1)*books_per_page).limit(books_per_page):
            if(r["status"] =="OK")
                book = Book(r["_id"],r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],r["rent_price"],r["sell_price"])
                books.append(book)
            
        for r in bookCollection.find({"image":regex}).skip((required_page-1)*books_per_page).limit(books_per_page):
            if(r["status"] =="OK")
                book = Book(r["_id"],r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],r["rent_price"],r["sell_price"])
                books.append(book)    
        print "before serializing"
        serializedList = BookSerializer(books, many=True)
        #print serializedList.data
        return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print request.body
        received_json_data=json.loads(request.body)
        
        user_name = received_json_data.get("user_name",False)
        book_list = userCollection.find({"user_name":user_name})
        print "Array of books is"
        #print  book_list["user_name"]
        #for index in range(len(book_list["books"])):
        for r in book_list :
            print r
            for index in range(len(r["books"])):
                try:
                    if(r["books"][index]["status"] ==1)
                        book = Book(r["_id"],r["books"][index]["name"],r["books"][index]["description"],r["books"][index]["published_date"],r["books"][index]["status"],r["books"][index]["author"],r["books"][index]["image"],[],r["books"][index]["rent_price"],r["books"][index]["sell_price"])
                        #print r["books"][index]["author"]
                #print book_list["books"][index]["author"]
                except Exception as e:
                    print "Exception is"
                    print(e)
            books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
        

####ADDBOOK FUNCTION####
#GET method is useless as of now
#POST METHOD IS THE ACTUAL LOGIC CONTAINING ADD BOOK
@csrf_exempt        
def addbook(request):
    #connect to our local mongodb
    print "About to request Connection"
    db = MongoClient('urkk30b07ae8.ravitejabadisa.koding.io',27017)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']

    if request.method == 'GET':
        #get all books collection
        print "Inside GET"
        print "Going into for loop"
        for r in bookCollection.find():
            if(r["status"] == "OK")
                book = Book(r["_id"],r["name"],r["description"],r["published_date"],r["status"],r["author"],r["image"],r["users"],[],[])
                books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print request.body
        received_json_data=json.loads(request.body)
        name = received_json_data.get("name",False)
        description = received_json_data.get("description",False)
        published_date = received_json_data.get("published_date",False)
        status = received_json_data.get("status",False)
        author = received_json_data.get("author",False)
        image = received_json_data.get("image",False)
        sell_price = received_json_data.get("sell_price",False)
        rent_price = received_json_data.get("rent_price",False)
        print name
        print author
        user_name = received_json_data.get("user_name",False)
         = received_json_data.get("home_longitude",False)
         = received_json_data.get("home_latitude",False)
         = received_json_data.get("office_longitude",False)
         = received_json_data.get("office_latitude",False)
        
        print "Going into try catch block to insert books"
        
        try:
            #FInd user details of that user_name
            user_details = userCollection.find({"user_name":user_name})
            
            
            home_longitude = user_details["home_longitude"]
            home_latitude = user_details["home_latitude"]
            office_longitude = user_details["office_longitude"]
            office_latitude = user_details["office_latitude"]
            
            
            
            #bookCollection.insert({"name" : name, "author": author})
            bookCollection.update({"name" : name, "author": author,"image":image,"description":description,"published_date":published_date,"status":status},
                                    {'$push':
                                        {"users":{"user_name": user_name,"home_longitude": home_longitude,"home_latitude": home_latitude,"office_longitude": office_longitude,"office_latitude": office_latitude,"sell_price": sell_price,"rent_price": rent_price }}
                                    },True)
                                    
            userCollection.update({"user_name":user_name,"home_longitude": home_longitude,"home_latitude": home_latitude,"office_longitude": office_longitude,"office_latitude": office_latitude},
                                    {'$push': {"books":{"name": name,"author": author,"image": image,"sell_price": sell_price,"rent_price": rent_price }}
                                    },True)
        except Exception as e:
            print(e)
            return HttpResponse("false" )
        return HttpResponse("OK")

@csrf_exempt        
def authenticating(request):
    #connect to our local mongodb
    print "About to Authenticate user"
    if request.method == 'GET':
        #get our collection
        print "Inside GET"
        return HttpResponse("OK")
    elif request.method == 'POST':
        #get data from the request and insert the record
        print "Inside POST"
        print request.body
        print "PRINTED PAYLOAD"
        received_json_data=json.loads(request.body)
        token = received_json_data.get("token",False)
        print token
        CLIENT_ID = "979314773329-m6j6e9la8u2o9rt15q8655uqnuuolko5.apps.googleusercontent.com"
        ANDROID_CLIENT_ID = "979314773329-e7kl7cavu9e85hclbbfscruhmtb4t685.apps.googleusercontent.com"
        IOS_CLIENT_ID = ' '
        WEB_CLIENT_ID = ' '
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)
            if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            if idinfo['hd'] != APPS_DOMAIN_NAME:
                raise crypt.AppIdentityError("Wrong hosted domain.")
        except crypt.AppIdentityError:
            traceback.print_exc()
            # Invalid token
            print "Returning Failure of user auth"
            return HttpResponse("ERROR")
        userid = idinfo['sub']
        print "Returning Success of user auth"    
        return HttpResponse(userid)
    
""" COMMENTED OUT
def perform_exchange(request):
    #connect to our local mongodb
    print "About to request Connection"
    db = MongoClient('urkk30b07ae8.ravitejabadisa.koding.io',27017)
    #get a connection to our database
    print "Opening Jillion books DB"
    dbconn = db.jb
    print "Opening collection books"
    bookCollection = dbconn['books']
    userCollection = dbconn['users']
    transactionCollection = dbconn['transactions']

    if request.method == 'GET':
        #get all books collection
        print "Inside GET"
        print "Going into for loop"
        for r in bookCollection.find():
            book = Book(r["_id"],r["name"],r["author"],r["image"],r["users"])
            books.append(book)
        serializedList = BookSerializer(books, many=True)
        return Response(serializedList.data)
    elif request.method == 'POST':
        #get data from the request and insert the record
        print request.body
        received_json_data=json.loads(request.body)
        name = received_json_data.get("name",False)
        author = received_json_data.get("author",False)
        image = received_json_data.get("image",False)
        print name
        print author
        user_name = received_json_data.get("user_name",False)
        longitude = received_json_data.get("longitude",False)
        latitude = received_json_data.get("latitude",False)
        print "Going into try catch block to insert books"
        
        try:
            #bookCollection.insert({"name" : name, "author": author})
            bookCollection.update({"name" : name, "author": author,"image":image},{'$push': {"users":{"user_name": user_name,"longitude": longitude,"latitude": latitude }}},True)
            userCollection.update({"user_name":user_name,"longitude": longitude,"latitude": latitude},{'$push': {"books":{"name": name,"author": author,"image": image }}},True)
        except Exception as e:
            print(e)
            return HttpResponse("false" )
        return HttpResponse("OK")

@csrf_exempt        
def authenticating(request):
    #connect to our local mongodb
    print "About to Authenticate user"
    if request.method == 'GET':
        #get our collection
        print "Inside GET"
        return HttpResponse("OK")
    elif request.method == 'POST':
        #get data from the request and insert the record
        print "Inside POST"
        print request.body
        print "PRINTED PAYLOAD"
        received_json_data=json.loads(request.body)
        token = received_json_data.get("token",False)
        print token
        CLIENT_ID = "979314773329-m6j6e9la8u2o9rt15q8655uqnuuolko5.apps.googleusercontent.com"
        ANDROID_CLIENT_ID = "979314773329-e7kl7cavu9e85hclbbfscruhmtb4t685.apps.googleusercontent.com"
        IOS_CLIENT_ID = ' '
        WEB_CLIENT_ID = ' '
        try:
            idinfo = client.verify_id_token(token, CLIENT_ID)
            if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            if idinfo['hd'] != APPS_DOMAIN_NAME:
                raise crypt.AppIdentityError("Wrong hosted domain.")
        except crypt.AppIdentityError:
            traceback.print_exc()
            # Invalid token
            print "Returning Failure of user auth"
            return HttpResponse("ERROR")
        userid = idinfo['sub']
        print "Returning Success of user auth"    
        return HttpResponse(userid)
"""
