import json
import os


def inform(res, file):
    for key in res:
        if key != "0":
            members_count = res[key]['members_count'] #количество подписчиков
            name = res[key]['name'] #название сообщества
            for num in res[key]['posts']: #идем по номерам записей
                if res[key]['posts'][num]['comments']: #если есть комменты, то смотрим их авторов
                    auth.append("Комментарии к записи номер"+ " " + num)
                    if 'author' in res[key]['posts'][num]: #если есть строка с автором записи, то записываем инф-ию о нём
                        auth.append("Автор записи")
                        auth.append(res[key]['posts'][num]['author'])
                    else:
                        auth.append("Автор удалён")
                    for c_num in res[key]['posts'][num]['comments']:
                        auth.append(res[key]['posts'][num]['comments'][c_num]['author'])
                    auth.append("Конец комментариев")
                else:
                    auth.append(res[key]['posts'][num]['author']) #достаем инфу об авторе
    file.write('Имя группы' + ' ' + str(name) + '\n' + 'Количество человек' + ' ' + str(members_count) + '\n' + 'Авторы:' + '\n')
    return auth

def di(auth):
    for memb in auth: #формируем словарь частотности каждого пользователя
        if 'id' in memb:
            if memb['id'] in d:
                d[memb['id']] += 1
            else:
                d[memb['id']] = 1
        file.write( ''.join(str(memb)) + '\n')
 #   file.write(''.join(str(d)) + '\n' + '\n') #записываем сам словарь частотности
    f.close()


file = open("result.txt", 'w', encoding ='utf-8')
for (path, dirs, files) in os.walk("/Users/alinashaymardanova/Downloads/tat_vk_corpus"):
    i = 1
    while i < len(files):
        auth = []
        d = {}
        f = open(''.join(path) + '/' + ''.join(files[i]), 'r', encoding = 'utf-8')
        res = json.load(f)
        f.close()
        inform(res, file)
        di(auth)
        i += 1
file.close()

