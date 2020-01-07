# python imports
import datetime
import requests
import json
import urllib, urllib.request, urllib.error
from operator import itemgetter 
from horsesDAO import horseDAO
import time
import betfairApi as bf 

# call betfair api and add horses into the mysql database from the upcoming races
bf.getUpcHorses()
