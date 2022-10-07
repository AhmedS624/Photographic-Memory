# Photographic Memory
#### Video Demo:  <https://youtu.be/sxXAgOfb99o>
#### Description:A program that lets you memorize difficult concepts with pictures


Do you know what is a mind palace or the method of loci or memory journey
it is a strategy for memory enhancment,which uses vusualization of familiar spatial environments in order to engance the recall of information
you can read more about it here:

https://en.wikipedia.org/wiki/Method_of_loci

but basicly this webapp is designed to help you optimize your memorizing of information using this very strategy

How does it work 
simply you choose your palace (the physical space to put your info you want memorized in) it could be your home your way to work even your own body
then you select checkpoint it is recomended to not assign more then necccesarry for exmple if the palace is your home assign 5 checkpoints per room

Example
Palace : home
checkpoint 1: door 
chekpoint 2: sofa
checkpint 3: TV
...etc

Then you make the cards(info) now this is the fun parn as you let your imagination run wild to turn your information into into a picture or a short story

Then assign it to a checkpoint

let's take the word Quintessential for example when I see this word I see the "Queen" of England (RIP) with a red full bag of "essential" stuff

Now to put that mind image in a checkpoint

Palace : home.
checkpoint 1: door card Quintessential = Queen + essential Explanation: I pass by the Queen standing at the door with her red bag full of essentials
              and she calls me a typical human
              (the word quintessential means typical)
              
Now try forgetting that

This method is like a cheat to studing as you are having fun creating and also memorizing even better than the traditional way

# Now that I expalined the idea behind it let's get to the nitty gritty stuff

This project is made with the Flask module so it has(static,templates and other files for the backend like .py files and a database)

the folder Photographic memory has on pakage "final_porject" and a py file to run the app 

the pakage has the meat and bones of the project first the static folder it has(the style sheet,script sheet and a photos folder)

the style sheet for styling

the script.js file which contains javascript for some functionallty
like the photo apearing when you uploade it and the expanding and collapsing of the cards

photos folder

the photos you upload are saved in this folder with thier names saved in the database

After that we have
# the templates folder

basaclly all the pages on the site let't start from the top

# browse-cards.html,browse-palaces 

these two do the same job they get info from the data base and do a for loop on it to display the cards/palaces to the user

# cards.html , select_palace.html
you can acess this page after you pass by select_palace.html(which is just a select menu for all the palaces you added to the database)
after you choose the palace to add your cards into you get to this page which is a form that contains a select file field to upload your photo that only accepts .jpg and .png files
then  concept and explanation are text then you choose your checkpoint based on the palace you choose earlier then sumit button

# home.html

the introdution page that show you how this app works and how it is designed to be used
# layout.html
the basic layout of all the pages and the nav bar
# login.html , register.html
forms to register and login the the user
# palace.html
when you want to create a palace you first meet this page which asks for the name of your palace the redirects you to routes.html
# routes.html
this asks you for each check point in your palace and displays them one by one as you add them

that concludes the tamplates folder

# .py files
# __init__.py
the setup and initalization of the app

# forms.py
using flask.wtforms here to make the essential forms like the loign and register forms as well as the cards form and select palace
# functions 
this file contains two functions I made to make it easier to get info from the database
# Models.py
since I used SQLAlchemy with sqlite I made the tables in this file and it was the right choice as it made easier to change the tables when needed
# routes.py
the backbone of this app it containst all the routes and functions that run in the backend

# other files

# database.db
a sqlite data base that stores the data for each user thier cards and palaces
# garbage_code 
somtime I'd like to experiment with somthing I don't like it so I throw the code here cause when I get stuck somtimes I look in it and behold the soultion to may problems infront of me (or atleast some instpiration)
# requirements.txt 
required modules that had to be on my device

this concludes this read me file
thanks for reading 
This was CS50

