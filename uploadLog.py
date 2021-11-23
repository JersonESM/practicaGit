
# -*- coding: utf-8 -*-
import requests
import json
import os
import os.path, time
import datetime
import pathlib
import mysql.connector

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
# print(now)
fileSize = os.stat(r'/home/pi/Documents/Control/js/log_18_Nov.log')
# print('File Size is', fileSize.st_size, 'bytes')

if myresult[0] != now.day:
    print("Aun no se ha subido el archivo")
    if fileSize.st_size <= 6000000:
        print("El archivo pesa menos de 6MB")
        print("Subiendo el archivo")
    else:
        print("Borrando el archivo por el peso")
else:
    print("Ya existe un archivo en la base")



# fname = pathlib.Path(r'/home/pi/Documents/Control/js/log_18_Nov.log')
# dateCreate = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
# print(dateCreate)

# daysOnRasp = abs(now - dateCreate)
# print(daysOnRasp.days)

# if daysOnRasp.days <=2 and fileSize.st_size <= 6000000:
#     print("Si se cumplen las condiciones")
#     print("Cambiando el archivo")
#     mycursor = mydb.cursor()
#     sql = "UPDATE uploadFile SET upload = 1 WHERE id = 1"
#     mycursor.execute(sql)
#     mydb.commit()
#     print(mycursor.rowcount, "record(s) affected")


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True
url = "https://datalogger.esmindustries.com.mx/innovasports/upload_log.php"
# path=os.path.dirname(__file__)+"/../js/"
path = "/home/pi/Documents/Control/js"
filename="log_18_Nov.log"
# filepath=os.path.normpath(path)+"\\"+filename
filepath=os.path.normpath(path)+"/"+filename
print(filepath)
file=open(filepath,'rb')
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
                os.remove(filepath)
                print("removing file "+filepath)
    else:
        print("The file does not exist")
except ValueError as e:
    print (e)


#Crear una tabla mysql y guardar ahí si se subio el archivo con exito 
#Cada que se ejecuta python checar si se subio, si no que lo vuelva a subir 
#Condicion de que si no se ha subido y pesa mas de 6MB que borre el programa si es que no se ha subido en 2 días 
#Cuando subes el archivo por ende se borra para crear uno nuevo 
#Expresion crontab 30 1 0,2,5,9,11,15,17,21,23 ? * * *


#1. Valuar la fecha de creación y fecha actual
#2. Valuar el peso del archivo a subir
#3. Condición si la fecha es menos de 2 días y el archivo pesa menos de 6MB subir, si no borar
#4. Dentro del if intentar que se suba varias veces el archivo si se sube borrar el archvio