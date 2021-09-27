from io import open as ioopen
from json import dump as jdump
from os import mkdir
from time import sleep
from colorama import init as colorinit
from termcolor import cprint
from shutil import copyfile
from json_func import *

colorinit()

folder = input("\nВведи алиас парка для папки на гитлабе\nНапример: для Ривьеры алиас - 'riviera', для Каунаса - 'kaunas': ")
try:
    mkdir(f'{folder}')
except FileExistsError:
    cprint('\nТакая папочка уже существует в этой директории, через 15 сек данные в ней будут перезаписаны.\nЕсли тебя это не устраивает нажми "Ctrl + C"', 'red')
    sleep(15)


with ioopen('config.csv', encoding='utf-8') as ocel_csv:
    line_num = 0
    breakcounter = 0
    pc_list = [] # в него добавляются компы по очереди
    app_dict = {} # в нем собирается инфа о повторении зон
    tracker_dict = {}
    zone_list = []
    tracker_list = []
    app_dict = {}
    app_list = []
    led_list = []
    app_name_dict = {}
    ocel_csv = ocel_csv.readlines()

    cprint('\n\nШрек начал генерировать конфиги', 'green')
    print('\n<--------------------------------------------------->\n')

    first_line = 0
    for line in ocel_csv:
        line_num +=1
        if first_line == 0:
            first_line +=1 # не читать первую строчку потому что она с описаниями

        else:
            word = line.split(',')
            if first_line == 1:

                # язык
                if word[18] == 'hp' or word[18] == 'hp\n': park_theme = 'yes'
                else: park_theme = 'no'
                if word[15] == 'ru' or word[15] == 'ru\n': language = 'ru'
                else: language = 'en'

                # блок за park.json
                if word[14] == '':
                    cprint(
                        f'ОШИБКА:\nНет айпишника у админки. Отмена конфигов, Исправь проблему и перегенерь конфиги\nСмотри строчку {line_num} столбец O\n', 'red'
                    )
                    breakcounter = 1
                    break
                else:
                    if word[16] == '' or word[17] == '':
                        mqtt_ip = word[14]
                        park = park_json(mqtt_ip, word[15])
                        cprint('ПРЕДУПРЕЖДЕНИЕ:\nНе указано логин или пароль к MQTT серверу, вставляется дефолный лог и пароль\nСмори строчку 1 столбец Q или R\n', 'white')
                        mqtt_credentials = 'Дефолтные (ShrWAPek - O403seL)'
                    else:
                        mqtt_ip = word[14]
                        park = park_json(mqtt_ip, word[15], word[16], word[17])
                        mqtt_credentials = f'Кастомные ({word[16]} - {word[17]})'

                    with ioopen(f'{folder}/park.json', 'w', encoding='utf-8') as pfile:
                        jdump(park, pfile, indent=2, ensure_ascii=False)

                # блок за themes.json
                if word[18] == 'hp' or word[18] == 'hp\n':
                    themes = hp_themes_json(language)
                    main_theme = 'Хеллоу Порк'
                else:
                    themes = hc_themes_json(language)
                    main_theme = 'ХК Порк'

                with ioopen(f'{folder}/themes.json', 'w', encoding='utf-8') as tfile:
                    jdump(themes, tfile, indent=2, ensure_ascii=False)

                first_line += 1

            if word[0] != '' and word[2] != '': # забить на пустые строки и на обозначения приложений

                if word[3] == '':
                    cprint(
                        f'ОШИБКА:\nНет mac адреса в паре "ip - mac".\nШрек отменяет генерацию конфигов. Исправь проблему и перегенерь конфиги\nСмотри строчку {line_num} столбец D\n', 'red'
                    )
                    breakcounter = 1
                    break

                app_dict[word[2]] = app_dict.get(word[2], 0) + 1
                ip_qty = app_dict.get(word[2])

                app_dict[word[3]] = app_dict.get(word[3], 0) + 1
                mac_qty = app_dict.get(word[3])

                if ip_qty != 1:
                    cprint(
                        f'ОШИБКА:\nАйпишник из {line_num} строчки уже занят другим компом в табличке.\nШрек отменяет генерацию конфигов. Исправь проблему и перегенерь конфиги\nСмотри строчку {line_num} столбец С\n', 'red'
                    )
                    breakcounter = 1
                    break
                if mac_qty != 1:
                    cprint(
                        f'ОШИБКА:\nMак из {line_num} строчки уже занят другим компом в табличке.\nШрек отменяет генерацию конфигов. Исправь проблему и перегенерь конфиги\nСмотри строчку {line_num} столбец D\n', 'red'
                    )
                    breakcounter = 1
                    break

                if len(word[2].split('.')) != 4:
                    cprint(
                        f'ОШИБКА:\nНеверный формат ip. В ip должно быть 4 блока данных разделеных точкой. Например: 10.0.23.111.\nИсправь проблему и перегенерь конфиги\nСмотри строчку {line_num} столбец С\n', 'red'
                    )
                    breakcounter = 1
                    break

                if len(word[3].split(':')) != 6:
                    cprint(
                        f'ОШИБКА:\nНеверный формат mac. В mac должно быть 6 блоков данных разделеных двоеточием. Например: 48:A4:72:4C:66:E3.\nИсправь проблему и перегенерь конфиги\nСмотри строчку {line_num} столбец D\n', 'red'
                    )
                    breakcounter = 1
                    break

                # блок за computer.json

                # считает сколько повторений зоны
                app_dict[word[0]] = app_dict.get(word[0], 0) + 1
                pc_quantity = app_dict.get(word[0])

                # если название зоны больше чем 1 слово
                word0_list = word[0].lower().split()
                if len(word0_list) != 1:

                    pc_id = ''
                    topic = ''
                    for i in range(len(word0_list)):
                        topic = f'{topic}{word0_list[i]}-'
                        pc_id = f'{pc_id}{word0_list[i]}_'
                    zone_id = pc_id[:-1]
                    tracker_topic = topic[:-1]
                    pc_id = f'hc_{pc_id}{pc_quantity}'
                    topic = f'WinThing/hc-{topic}{pc_quantity}'

                else:
                    pc_id = f'hc_{word[0]}_{pc_quantity}'
                    topic = f'WinThing/hc-{word[0]}-{pc_quantity}'
                    zone_id = word[0].lower()
                    tracker_topic = zone_id

                if language == 'ru' and word[1] != '':
                    name = word[1].capitalize()
                    pc_name = f'{name} {pc_quantity}'
                elif language == 'ru' and word[1] == '':
                    cprint(
                        f'ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ:\nВ зоне {word[0]} не написано название зоны на русском. Зона будет называться на англе\nСмотри строчку {line_num} столбец B\n', 'yellow'
                    )
                    name = word[0].capitalize()
                    pc_name = f'{name} {pc_quantity}'
                else:
                    name = word[0].capitalize()
                    pc_name = f'{name} {pc_quantity}'

                ip = word[2]
                mac = word[3]
                computer = computers_json(pc_id, pc_name, ip, mac, name, topic, zone_id)
                pc_list.append(computer)


                # блок по leds.json
                if word[13] == 'yes' or word[13] == 'yes\n':
                    led_key_words = [word[0], word[1], word[8], word[9], word[10]]

                    led_dict_id = f'{zone_id}_led'
                    app_dict[led_dict_id] = app_dict.get(led_dict_id, 0) + 1
                    led_qty = app_dict.get(led_dict_id)

                    led = led_json(led_key_words, led_qty, zone_id, language)
                    if led != None:
                        led_list.append(led)


                # блок за zones.json если есть компьютер
                if pc_quantity == 1:
                    if word[4] == park_theme: zone = zones_json(name, 'global', zone_id)
                    else:  zone = zones_json(name, 'apps', zone_id)
                    zone_list.append(zone)


                # блок за apps.json если в строчке есть комп
                if word[8] == '' or word[10] == '':
                    cprint(f'ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ:\nВ зоне {word[0]} не указано приложение.\nКонфиг формируется без приложения в этой зоне\nСмотри строчку {line_num} столбик I или К\n', 'yellow')
                else:
                    app_scenes = []
                    if word[4] == 'yes' or word[4] == 'yes\n': app_scenes = hp_scenes(language)
                    else:
                        if word[11] == '' or word[12] == '':
                            cprint(
                            f'ОШИБКА:\nДля приложений в которых нет 5 тем, обяз надо писать названия тем и их команды.\nИсправь проблему и перегенерь конфиги\nСмотри строчку {line_num} столбец L или M \n', 'red'
                        )
                            breakcounter = 1
                            break

                        try:
                            scene_names = word[11].split(';')
                            scene_commands = word[12].split(';')
                            for n, c in zip(scene_names, scene_commands):
                                one_scene = {
                                'name': n.capitalize(),
                                'scene' : c
                                }
                                app_scenes.append(one_scene)

                        except ValueError:
                            cprint(
                                f'ОШИБКА:\nПерепроверь названия сцен и их команды и перегенерь конфиги.\nКаждому названию сцены должна соответствовать своя команда.\nPазделение идет через между новой зоной или командой через ;.\nПроблема d {line_num} строке L и M столбе\n', 'red'
                            )
                            breakcounter = 1
                            break

                    apps_custom = [word[0], word[1], word[8], word[9], word[10]]

                    app_dict[word[10]] = app_dict.get(word[10], 0) + 1
                    app_qty = app_dict.get(word[10])

                    app_name_dict[word[8]] = app_name_dict.get(word[8], 0) + 1
                    app_name_qty = app_name_dict.get(word[8])

                    if language == 'ru':
                        if word[9] != '': app_name = word[9].capitalize()
                        else:
                            cprint(
                            f'ПРЕДУПРЕЖДЕНИЕ:\nВ зоне {word[0]} не написано название приложения на русском. Будет использован англ\nСмотри строчку {line_num} столбец J\n', 'white'
                            )
                            app_name = word[8].capitalize()
                    else: app_name = word[8].capitalize()

                    app_topic = ''
                    app_id = ''
                    for app_word in word[8].split():
                        app_topic = f'{app_topic}{app_word.lower()}-'
                        app_id = f'{app_id}{app_word.lower()}_'
                    app_id = f'{app_id}{app_name_qty}_unity'
                    app_topic = f'{app_topic}{app_qty}/{word[10]}'

                    app_list.append(apps_json(app_scenes, app_id, app_name, app_topic, zone_id, language, apps_custom, pc_id))


                # блок про trakers.json
                try: # лазер
                    j = 0
                    for j in range(int(word[5])):
                        sensor = f'{zone_id}_laser'
                        tracker_dict[sensor] = tracker_dict.get(sensor, 0) + 1
                        tr_quantity = tracker_dict.get(sensor)
                        tracker = trackers_json('laser', f'{sensor}_{tr_quantity}', f'{tracker_topic}/laser-{tracker_topic}-{tr_quantity}', zone_id, language)
                        tracker_list.append(tracker)
                except ValueError:
                    pass

                try: # композер
                    j = 0
                    for j in range(int(word[6])):
                        sensor = f'{zone_id}_composer'
                        tracker_dict[sensor] = tracker_dict.get(sensor, 0) + 1
                        tr_quantity = tracker_dict.get(sensor)
                        tracker = trackers_json('composer', f'{sensor}_{tr_quantity}', f'{tracker_topic}/composer-{tracker_topic}-{tr_quantity}', zone_id, language, 'composer')
                        tracker_list.append(tracker)
                except ValueError:
                    pass

                try: # депс
                    j = 0
                    for j in range(int(word[7])):
                        sensor = f'{zone_id}_depth'
                        tracker_dict[sensor] = tracker_dict.get(sensor, 0) + 1
                        tr_quantity = tracker_dict.get(sensor)
                        tracker = trackers_json('depth', f'{sensor}_{tr_quantity}', f'{tracker_topic}/depth-{tracker_topic}-{tr_quantity}', zone_id, language)
                        tracker_list.append(tracker)
                except ValueError:
                    pass


            #  блок про apps.json если в строчке нет компа
            elif word[0] != '' and word[2] == '':
                if word[3] != '':
                    cprint(
                        f'ОШИБКА:\nЛишний mac адрес. Если нет ip значит и mac быть не должно быть.\nИсправь проблему и перегенерь конфиги\nСмотри строчку {line_num} столбец D\n', 'red'
                    )
                    breakcounter = 1
                    break
                if word[8] == '' or word[10] == '': cprint(
                        f'ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ:\nВ зоне {word[0]} не указано приложение.\nКонфиг формируется без приложения в этой зоне\nСмотри строку {line_num} столбик I или К\n', 'yellow'
                    )
                else:
                    app_scenes = []
                    if word[4] == 'yes' or word[4] == 'yes\n': app_scenes = hp_scenes(language)
                    else:
                        if word[11] == '' or word[12] == '':
                            cprint(
                            f'ОШИБКА:\nДля приложений в которых нет 5 тем, обяз надо писать названия тем и их команды.\nИсправь проблему и перегенерь конфиги\nСмотри строчку {line_num} столбец L или M \n', 'red'
                        )
                            breakcounter = 1
                            break

                        try:
                            scene_names = word[11].split(';')
                            scene_commands = word[12].split(';')
                            for n, c in zip(scene_names, scene_commands):
                                one_scene = {
                                'name': n.capitalize(),
                                'scene' : c
                                }
                                app_scenes.append(one_scene)

                        except ValueError:
                            pass
                            cprint(
                                f'ОШИБКА:\nПерепроверь названия сцен и их команды и перегенерь конфиги.\nКаждому названию сцены должна соответствовать своя команда.\nPазделение идет через между новой зоной или командой через ; .\nПроблема в сточке{line_num} столбце L и M \n', 'red'
                            )
                            breakcounter = 1
                            break

                    apps_custom = [word[0], word[1], word[8], word[9], word[10]]

                    app_dict[word[10]] = app_dict.get(word[10], 0) + 1
                    app_qty = app_dict.get(word[10])

                    app_name_dict[word[8]] = app_name_dict.get(word[8], 0) + 1
                    app_name_qty = app_name_dict.get(word[8])

                    if language == 'ru':
                        if word[9] != '': app_name = word[9].capitalize()
                        else:
                            cprint(
                            f'ПРЕДУПРЕЖДЕНИЕ:\nВ зоне {word[0]} не написано название приложения на русском. Будет использован англ\nСмотри строчку {line_num} столбец J\n', 'white'
                            )
                            app_name = word[8].capitalize()
                    else: app_name = word[8].capitalize()

                    app_topic = ''
                    app_id = ''
                    for app_word in word[8].split():
                        app_topic = f'{app_topic}{app_word.lower()}-'
                        app_id = f'{app_id}{app_word.lower()}_'
                    app_id = f'{app_id}{app_name_qty}_unity'
                    app_topic = f'{app_topic}{app_qty}/{word[10]}'

                    word0_list = word[0].lower().split()
                    if len(word0_list) != 1:
                        zone_id = ''
                        for i in range(len(word0_list)):
                            zone_id = f'{zone_id}{word0_list[i]}_'
                        zone_id = zone_id[:-1]

                    else: zone_id = word[0].lower()
                    app_list.append(apps_json(app_scenes, app_id, app_name, app_topic, zone_id, language, apps_custom))

                    # блок по leds.json
                if word[13] == 'yes' or word[13] == 'yes\n':
                    led_key_words = [word[0], word[1], word[8], word[9], word[10]]

                    led_dict_id = f'{zone_id}_led'
                    app_dict[led_dict_id] = app_dict.get(led_dict_id, 0) + 1
                    led_qty = app_dict.get(led_dict_id)

                    led = led_json(led_key_words, led_qty, zone_id, language)
                    if led != None:
                        led_list.append(led)


                # блок за zones.json если нет компьютерa
                if language == 'ru' and word[1] != '':
                    name = word[1].capitalize()
                elif language == 'ru' and word[1] == '':
                    cprint(
                        f'ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ:\nВ зоне {word[0]} не написано название зоны на русском. Зона будет называться на англе\nСмотри строчку {line_num} столбец B\n', 'yellow'
                    )
                    name = word[0].capitalize()
                else:
                    name = word[0].capitalize()

                app_dict[word[0]] = app_dict.get(word[0], 0) + 1
                zone_qty = app_dict.get(word[0])
                if zone_qty == 1:
                    if word[4] == park_theme: zone = zones_json(name, 'global', zone_id)
                    else:  zone = zones_json(name, 'apps', zone_id)
                    zone_list.append(zone)





