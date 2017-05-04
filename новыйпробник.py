import json
import os
import re
from datetime import date



def inform(res):
    ages= {}
    for key in res:
        if key != '0':
            for post in res[key]['posts']:
                if 'author' in res[key]['posts'][post]:
                    if 'id' in res[key]['posts'][post]['author']:
                        if res[key]['posts'][post]['author']['id'] not in ages:
                            if "bdate" in res[key]['posts'][post]['author']:
                                ages[res[key]['posts'][post]['author']['id']] = res[key]['posts'][post]['author']['bdate']
                        if res[key]['posts'][post]['comments']:
                            for com_n in res[key]['posts'][post]['comments']:
                                if type(res[key]['posts'][post]['comments'][com_n]['author']) != str:
                                    if res[key]['posts'][post]['author']['id'] in result:
                                        result[res[key]['posts'][post]['author']['id']].append(res[key]['posts'][post]['comments'][com_n]['author']['id'])
                                    else:
                                        result[res[key]['posts'][post]['author']['id']] = list()
                                        result[res[key]['posts'][post]['author']['id']].append(res[key]['posts'][post]['comments'][com_n]['author']['id'])
    return ages


def age(ages):
    for person in ages:
        year = re.search('([0-9]*?)\.([0-9]*?)\.([0-9]*)', str(ages[person]))
        if year:
            today = date.today()
            age = today.year - int(year.group(3))
            if today.month < int(year.group(2)):
                age -= 1
            elif today.month == int(year.group(3)) and today.day < int(year.group(1)):
                age -= 1
            ages[person] = age
        else:
            ages[person] = 0
    a.update(ages)               
                         
               
    
result = {}
a = {}
for (path, dirs, files) in os.walk("/Users/alinashaymardanova/Desktop/курсовая/tat_vk_corpus"):
    i = 1
    while i < len(files):
        f = open(''.join(path) + '/' + ''.join(files[i]), 'r', encoding = 'utf-8')
        res = json.load(f)
        f.close()
        ages = inform(res)
        age(ages)
        i += 1
print(len(a)) #количество человек
k = 0
for el in a:
    if a[el] != 0:
        k += 1
print(k) #количество человек с датами рождения
file = open("result.txt", 'w', encoding ='utf-8')
file.write(str(result)) 
file.close()

