«Анализ социальной сети носителей татарского языка в VK.com»
===========
Данная программа реализует анализ коллекции текстов на татарском языке, взятой с сайта проекта "Языки России". Коллекция текстов состоит из json-файлов каждый из которых содержит информацию о постах на стене определенной группы и комментариев к ним, а так же об авторах каждого из них (сгенерированный id (отличный от id в вк), дата рождения, пол). Подробнее: http://web-corpora.net/wsgi3/minorlangs/about.
Структура файла для группы с одним постом и одним комментарием к нему:
 {
    "group_name": {
        "members_count": 129,
        "posts": {
            "3186": {
                "comments": {
                    "3188": {
                        "language": "Tat",
                        "date": "2014-05-05 12:56:52",
                        "text": "18е Тукай музеена ШӘРЫК ветераннары җыела! Кем Шәрыкны ярата, рәхим итсен!",
                        "sort": 1399283812,
                        "author": {
                            "bdate": "8.7.1987",
                            "sex": 2,
                            "city": "Казань",
                            "id": 333953
                        }
                    }
                },
                "language": "Tat",
                "text": "Бинабыз татар халкыннан тартып алында. Аны инде кабаттан арттырып сатуга да куйдылар. Тик суз ул урыда тугел. Килэсе очрашу кайда булуын телисенг? Башка вариантларны аска яз.",
                "date": "2014-04-10 21:19:52",
                "sort": 1397153992,
                "copy_text": "",
                "author": "aralash"
            },          
        },
        "id": 12345678,
        "name": "название группы"
    },
    "0": {
        "date": "2015-03-26 21:49:44.990087",
        "language": "татарский"
    }
}


Так как в репризитории с коллекцией есть вложенные папки, мы обходим его следующим образом:
for (path, dirs, files) in os.walk("/Users/alinashaymardanova/Desktop/курсовая/tat_vk_corpus"):
    i = 1
    while i < len(files):
        f = open(''.join(path) + '/' + ''.join(files[i]), 'r', encoding = 'utf-8')
        res = json.load(f)
        f.close()
        i += 1
res -- декодированный json'овский объект (словарь). 
Мы считаем, что авторы комментариев к определенному посту общаются с автором поста. Таким образом, для построения сети необходимы 'id' авторов постов, а так же 'id' авторов комментариев к ним. Попутно с этим, в словарь ages записываем дату рождения каждого пользователя. Если дата рождения не указана, ставим 0. Функция inform получает на вход словарь res и вытаскивает всю необходимую информацию:
Обходим единственные два элемента в словаре, ища нужный ключ с названием группы: 
    for key in res:
        if key != '0':

Найдя необходимый ключ, заходим во вложенный в его значение словарь и ищем ключ 'posts' -- его значением является словарь, ключи которого -- это номера постов, а значения -- вся информация о постах.
    for post in res[key]['posts']:
    
Далее, проверяем, есть ли раздел 'author' в информации о посте и указано ли 'id' у автора:
    if 'author' in res[key]['posts'][post]:
        if 'id' in res[key]['posts'][post]['author']:

Если 'id' есть, то проверяем его наличие в словаре ages. Если в ages его нет, то проверяем, указана ли дата рождения у пользователя: если указана, то образуем пару 'id' -- ключ, дата рождения -- значение, а если не указана, то также образуем пару, но в значение ставим 0:
    if res[key]['posts'][post]['author']['id'] not in ages:
        if "bdate" in res[key]['posts'][post]['author']:
            ages[res[key]['posts'][post]['author']['id']] = res[key]['posts'][post]['author']['bdate']
        else:
            ages[res[key]['posts'][post]['author']['id']] = 0

Далее, проверяем наличие комментариев. Если есть, то обходим каждый из них:
  for com_n in res[key]['posts'][post]['comments']:
  
Если автором поста является не сама группа, тогда проверяем наличие 'id' автора в словаре result. Если такого ключа нет, то мы добавляем его в словарь и в значении ключа заводим массив. Проходимся по всем комментариям к посту и если 'id' автора поста не совпадает с 'id' автора комментария, то добавляем 'id' автора комментария в массив значений:
if type(res[key]['posts'][post]['comments'][com_n]['author']) != str:
    if res[key]['posts'][post]['author']['id'] in result:
        if res[key]['posts'][post]['comments'][com_n]['author']['id'] != res[key]['posts'][post]['author']['id']:
            result[res[key]['posts'][post]['author']['id']].append(res[key]['posts'][post]['comments'][com_n]['author']['id'])
 
Далее, заносим возраст всех авторов комментариев в словарь ages:
if res[key]['posts'][post]['comments'][com_n]['author']['id'] not in ages:
    if "bdate" in res[key]['posts'][post]['comments'][com_n]['author']:
        ages[res[key]['posts'][post]['comments'][com_n]['author']['id']] = res[key]['posts'][post]['comments'][com_n]['author']['bdate']
    else:
        ages[res[key]['posts'][post]['comments'][com_n]['author']['id']] = 0


Если комментариев к посту нет, то мы заносим 'id' автора в result и массив значений оставляем пустым:
if res[key]['posts'][post]['author']['id'] not in result:
    result[res[key]['posts'][post]['author']['id']] = list()
    

