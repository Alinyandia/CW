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
    plt.title("Общая сеть")
    nx.draw_networkx_nodes(G, pos, node_color='green', node_size=10)
    nx.draw_networkx_edges(G, pos, edge_color='yellow')
    plt.savefig('1.png')
    plt.axis('off')
    plt.show()

    print('количество узлов' + ' ' + str(G.number_of_nodes())) #количество узлов
    print('количество рёбер' + ' ' + str(G.number_of_edges())) #количество рёбер
    print('плотность графа ' + ' ' + str(nx.density(G))) #плотность графа (отношение рёбер и узлов)
    print('средний коэффициент кластеризации' + ' ' + str(nx.average_clustering(G))) # средний коэффициент кластеризации
    print('коэфициент транзитивности' + ' ' + str(nx.transitivity(G))) # коэфициент транзитивности           


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
                if a[com] > 20 and a[com] <= 25:
                    colours.append('b')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 25 and a[com] <= 30:
                    colours.append('m')
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
                if a[com] > 20 and a[com] <= 25:
                    colours.append('b')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 25 and a[com] <= 30:
                    colours.append('m')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 30:
                    colours.append('g')
                    G.add_node(com)
                    edge.append((name, com))                    

        if a[name] > 20 and a[name] <= 25:
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
                if a[com] > 20 and a[com] <= 25:
                    colours.append('b')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 25 and a[com] <= 30:
                    colours.append('m')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 30:
                    colours.append('g')
                    G.add_node(com)
                    edge.append((name, com))
        if a[name] > 25 and a[name] <= 30:
            colours.append('m')
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
                if a[com] > 20 and a[com] <= 25:
                    colours.append('b')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 25 and a[com] <= 30:
                    colours.append('m')
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
                if a[com] > 20 and a[com] <= 25:
                    colours.append('b')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 25 and a[com] <= 30:
                    colours.append('m')
                    G.add_node(com)
                    edge.append((name, com))
                if a[com] > 30:
                    colours.append('g')
                    G.add_node(com)
                    edge.append((name, com))            
 
    node_colours = [i for i in colours]
    G.add_edges_from(edge)
    pos=nx.spring_layout(G)
    plt.title("Граф с отражнением возраста")
    nx.draw_networkx_nodes(G, pos, node_color=''.join(node_colours), node_size=10)
    nx.draw_networkx_edges(G, pos, edge_color='yellow')
    plt.savefig('2.png')
    plt.axis('off')
    plt.show()

    deg = nx.degree_centrality(G)
    _list = []
    
    for nodeid in sorted(deg, key=deg.get, reverse=True): #центральность узлов (важность узлов)
 #       print(nodeid, G.degree(nodeid)) #показывает сам узел, его соседей и возраст человека
        _list.append(a[nodeid])
        _list.append(G.degree(nodeid))
        
    return G, _list


def ages_count(a): # подсчитывает количество людей в каждой возрастной категории
    f = 0
    s = 0
    t = 0
    k = 0
    for el in a:
        if a[el] != 0 and a[el] <= 20:
            f += 1
        if a[el] > 20 and a[el] <= 25:
            s += 1
        if a[el] > 25 and a[el] <=30:
            k += 1
        if a[el] > 30:
            t += 1
    print('младше 20' + ' ' + str(f))
    print('от 21 до 25' + ' ' + str(s))
    print('от 26 до 30' + ' ' + str(k))
    print('старше 30' + ' ' + str(t))
    print('количество человек с датами рождения ' + ' ' + str(f+s+k+t))


def age_vs_len(_list): # для каждого возраста среднее колчиество связей
    i = 0
    b = 0
    res = {}
    for mem in _list:
        i += 1
        if i % 2 != 0:
            if mem in res:
                res[mem].append(_list[b+1])
                b += 2
            else:
               res[mem] = list()
               res[mem].append(_list[b+1])
               b += 2
    fin_res={}
    for el in res:
        friends = 0
        k = 0
        for p in res[el]:
            friends += p
            k += 1
        fin_res[el] = round(friends/k, 1)
    return fin_res


def bar_graf1(fin_res): #график возраст vs средне количество соседей
    age = [int(mem) for mem in fin_res]
    friends = [int(fin_res[mem]) for mem in fin_res]
    plt.figure(figsize=(12,5))
    plt.bar(age, friends)
    plt.xticks(age, age, rotation='vertical', size = 6)
    plt.yticks(friends, friends, rotation='vertical')
    plt.title('Соотношение возраста и средней степени')
    plt.ylabel('Среднее количество соседей')
    plt.xlabel('Возраст')
    plt.grid('on')
    plt.savefig('3.png')
    plt.show()

def graf2(G):
    p={}
    deg = nx.degree_centrality(G)
    for nodeid in sorted(deg, key=deg.get, reverse=True):
        p[nodeid] = G.degree(nodeid)        
    age = [int(mem) for mem in p]
    qantit = [int(p[mem]) for mem in p]
    plt.scatter(age, qantit, s=4, c='g')
    plt.xticks()
    plt.ylabel('Степень')
    plt.xlabel('Пользователи')
    plt.grid('off')
    plt.savefig('4.png')
    plt.show() 
    
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

graph(results)
g, l = graph_age(results, a)
ages_count(a)
f = age_vs_len(l)
bar_graf1(f)
graf2(g)
