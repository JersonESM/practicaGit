
# -*- coding: utf-8 -*-
import requests
import json
import os
import os.path, time
import datetime
import pathlib
import mysql.connector

url = "https://datalogger.esmindustries.com.mx/innovasports/upload_log.php"
# path=os.path.dirname(__file__)+"/../js/"
path = "/home/pi/Documents/Control/js"
filename="log_18_Nov.log"
# filepath=os.path.normpath(path)+"\\"+filename
filepath=os.path.normpath(path)+"/"+filename
# print(filepath)
file=open(filepath,'rb')

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="esmpi",
    database="controlv2"
)

#buscando si existe un registro en la base de datos 
mycursor = mydb.cursor()
mycursor.execute("SELECT day FROM uploadFile")
myresult = mycursor.fetchone()
print(myresult[0])

now = datetime.datetime.now()
print(now.day)
fileSize = os.stat(r'/home/pi/Documents/Control/js/log_18_Nov.log')
# print('File Size is', fileSize.st_size, 'bytes')

if myresult[0] != now.day:
    print("Aun no se ha subido el archivo")
    if fileSize.st_size <= 6000000:
        print("El archivo pesa menos de 6MB")
        print("Subiendo el archivo")
        try:
            if os.path.exists(filepath):
                print("file exists "+filepath)
                payload={'hash': '1f7ede94-af44-46c0-b19d-6f5ab5f47140','id': '23'}
                files=[('file',(filename,file,'application/octet-stream'))]
                headers = {'Authorization': 'Basic aW5ub3ZhOjRrSi9XOD5UOSh5Z1JzKQ=='}
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                print(response.text)
                file.close()
                if is_json(response.text):
                    obj=json.loads(response.text)
                    if obj["success"]:
                        print("Modificando la base local")
                        mycursor = mydb.cursor()
                        sql = "UPDATE uploadFile SET day = %s WHERE id = %s"
                        val = (now.day,'1')
                        mycursor.execute(sql,val)
                        mydb.commit()
                        print(mycursor.rowcount, "record(s) affected")
                        print("removing file "+filepath)
                        os.remove(filepath)
            else:
                print("The file does not exist")
        except ValueError as e:
            print (e)
    else:
        print("Borrando el archivo por el peso")
        os.remove(filepath)
else:
    print("Ya existe un archivo en la base")


#Expresion crontab 30 1 0,2,5,9,11,15,17,21,23 ? * * *


