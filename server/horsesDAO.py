import mysql.connector
import dbconfig as cfg


class HorseDAO:
  db=""
  def __init__(self):
    self.db = mysql.connector.connect(
    host=cfg.mysql['host'], 
    user=cfg.mysql['user'], 
    password=cfg.mysql['password'],  
    database=cfg.mysql['database'] 
    )

  def create(self, values):
    cursor = self.db.cursor()
    sql="insert into horse (id, name, age, sex, owner, trainer, form) values (%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, values)

  def createAll(self, val):
    cursor = self.db.cursor()
    sql="""insert into horse (id, name, age, sex, owner, trainer, form) values (%s,%s,%s,%s,%s,%s,%s)"""
    cursor.executemany(sql, val)
    self.db.commit()
    return cursor.lastrowid

  def getAll(self):
    cursor = self.db.cursor()
    sql = "select * from horse"
    cursor.execute(sql)
    results = cursor.fetchall()
    returnArray = []
    for result in results:
      returnArray.append(self.convertToDictionary(result))
    return returnArray
    
  def findByID(self, id):
    cursor = self.db.cursor()
    sql = "select * from horse where id = %s"
    values = (id,)
    cursor.execute(sql, values)
    result = cursor.fetchone()
    return self.convertToDictionary(result)

  def update(self, values):
    cursor = self.db.cursor() 
    sql="update horse set name = %s, age = %s, sex = %s, owner = %s, trainer = %s, form = %s where id = %s"
    cursor.execute(sql, values)
    self.db.commit()

  def delete(self, id):
    cursor = self.db.cursor()
    sql= "delete from  horse where id = %s"
    values = (id,)
    cursor.execute(sql, values)
    self.db.commit()
    print("delete done")
  
  def convertToDictionary(self, result):
    colnames=['id','Name','Age', 'Sex', 'Owner', 'Trainer', 'Form']
    item = {}
    # check if result empty     
    if result:
        for i, colName in enumerate(colnames):
            value = result[i]
            item[colName] = value
    return item
  
# make a new instance of the class when testing use this instance
horseDAO = HorseDAO()
