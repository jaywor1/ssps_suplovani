from tracemalloc import start
from numpy import tri
import requests
import json
from datetime import date, datetime
from datetime import timedelta
import datetime

print("Datum, Hodina, Původní Učitel,Suplovací učitel, Předmět, Skupina, Změna")

today = date.today() + timedelta(days=1)

startOfSchool = datetime.date(2021,9,1)

currentCheckingDate = startOfSchool;

while(currentCheckingDate != startOfSchool + timedelta(days=365)):
    d1 = currentCheckingDate.strftime("%Y%m%d")

    odpoved = requests.get(f'https://skripta.ssps.cz/substitutions.php/?date={d1}')
    data = json.loads(odpoved.text)

    indexOfClass = -1;

    for i in range(len(data["ChangesForClasses"])):
        if(data["ChangesForClasses"][i]["Class"]["Abbrev"] == "2.K"):
            indexOfClass = i
            #print(f'\033[92m' + f'[   OK   ]: date is {currentCheckingDate}' + '\033[0m')        
            break

    if(indexOfClass == -1):
        #print('\033[91m'+ f'[   ERROR   ]: failed to find class 2.K (date: {currentCheckingDate})' + '\033[0m')
        currentCheckingDate = currentCheckingDate + timedelta(days=1)
        continue
    else:
        tridaData = data["ChangesForClasses"][indexOfClass]["ChangedLessons"]
    if(len(tridaData) != 0):
        #print("Dneska odpadají následující předměty:")
        if(len(tridaData) >= 6):
            for i in range(len(tridaData)):
                print(f'{currentCheckingDate},{tridaData[i]["Hour"]},{tridaData[i]["ChgType2"]},{tridaData[i]["Teacher"]},{tridaData[i]["Subject"]},{tridaData[i]["Group"]},{tridaData[i]["Teacher"]},{tridaData[i]["ChgType1"]}')
        else:            
            for i in range(len(tridaData)):
                print(f'{currentCheckingDate},{tridaData[i]["Hour"]},{tridaData[i]["ChgType2"]},{tridaData[i]["Teacher"]},{tridaData[i]["Subject"]},{tridaData[i]["Group"]},{tridaData[i]["ChgType1"]}')
            #print(f'{tridaData[i]["Hour"]}. hodinu {tridaData[i]["ChgType1"]} {tridaData[i]["Subject"]} pro {tridaData[i]["Group"]}')
    currentCheckingDate = currentCheckingDate + timedelta(days=1)
    


