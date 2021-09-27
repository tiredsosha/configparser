def computers_json(id, pc_name, ip, mac, name, topic, zone):
    return {
        'computer_id' : id,
        'computer_name': pc_name,
        'ip': ip,
        'mac': mac,
        'name' : name,
        "winthing_topic_prefix": topic,
        'zone_id': zone
    }


def park_json(ip, lang='en', login='ShrWAPek', password="O403seL", name='Park', port=80):
    return {
        "mqtt" : {
            "ip": ip,
            "password": password,
            "username": login
        },
        'port' : port,
        "language": lang,
        "name": name
    }


def led_json(key_word_list, led_qty, zone, lang):

    cubes = ['cube', 'boxgame', 'кубик']
    painter = ['painter', 'худо', 'кист']
    pictures = ['picture', 'рисунки', 'оживш', 'livin']
    ballstrike = ['ball', 'kidalki', 'кидалк']
    figures = ['figure', 'фигур', 'form', 'shape']
    led_id = None
    led_topic = None

    if lang == 'ru':
        led_name = 'Дерево'
        names_list = ['Город', 'Космос', 'Животные', 'Подводный мир', 'Игрушки', 'Новый год']
    else:
        led_name = 'Led'
        names_list = ['City', 'Space', 'Toys', 'Underwater', 'Toys', 'New Year']

    for key_word in key_word_list:
        key_word = key_word.lower()
        for cube_word in cubes:
            if cube_word in key_word:
                led_topic = 'cubes/cubes_led'
                led_id = 'led_cubes_'
                break
        for painter_word in painter:
            if painter_word in key_word:
                led_topic = 'painter/painter_led'
                led_id = 'led_painter_'
                break
        for pictures_word in pictures:
            if pictures_word in key_word:
                led_topic = 'pictures/pictures_led'
                led_id = 'led_pictures_'
                break
        for ballstrike_word in ballstrike:
            if ballstrike_word in key_word:
                led_topic = 'ballstrike/ballstrike_led'
                led_id = 'led_ballstrike_'
                break
        for figures_word in figures:
            if figures_word in key_word:
                led_topic = 'figures/figures_led'
                led_id = 'led_figures_'
                break


    if led_id != None:
        led_dict = {
            "name": led_name,
            "led_id": f"{led_id}{led_qty}",
            "topic_prefix": led_topic,
            "zone_id": zone,
            "all_scenes": [
                {
                    "name": names_list[0],
                    "scene_id": "city"
                },
                {
                    "name": names_list[1],
                    "scene_id": "space"
                },
                {
                    "name": names_list[2],
                    "scene_id": "animals"
                },
                {
                    "name": names_list[3],
                    "scene_id": "underwater"
                },
                {
                    "name": names_list[4],
                    "scene_id": "toys"
                },
                {
                    "name": names_list[5],
                    "scene_id": "newyear"
                }
            ]
        }
        return led_dict




# themes func
def hp_themes_json(lang):
    if lang == 'ru': names_list = ['Город', 'Космос', 'Животные', 'Подводный мир', 'Игрушки', 'Новый год']
    else: names_list = ['City', 'Space', 'Toys', 'Underwater', 'Toys', 'New Year']

    hp_themes = [
        {
            "name": names_list[0],
            "theme_id": "city",
            "scene_id": "City"
        },
        {
            "name": names_list[1],
            "theme_id": "space",
            "scene_id": "Space"
        },
        {
            "name": names_list[2],
            "theme_id": "animals",
            "scene_id": "Animals"
        },
        {
            "name": names_list[3],
            "theme_id": "underwater",
            "scene_id": "Underwater"
        },
        {
            "name": names_list[4],
            "theme_id": "toys",
            "scene_id": "Toys"
        },
        {
            "name": names_list[5],
            "theme_id": "newyear",
            "scene_id": "NewYear"
        }
    ]

    return hp_themes



def hc_themes_json(lang):
    if lang == 'ru': return [
        {
            "name": "Общая",
            "theme_id": "main",
            "scene_id": "Main"
        }
    ]
    else: return [
        {
            "name": "Main",
            "theme_id": "main",
            "scene_id": "Main"
        }
    ]


def ui_json():
    return {
        "show_apps_on_the_main_page": True
    }


def zones_json(name, theme, zone):
    return {
        "name": name,
        "themes" : theme,
        "zone_id": zone
    }


def trackers_json(name, id, topic, zone, lang, tracker_type=None):

    if lang == 'ru': name_list = ['Фон', 'очистить']
    else: name_list = ['Backgrd', 'clear']
    if tracker_type == None:
        return {
            "name": name,
            "tracker_id" : id,
            'topic_prefix' : topic,
            "zone_id": zone
        }
    else:
        return {
            "name": name,
            "tracker_id" : id,
            'topic_prefix' : topic,
            "custom" : [
                {
                    "type" : "button",
                    "icon" : "mdi:texture",
                    "name" : name_list[0],
                    "action_name" : name_list[1],
                    "topic" : "savebg",
                    "value" : "true"
                }
            ],
            "zone_id": zone
        }



# apps func
def volume(lang):
    if lang == 'ru':
        return [
            {
                "name": "Музыка",
                "volume_id": "volume_music"
            },
            {
                "name": "Эффекты",
                "volume_id": "volume_fx"
            },
            {
                "name": "Голос",
                "volume_id": "volume_voice"
            }
        ]
    else:
        return [
            {
            "name": "Music",
            "volume_id": "volume_music"
            },
            {
            "name": "Fx",
            "volume_id": "volume_fx"
            },
            {
            "name": "Voice",
            "volume_id": "volume_voice"
            }
        ]


