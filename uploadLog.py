import requests
import json
import os
import os.path, time
import datetime
import pathlib

fileSize = os.stat(r'C:\Users\jerso\Desktop\Empresas\InnovaSport\proyectoGit\raspcontrol\js\log_18_Nov.log')
print('File Size is', fileSize.st_size, 'bytes')

fname = pathlib.Path(r'C:\Users\jerso\Desktop\Empresas\InnovaSport\proyectoGit\raspcontrol\js\log_18_Nov.log')
dateCreate = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
print(dateCreate)

now = datetime.datetime.now()
print(now)

daysOnRasp = abs(now - dateCreate)
print(daysOnRasp.days)



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