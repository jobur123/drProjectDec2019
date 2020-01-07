# This program interacts with the betfairApi
# The functions are called from both the server.py and updatedb.py
# python imports
import datetime
import requests
import json
import urllib, urllib.request, urllib.error
from operator import itemgetter 
from horsesDAO import horseDAO
import time


# Betfair varialbes - update where necessary
# Login credentials update where necessary
payload = 'username=drProjJobur&password=annaMicg1'
my_app_key = "Hdosy89LLwLq5hvu"
# Update cert paths to your own and correct location
crtjb = '/home/jobur/da/dr/project/Certificate/client-2048.crt'
keyjb = '/home/jobur/da/dr/project/Certificate/client-2048.key'


# API variables

# urls
bet_url = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
login_url = 'https://identitysso-cert.betfair.com/api/certlogin'

# return SOID and headers through functions as SSOID updates regularly
def getSsoid():
  login_headers = {'X-Application': my_app_key, 'Content-Type': 'application/x-www-form-urlencoded'}
  resp = requests.post('https://identitysso-cert.betfair.com/api/certlogin', data=payload, cert=(crtjb, keyjb), headers=login_headers)
  resp_json = resp.json()
  SSOID = resp_json['sessionToken']
  return SSOID

# header
def getheader():
  headers = {'X-Application': my_app_key, 'X-Authentication': getSsoid(),'Content-Type': 'application/json'}
  return headers

# set up filters
# Time filters
xdays = 30
now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
marketEndTime = (datetime.datetime.now()+ datetime.timedelta(days=xdays)).strftime("%Y-%m-%dT%TZ")
# Other filters comment and adjust as needed
#countryCode = '[]'
#countryCode = '["IE"]'
countryCode = '["IE","GB"]'


# API queries with filters
upcoming_races_meetings = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": {"filter":{"eventTypeIds":["7"],"marketCountries":'+str(countryCode)+',    "marketStartTime":{"from":"' +now + '", "to": "' + marketEndTime +'"}},"sort":"FIRST_TO_START"}, "id": 1}'

upcoming_races = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventIds":["29642169"],"marketTypeCodes":["WIN"]},"sort":"FIRST_TO_START","maxResults":"1000","marketProjection": ["COMPETITION","EVENT","MARKET_START_TIME"]}, "id": 1}'


# Support Functions

# get list of all horse ids from mysql db 
def getDbIdList():
  results = horseDAO.getAll()
  dbIdList = []
  for i in results:
    dbIdList.append(i['id'])
  return dbIdList

# function to find and return index of duplicates from a list
def getDuplicates(checkdups):
  id_set = set() 
  duplicate_index = [] 
  for idx, value in enumerate(checkdups): 
    if value not in id_set: 
      id_set.add(value)          
    else: 
      duplicate_index.append(idx)
  #print("dups", str(duplicate_index))
  # reverse sort list to avoid deleting 
  desc_dup_index = sorted(duplicate_index, reverse=True)
  return desc_dup_index

# break a list into chuncks of size n - no longer in use issue resolved
# from https://chrisalbon.com/python/data_wrangling/break_list_into_chunks_of_equal_size/
def getChunks(l, n):
  # For item i in a range that is a length of l,
  for i in range(0, len(l), n):
      # Create an index range for l of n items:
      yield l[i:i+n]

# Betfair API functions

# functions to get upcoming racemeetings within the next 30 days from the betfair api
def getEvents():
  req = requests.post(bet_url, data=upcoming_races_meetings.encode('utf-8'), headers=getheader())
  lEvents = req.json()
  events = []
  for item in lEvents['result']:
    ID = item['event']['id']
    Name = item['event']['name']
    Country = item['event']['countryCode']
    OpenDate = item['event']['openDate']
    event = {"ID":ID, "Name":Name, "Country":Country, "OpenDate":OpenDate}
    events.append(event)
  return events

# get upcoming race info from the betfair api
# Filter the api by eventIds to get the races for each racemeeting
def getUpcRaces():
  # get event ids in a list
  events = getEvents()
  evids = list(map(itemgetter('ID'), events))
  # add quotes
  eventids = json.dumps(evids)
  # API request
  upcoming_races = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketCatalogue", "params": {"filter":{"eventIds": '+eventids+',"marketTypeCodes":["WIN"]},"sort":"FIRST_TO_START","maxResults":"1000","marketProjection": ["RUNNER_METADATA","EVENT","MARKET_START_TIME"]}, "id": 1}'
  req = requests.post(bet_url, data=upcoming_races.encode('utf-8'), headers=getheader())
  upcRaces = req.json()
  upcomingraces = []
  # Filter and format results
  for item in upcRaces['result']:
    EID = item['event']['id']
    EName = item['event']['name']
    RID = item['marketId']
    RNAME = item['marketName']
    RSTARTTIME = item['marketStartTime']
    RUNNER = []
    for run in item['runners']:
      id = int(run['selectionId'])
      Name = run['runnerName']
      Age = run['metadata']['AGE']
      Sex = run['metadata']['SEX_TYPE']
      Owner = run['metadata']['OWNER_NAME']
      Trainer = run['metadata']['TRAINER_NAME']
      Form = run['metadata']['FORM']
      if Form == None:
        Form = "NoForm"
      values = (id, Name, Age, Sex, Owner, Trainer, Form)
      RUNNER.append(values)
    upcr = {"EID":EID, "EName":EName, "RID":RID, "RNAME":RNAME, "RSTARTTIME":RSTARTTIME,"RUNNER":RUNNER}
    upcomingraces.append(upcr)
  return upcomingraces


# Update Database from API functions

# retreive horses for upcoming races from API and update database horse table
def getUpcHorses():
  # id is the primary key 
  dbHorseIdList = getDbIdList()
  [str(i) for i in dbHorseIdList]
  print(dbHorseIdList)
  # Call data on upcoming races from the betfair api
  upcRaces = getUpcRaces()
  #print(upcRaces)
  # initiate lists
  horselist = []
  runnerslist = []
  checkduplicates = []
  # Loop to populate lists
  for run in upcRaces:
    runnerslist.append(run['RUNNER'])
    for runners in runnerslist:
      val = (runners)
      for horse in val:
        id = horse[0]
        checkduplicates.append(id)
        horselist.append(horse)
  # Duplicates checking - possible to have a horse more than once in the upcRaces
  if len(set(checkduplicates)) != len(checkduplicates):
    indexesTodelete =  getDuplicates(checkduplicates)
    #print(indexesTodelete)
    for i in indexesTodelete:
      del checkduplicates[i]
      del horselist[i]
    print("hl",len(horselist))
  # Check and remove any horses already in the database
  for i in dbHorseIdList:
    if i in checkduplicates:
      idx = checkduplicates.index(i)
      del checkduplicates[idx]
      del horselist[idx]
  # Workaround for mysql timeouts - break the list into chunks
  #https://chrisalbon.com/python/data_wrangling/break_list_into_chunks_of_equal_size/
  # horseChunks = list(getChunks(horselist, 20))
  # print(horseChunks)
  # print(len(horselist)) 
  # revised approach if issue reoccurs load the first 20 each time
  # Only load 20 each time its called due to timeout   
  #horses = (horselist[0:20])
  #time.sleep(1)
  horses = (horselist)
  print("Loading from the API into the database: ", horses)
  horseDAO.createAll(horses)
  