with ioopen(f'{folder}/apps.json', 'w', encoding='utf-8') as afile:
    jdump(app_list, afile, indent=2, ensure_ascii=False)

with ioopen(f'{folder}/trackers.json', 'w', encoding='utf-8') as trfile:
    jdump(tracker_list, trfile, indent=2, ensure_ascii=False)

with ioopen(f'{folder}/computers.json', 'w', encoding='utf-8') as cfile:
    jdump(pc_list, cfile, indent=2, ensure_ascii=False)

with ioopen(f'{folder}/zones.json', 'w', encoding='utf-8') as zfile:
    jdump(zone_list, zfile, indent=2, ensure_ascii=False)

with ioopen(f'{folder}/ui.json', 'w', encoding='utf-8') as uifile:
    jdump(ui_json(), uifile, indent=2, ensure_ascii=False)

copyfile('config.csv', f'{folder}/config.csv')

if led_list:
    with ioopen(f'{folder}/led.json', 'w', encoding='utf-8') as ledfile:
        jdump(led_list, ledfile, indent=2, ensure_ascii=False)

print('<--------------------------------------------------->\n')

cprint('Шрек закончил генерить конфиги!\n', 'green')

if breakcounter != 1:
    print(
        f'''Сведения о парке:
            Язык : {language}
            Тематика парка : {main_theme}
            MQTT ip : {mqtt_ip}
            MQTT credentials : {mqtt_credentials}

            Все JSON файлы сохранены в папочку '{folder}', которая создалась в этой директории.
            Тебе надо только эту папочку перенести на гитлаб. Вот ток енту - '{folder}'
            '''
        )
else: print('Никакого тебе парка. Исправляй ошибки и перегенерируй')