Функция age получает на вход словарь ages и высчитывает количество полных лет. Для реализации функции необходимо импортировать модуль для определения сегодняшней даты:
from datetime import date

Далее с помощью регулярного выражения проверяем наличие полной даты рождения. Если дата полная, то вычисляем возраст:
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
 
 Если дата не полная, то ставим 0:
  else:
    ages[person] = 0
 
 Полученный для каждой группы словарь с возрастами добавляем к общему словарю с возрастами a:
    a.update(ages)
    
Далее, в функции graph мы рисуем граф, узлы которого отображают каждого из пользователей, а ребра -- общение этих пользователей. Функция получает на вход словарь result:

Создаем пустой граф: 
G = nx.Graph()

Для каждого ключа словаря result создаем узел:
for name in result:
    G.add_node(name)

У каждого ключа обходим массив значений, создавая для каждого элемента узел и добавляя пару -- ключ и элемент_массива_значений этого ключа -- в массив с рёбрами edge:
for com in result[name]:
    G.add_node(com)
    edge.append((name, com))
    
Добавляем информацию о всех рёбрах в граф:
G.add_edges_from(edge)

Выбираем способ организации графа:
pos=nx.spring_layout(G)

Рисуем узлы (зеленым) и рёбра (желтым):
nx.draw_networkx_nodes(G, pos, node_color='green', node_size=10)
nx.draw_networkx_edges(G, pos, edge_color='yellow')

Далее, вытаскиваем информацию о полученном графе:
Количество узлов и рёбер:
print(G.number_of_nodes())
print(G.number_of_edges())

Плотность графа:
print(nx.density(G))

Коэффициент транзитивности и средний коэффициент кластеризации:
print(nx.transitivity(G))
print(nx.average_clustering(G))

В функции graph_age мы рисуем точно такой же граф, только с учетом возрастной категории пользователей. На вход функция получает словари result и a. Отличием этой функци от предыдущей является то, что попутно с добавлением узла в граф, мы добавляем цвет узла в массив colours: 'k' -- чёрный, если возраст не указан (= 0), 'r' -- красный, если младше 20, 'b' -- синий, если от 21 до 25 включительно, 'm' -- фиолетовый, если от 26 до 30 включительно и 'g' - зеленый, если старше 30. 
Далее, организуем массив последовательностей цветов для каждого узла:
node_colours = [i for i in colours]

Добавляем информацию о рёбрах, задаем способ организации графа и рисуем:
G.add_edges_from(edge)
pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color=''.join(node_colours), node_size=10)
nx.draw_networkx_edges(G, pos, edge_color='yellow')

В этой же функции определяем центральность всех узлов, а так же записываем в массив _list возраст и степень узлов в порядке убывания степени (для будущего графика):
for nodeid in sorted(deg, key=deg.get, reverse=True):
    print(nodeid, G.degree(nodeid)) #показывает сам узел, его соседей и возраст человека
    _list.append(a[nodeid])
    _list.append(G.degree(nodeid))
    
В следующей функции age_vs_len вычисляем среднюю степень для каждого возраста. Обходя массив и выделяя каждый нечетный элемент массива _list -- возраст -- формируем словарь res, ключом которого станет возраст, а в массиве значений будет список средних степеней узлов подходящего возраста:
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
        
Далее обходим каждый вложенный массив и составляем новый словарь fin_res, где ключи -- возраст, а значения -- средняя степень, округленная до десятых:
fin_res={}
for el in res:
    friends = 0
    k = 0
    for p in res[el]:
        friends += p
        k += 1
    fin_res[el] = round(friends/k, 1)

В следующей функции строим график отображающий зависимость средней степени от возраста пользователей. На вход получаем словарь fin_res и на его основе создаем два массива: age и friends -- возраст и степень, соответственно:
age = [int(mem) for mem in fin_res]
friends = [int(fin_res[mem]) for mem in fin_res]

Строим график с показателями возраста по оси OX и показателями степени по OY. Задаём параметры подписей осей:
plt.bar(age, friends)
plt.xticks(age, age, rotation='vertical', size = 6)
plt.yticks(friends, friends, rotation='vertical')

Далее, строим график, который покажет насколько сильно разнятся степени пользователей. На вход функция получает G, где содержится вся информация об узлах и ребрах общего графа. На основе G формируем словарь p, где ключ -- это 'id' пользователя (имя узла), а значение -- его степень. Далее, как и в прошлом графе, исходя из словаря p образуем два массива: с ключами и со значениями:
deg = nx.degree_centrality(G)
for nodeid in sorted(deg, key=deg.get, reverse=True):
    p[nodeid] = G.degree(nodeid)        
age = [int(mem) for mem in p]
qantit = [int(p[mem]) for mem in p]

Основываясь на них, строим график с несоединенными точками:
plt.scatter(age, qantit, s=4, c='g')

Функция ages_count -- дополнительная функция, которая подсчитывает количество человек в каждой возрастной категории. Она получает на вход словарь с возрастами пользователей a и обходит его.
