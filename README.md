# drProjectDec2019

#### Data Representation Project - December 2019


This project uses the Betfair API
<br>It contains:
  1. A parent folder: containing the requirements.txt file for the Python virtual environment and subfolders for othe sections.
  2. A html folder: all html pages are located here.
  3. A server foloder: containing
  4. A Certificate folder for the Betfair Certs.
  5. The project requries a mySQL database


#### How to
To run the server on linux you need to 
* Run the virtual environment:
  * python -m venv venv # create the virtual environment
  * source venv/bin/activate # activate it
  * pip install -r requirements.txt # load the required packages to the environment
* Update credentials:
  * update the server/dbconfig.cfg file for your local database details (ensure the database contains the horse table see 5a below.
  * check and update credentials if necessary for Api logins and login keys paths at the top of the betfairApi.py
  * pip install -r requirements.txt # load the required pages
  * Run the flask server(from the server folder):
  * export FLASK_DEBUG=1 # update the environment variables
  * export FLASK_APP=server 
  * flask run
  
  To update the database when the table is created and config files are updated in your database from the server folder
   * python updatedb.py
  
  The logins and session login are not set up yet, but to use the login from login.html you must use all three credentials:
  * username:   Andrew 
  * email:      andrewb@gmail.com
  * password    AndrewB


#### Further Notes

##### 1. Parent Folder:
  1.  The parent folder also contains APIReferenceGuide-Offline.pdf. This is a reference guide for the betfair api.

##### 2. Html Folder:
  1. The logins for the login.html page are above in the how to section. Proper Authentication with redirect and sessions not set up yet. The user credentials are stored in the html page.
  2. home.html is redirected from the login.html.
  3. horseviewer.html mirrors the bookviewer example.
  4. The buttons on this page pull their information from the betfair api using functions in  betfairApi.py.
 

##### 3. The Server Folder
  1.  horsesDAO.py: is similar to bookDAO.py. I added a createAll function. 
  2.  dbconfig.py: the database credentials.
  3.  dbupdate.py:  use this to populate the horses database.
  4.  server.py:  a straightforward flask server, i added functions for the api calls.
  5.  betfairAPI.py: see below.
  
 betfairAPI.py
 * It has 4 sections:
          Login credentials
          Betfair Variables
          Support Functions: these are used by the API call functions.
          API Call functions.
          
 * getEvents(): calls the race meeting info.
 * getUpcRaces(): uses getEvents and calls the races and horse info from the api
 * getUpcHorses(): this is used to populate the horses table in the database. It calls getUpcRaces for the API info. It is complicated slightly by the work to avoid duplicates. Horses can appear more than once in the API, and could already exist in the database.
    
 ##### 4. A Certificate folder for the Betfair Certs
My keys should work, from their current location. 
In betfairApi.py
# Update cert paths to your own and correct location
crtjb = '../Certificate/client-2048.crt'
keyjb = '../Certificate/client-2048.key'

This folder contains the betfair keys. To get your own keys you follow the process in the link below:
https://docs.developer.betfair.com/display/1smk3cen4v3lu3yomq5qye0ni/Certificate+Generation+With+XCA

The keys are used to get the session token when logging in to the API.

  
  
  ##### 5.  mySQL database
  1.  Update the server/dbconfig.cfg file for your mySQL login credentials and database
  2.  Create a horse table in your dabase with the command
      
  create table horse ( id int NOT NULL, name varchar(300), age varchar(300), sex varchar(30), owner varchar(300), trainer varchar(300), form varchar(300), PRIMARY KEY(id) );
  
  3. If the updatedb.py has timeout errors. In the betfairApi.py update 
  horses = (horselist)  to horses = (horselist[0:20]) in the 3rd last line of the getUpcHorses() function.
 
