import json
import os
import re
from datetime import date
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import OrderedDict

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
                            else:
                                ages[res[key]['posts'][post]['author']['id']] = 0
                        if res[key]['posts'][post]['comments']:
                            for com_n in res[key]['posts'][post]['comments']:
                                if type(res[key]['posts'][post]['comments'][com_n]['author']) != str:
                                    if res[key]['posts'][post]['author']['id'] in result:
                                        if res[key]['posts'][post]['comments'][com_n]['author']['id'] != res[key]['posts'][post]['author']['id']:
                                            result[res[key]['posts'][post]['author']['id']].append(res[key]['posts'][post]['comments'][com_n]['author']['id'])
                                    else:
                                        if res[key]['posts'][post]['comments'][com_n]['author']['id'] != res[key]['posts'][post]['author']['id']:
                                            result[res[key]['posts'][post]['author']['id']] = list()
                                            result[res[key]['posts'][post]['author']['id']].append(res[key]['posts'][post]['comments'][com_n]['author']['id'])
                                    if res[key]['posts'][post]['comments'][com_n]['author']['id'] not in ages:
                                        if "bdate" in res[key]['posts'][post]['comments'][com_n]['author']:
                                            ages[res[key]['posts'][post]['comments'][com_n]['author']['id']] = res[key]['posts'][post]['comments'][com_n]['author']['bdate']
                                        else:
                                            ages[res[key]['posts'][post]['comments'][com_n]['author']['id']] = 0
                        else: #изолированные вершины
                            if res[key]['posts'][post]['author']['id'] not in result:
                                result[res[key]['posts'][post]['author']['id']] = list()
                                                
                                
    return ages, result

def age(ages): #высичтывает возраст людей, у которых указана полная дата рождения. Если не указана, то ставит 0
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
                         
def graph(result): #общий граф людей
    G = nx.Graph()
    edge=[]
    for name in result:
        G.add_node(name)
        for com in result[name]:
            G.add_node(com)
            edge.append((name, com))
    G.add_edges_from(edge)
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='green', node_size=10)
    nx.draw_networkx_edges(G, pos, edge_color='yellow') 
    plt.axis('off')
    plt.show()

def graph_age(result, a): #граф по возрастам
    G = nx.Graph()
    edge=[]
    colours=[]
    for name in result:
        if a[name] == 0:
            colours.append('k')
            G.add_node(name)
            for com in result[name]:
                if a[com] == 0:
                    colours.append('k')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] <= 20 and a[com] != 0:
                    colours.append('r')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 20 and a[com] <= 30:
                    colours.append('b')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 30:
                    colours.append('g')
                    G.add_node(com)
                    edge.append((name, com))                    
           
        if a[name] <= 20 and a[name] != 0:
            colours.append('r')
            G.add_node(name)
            for com in result[name]:
                if a[com] == 0:
                    colours.append('k')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] <= 20 and a[com] != 0:
                    colours.append('r')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 20 and a[com] <= 30:
                    colours.append('b')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 30:
                    colours.append('g')
                    G.add_node(com)
                    edge.append((name, com))                    

        if a[name] > 20 and a[name] <= 30:
            colours.append('b')
            G.add_node(name)
            for com in result[name]:
                if a[com] == 0:
                    colours.append('k')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] <= 20 and a[com] != 0:
                    colours.append('r')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 20 and a[com] <= 30:
                    colours.append('b')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 30:
                    colours.append('g')
                    G.add_node(com)
                    edge.append((name, com))

        if a[name] > 30:
            colours.append('g')
            G.add_node(name)
            for com in result[name]:
                if a[com] == 0:
                    colours.append('k')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] <= 20 and a[com] != 0:
                    colours.append('r')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 20 and a[com] <= 30:
                    colours.append('b')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 30:
                    colours.append('g')
                    G.add_node(com)
                    edge.append((name, com))            
 
    node_colours = [i for i in colours]
    G.add_edges_from(edge)
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color=''.join(node_colours), node_size=10)
    nx.draw_networkx_edges(G, pos, edge_color='yellow') 
    plt.axis('off')
    plt.show()

    return G

def popular_mem(G, a): #самые общительные люди и их возраст
    d = {}
    i = 1
    k = 0
    for node in G.nodes():
        d[node]=G.degree(node)       
    newd = list(d.items())
    newd.sort(key=lambda item: item[1])
    while i <= 31:
        for el in newd[-i]:
            k += 1
            if k % 2 != 0:               
                print(a[el])
        print(newd[-i])
        i += 1
    file.close()

def ages_count(a): # подсчитывает количество людей в каждой возрастной категории
    f = 0
    s = 0
    t = 0
    null = 0
    for el in a:
        if a[el] == 0:
            null += 1
        if a[el] != 0 and a[el] <= 20:
            f += 1
        if a[el] < 20 and a[el] <= 30:
            s += 1
        if a[el] > 30:
            t += 1
    print(f,s,t,null)


    
    
result = {}
a = {} #возраст людей, у кого указан год рождения. у кого не указан, ставится 0
for (path, dirs, files) in os.walk("/Users/alinashaymardanova/Desktop/курсовая/tat_vk_corpus"):
    i = 1
    while i < len(files):
        f = open(''.join(path) + '/' + ''.join(files[i]), 'r', encoding = 'utf-8')
        res = json.load(f)
        f.close()
        ages,results = inform(res)
        age(ages)
        i += 1
print(len(a)) #количество человек (5084)
k = 0
for el in a:
    if a[el] != 0:
        k += 1
print(k) #количество человек с датами рождения (1660)
file = open("возраст.txt", 'w', encoding ='utf-8')
file.write(str(a)) 
file.close()
graph(results)
g = graph_age(results, a)
popular_mem(g,a)
ages_count(a)
