# drProjectDec2019

#### Data Representation Project - December 2019


This project uses the Betfair API
<br>It contains:
  1. A parent folder: containing the requirements.txt file for the Python virtual environment and subfolders for othe sections.
  2. A html folder: all html pages are located here.
  3. A server foloder: containing
  4. A Certificate folder for the Betfair Certs.
  5. The project requries a mySQL database

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

#### Further Notes

##### 1. Parent Folder:
  1.  The parent folder also contains: 
  1a.    
  3. 
  4. 


##### 2. Html Folder:
  1. A html folder contains 
  2.  
  3. 
  4. 
  5. 

##### 3. The Server Folder
  1.  The parent folder also contains: 
  1a.    
  3. 
  4. 
  
 ##### 4. A Certificate folder for the Betfair Certs
  1.  The parent folder also contains: 
  1a.    
  3. 
  4. 
  
  
  ##### 5.  mySQL database
  1.  Update the server/dbconfig.cfg file for your mySQL login credentials and database
  2.  Create a horse table in your dabase with the command
      
  create table horse ( id int NOT NULL, name varchar(300), age varchar(300), sex varchar(30), owner varchar(300), trainer varchar(300), form varchar(300), PRIMARY KEY(id) );
  
  3. 
  4. 