def hp_scenes(lang):
    if lang == 'ru': names_list = ['Город', 'Космос', 'Животные', 'Подводный мир', 'Игрушки', 'Новый год']
    else: names_list = ['City', 'Space', 'Toys', 'Underwater', 'Toys', 'New Year']

    hp_themes = [
        {
            "name": names_list[0],
            "scene_id": "City"
        },
        {
            "name": names_list[1],
            "scene_id": "Space"
        },
        {
            "name": names_list[2],
            "scene_id": "Animals"
        },
        {
            "name": names_list[3],
            "scene_id": "Underwater"
        },
        {
            "name": names_list[4],
            "scene_id": "Toys"
        },
        {
            "name": names_list[5],
            "scene_id": "NewYear"
        }
    ]

    return hp_themes


def apps_json(scenes, id, name, app_topic, zone, lang, apps_keyword_list, pc_app_id=0):
    table = ['room', 'party', 'interactive']
    disco = ['disco', 'диско', 'мини', 'mini', 'dance']
    custom_app = None

    for key_word in apps_keyword_list:
        key_word = key_word.lower()
        for table_word in table:
            if table_word in key_word:
                custom_app = 'table'
                break
        for disco_word in disco:
            if disco_word in key_word:
                custom_app = 'disco'
                break

    if lang == 'ru':
        table_name = "Поздравление!"
        disco_words = ['Трек', 'Остановить', 'Следующий', 'Предыдущий', 'Включить', 'Вечеринку', 'Фоновую', 'Название трека']

    else:
        table_name = "Congratulation!"
        disco_words = ['Track', 'Stop', 'Next', 'Previos', 'Turn on', 'Party music', 'Backgrnd', "Track's name"]


    if custom_app == 'table':
        if pc_app_id !=0:
            return {
                "all_scenes": scenes,
                "all_volume": volume(lang),
                "app_id": id,
                "name": name,
                "topic_prefix": app_topic,
                "zone_id": zone,
                "custom" : [
                    {
                        "type" : "input",
                        "name" : table_name,
                        "topic" : "command/name",
                        "icon" : "mdi:triangle"
                    }
                ],
                "computer_id": pc_app_id
            }
        else:
            return {
                "all_scenes": scenes,
                "all_volume": volume(lang),
                "app_id": id,
                "name": name,
                "topic_prefix": app_topic,
                "zone_id": zone,
                "custom" : [
                    {
                        "type" : "input",
                        "name" : table_name,
                        "topic" : "command/name",
                        "icon" : "mdi:triangle"
                    }
                ]
            }
    elif custom_app == 'disco':
        if pc_app_id !=0:
            return {
                "all_scenes": scenes,
                "all_volume": volume(lang),
                "app_id": id,
                "name": name,
                "topic_prefix": app_topic,
                "zone_id": zone,
                "custom" : [
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[0],
                        "action_name" : disco_words[1],
                        "topic" : "command/pause_track",
                        "value" : ""
                    },
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[0],
                        "action_name" : disco_words[2],
                        "topic" : "command/next_track",
                        "value" : ""
                    },
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[0],
                        "action_name" : disco_words[3],
                        "topic" : "command/prev_track",
                        "value" : ""
                    },
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[4],
                        "action_name" : disco_words[5],
                        "topic" : "command/use_admin",
                        "value" : ""
                    },
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[4],
                        "action_name" : disco_words[6],
                        "topic" : "command/use_auto",
                        "value" : ""
                    },
                    {
                        "type" : "value",
                        "name" : disco_words[7],
                        "icon" : "mdi:eye",
                        "topic" : "status/current_track"
                    }
                ],
                "computer_id": pc_app_id
            }
        else:
            return {
                "all_scenes": scenes,
                "all_volume": volume(lang),
                "app_id": id,
                "name": name,
                "topic_prefix": app_topic,
                "zone_id": zone,
                "custom" : [
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[0],
                        "action_name" : disco_words[1],
                        "topic" : "command/pause_track",
                        "value" : ""
                    },
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[0],
                        "action_name" : disco_words[2],
                        "topic" : "command/next_track",
                        "value" : ""
                    },
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[0],
                        "action_name" : disco_words[3],
                        "topic" : "command/prev_track",
                        "value" : ""
                    },
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[4],
                        "action_name" : disco_words[5],
                        "topic" : "command/use_admin",
                        "value" : ""
                    },
                    {
                        "type" : "button",
                        "icon" : "mdi:texture",
                        "name" : disco_words[4],
                        "action_name" : disco_words[6],
                        "topic" : "command/use_auto",
                        "value" : ""
                    },
                    {
                        "type" : "value",
                        "name" : disco_words[7],
                        "icon" : "mdi:eye",
                        "topic" : "status/current_track"
                    }
                ]
            }
    else:
        if pc_app_id !=0:
            return {
                "all_scenes": scenes,
                "all_volume": volume(lang),
                "app_id": id,
                "name": name,
                "topic_prefix": app_topic,
                "zone_id": zone,
                "computer_id": pc_app_id
            }
        else:
            return {
                "all_scenes": scenes,
                "all_volume": volume(lang),
                "app_id": id,
                "name": name,
                "topic_prefix": app_topic,
                "zone_id": zone,
            }
