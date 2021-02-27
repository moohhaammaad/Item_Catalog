Item Catalog Project  
---------------------
-It is an application that provides a list of items within a variety of categories as well as provide a user
registration and authentication system. Registered users will have the ability to add, edit and delete their own items.
-This web application use the Python framework Flask along with implementing third-party OAuth authentication.

Prerequisites
-------------
1- you should have a Python software onto your computer if you don't have it,
   check this link to setup it (https://www.python.org/downloads/) .

2- you should have a virtual machine , vagrant tool & virtual box if you don't have them ,
   it will be a good reference from udacity to install them ,
   check this link ( https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/
                    modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/
                    concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0 ) .

3- you should have a git bash terminal onto your computer also if not found,
   check this link to download & setup it (https://git-scm.com/downloads) .

4- you should have a browser on your PC, Google chrome is recommended.

Description
-----------
-In this sample project, the homepage(http://localhost:5000/restaurant/) displays all current restaurants we have.
-Selecting a specific restaurant from the list shows you all the menu items available for that restaurant.
-All users can show the restaurant(http://localhost:5000/restaurant/) & menu(http://localhost:5000/restaurants/number/) pages,
 but the authorized users only have the ability to make changes on the menu item
 as (add new item to menu, edit or delete a specific item from the menu)
 After logging in with Gmail, the user has the ability to add, update, or delete any item . 
-This application provides a three JSON endpoints which retrieve only the pure data quickly & without any styles on the page : 
   1) JSON API ENDPOINT TO RETURN ALL RESTAURANTS IN THE DATABASE, which exist in this path (http://localhost:5000/restaurants/JSON)
   2) JSON API ENDPOINT TO RETURN A SPECIFIC MENU IN THE RESTAURANT, which exist in this 
      path (http://localhost:5000/restaurants/restaurant no./menu/menu no./JSON)  
   3) JSON API ENDPOINT TO RETURN ALL MENUS IN SPECIFIC RESTAURANT , which exist in this 
      path (http://localhost:5000/restaurants/restaurant no./menu/JSON)  
-In the end, Currently I have applied:
   1) JSON endpoint as i say in the prvious point.
   2) CRUD approach : Read in both restaurant(http://localhost:5000/restaurant/) & menu(http://localhost:5000/restaurants/number/) pages,
                      Add, Update & delete in the menu(http://localhost:5000/restaurants/number/) page.
   3) Authentication & Authorization apprroaches also while visiting the menu(http://localhost:5000/restaurants/number/) page.
       

Guidelines
----------
after making sure you have python, virtual machine,vagrant tool, virtual box, Git bash & browser on your computer 
-you can go directly to test the project through following this steps :
   1) From your Git bash terminal, inside the vagrant subdirectory, run the command vagrant up.
   2) Run vagrant ssh to Log into the Linux VM.
   3) Inside the VM, change directory to /vagrant then cd to finalproj and look around with ls.
   4) setup the database on your machine by running python database.py to create the database and relations.
   5) run python fill_db.py to fill the database with data.
   6) run python final.py .
   7) open the web browser and visit this url (http://localhost:5000/restaurant/) to show all restaurants we have. 
   8) choose any of these restaurants to display all of its menu items.
   9) if you need to add a new item to this menu or edit any existing item or delete any item from the menu you should 
      sign in with your gmail first, so when you press on Add New Item, Edit or Delete buttons
      You will be taken to the gmail login page sign in then try to Add New Item, Edit or Delete items you will be able to do
      this after signing in. 
   10) After finishing all operations you need & you want to sign out from gmail you will find a link next to Add New Item button
       in the top right of the menu page press click on it & you will be signed out from Gmail .
   11) If you need to retrieve the data which exist in the database only (JSON endpoints) then you should visit these links :
       - (http://localhost:5000/restaurants/JSON) It's a JSON API ENDPOINT TO RETURN ALL RESTAURANTS IN THE DATABASE.
       - (http://localhost:5000/restaurants/restaurant no./menu/menu no./JSON) It's a JSON API ENDPOINT TO RETURN A SPECIFIC MENU IN THE RESTAURANT. 
       - (http://localhost:5000/restaurants/restaurant no./menu/JSON) It's a JSON API ENDPOINT TO RETURN ALL MENUS IN SPECIFIC RESTAURANT     
 
   12) If you back to Git bash& type exit (or Ctrl-D) at the shell prompt inside the VM, you will be logged out, 
       and put back into your host computer's shell. To log back in,
       make sure you're in the same directory and type vagrant ssh again,
       If you reboot your computer or type vagrant halt, you will need to run vagrant up to restart the VM.


Notes
-----
I have used the Udacity database which was provided for this project and followed much steps in videos instructions,
to make this project as much as possible, To build a project that works efficiently. 

Bugs and errors
---------------
if you have any error please make sure you have all of the prerequisites and followed the
guidelines correctly. if you still facing a problem contact with us 
on this mail : `mohamedahmed.mmes@gmail.com `


Built With 
----------
##### Item Cataloge project built with :
*_sqlalchemy_: we used it to build the database & do all queries we need.
* _Python 2_ : we used it to code our program .
 

Copyright and license 
---------------------
`Copyright (c)` [2017] [Mohammad Ahmed]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Item Catalog project"), 
to deal in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
