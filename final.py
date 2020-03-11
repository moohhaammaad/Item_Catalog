#!/usr/bin/env python2.7

#start of configuration code
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random, string  #used to create a pseudo-random string to identify each session.
from database import Base, Restaurant, MenuItem, User
#IMPORTS FOR gconnect
from oauth2client.client import flow_from_clientsecrets  #to store client id & cleint secret
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response  # convert the return value from a function into a real response 
import requests
from functools import wraps

app = Flask(__name__)

#gconnect
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
    
#connect to the database
engine = create_engine('sqlite:///restaurantmenuwithusers.db') 
Base.metadata.bind = engine   #bind classes to each others.

DBSession = sessionmaker(bind=engine)  #communication between code executions& engine.
session = DBSession()

def check_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function        

# JSON API ENDPOINT TO RETURN ALL MENUS IN THE RESTAURANT 
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])  #The loop here to serialize all database entries.

#JSON API ENDPOINTS
#1) JSON API ENDPOINT TO RETURN ALL RESTAURANTS IN THE DATABASE
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[i.serialize for i in restaurants])
#2) JSON API ENDPOINT TO RETURN A SPECIFIC MENU IN THE RESTAURANT
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)
    
#3) Show all menu items of a restaurant 
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicmenu.html', restaurant=restaurant, 
                                items=items, creator = creator)
    else:
        return render_template('menu.html', restaurant=restaurant,
                                 items=items, creator = creator)

# Show all restaurants
@app.route('/')                
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant.html', restaurants=restaurants)
    
# Add a new item in the menu of restaurant
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
@check_login
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id, 
                           user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New item added to the menu")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('additem.html', restaurant_id=restaurant_id)

#Edit an item in the menu
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
@check_login
def editMenuItem(restaurant_id, menu_id, methods=['GET', 'POST']):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if editedItem.user_id != login_session['user_id']:  #check if the user is the author
        return "<script>function myFunction() {alert('You are not authorized to\
                 edit this item.');}</script><body onload='myFunction()''>" 
    else:                
        if request.method == 'POST':
            if request.form['name']:
                editedItem.name = request.form['name']
                session.add(editedItem)
                session.commit()
                flash("The item is Edited successfully!")
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
        # THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES WHICH
        # SHOULD USE IN EDITMENUITEM TEMPLATE
            return render_template('edititem.html', restaurant_id=restaurant_id,
                                    menu_id=menu_id, item=editedItem)


#Delete an item from the menu
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
@check_login
def deleteMenuItem(restaurant_id, menu_id, methods=['GET', 'POST']):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if itemToDelete.user_id != login_session['user_id']:  #check if the user is the author
        return "<script>function myFunction() {alert('You are not authorized to\
                 delete this item.');}</script><body onload='myFunction()''>"
    else:             
        if request.method == 'POST':
            session.delete(itemToDelete)
            session.commit()
            flash("The item has Deleted")
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        else:
            return render_template('deleteitem.html', restaurant_id=restaurant_id,
                                    menu_id=menu_id, item=itemToDelete)

# Create anti-forgery state token (authentication)
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))  # state is 32 letters& is mixed of Upper case letters& digits
    login_session['state'] = state  #store state variable in the login session object
    return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    #Ensure that the token which sent to the server by the cleint 
    #is the same which te server sent to the cleint
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data  #In case if statement isn't true collect code from server with request.data function.
    #Try & use this code & ecxchange it for a cardentials object
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)  #if all previous steps goes well, google response will be this object
    #If any error happen along the way send the response as JSON object
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response    

    #verify that the access token is true.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    #JSON GET request containing url & access token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If the result contains any errors 
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    
    #check if user is already logged in 
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response       
    
    # In case all of if statements weren't true.
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info by G+ API
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()  

    # store data
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    #see if user exists, if not make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id    
    
    # response to know the user's his name and pic
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id  # return the user_id of the new user created.

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

if __name__ == '__main__':  #make sure if the script directly running from the python interpreter
    app.secret_key = 'super_secret_key'  #create sessions to users by flask
    app.debug = True        # restart the server after modifying the code
    app.run(host='0.0.0.0', port=5000)  #run on localhost