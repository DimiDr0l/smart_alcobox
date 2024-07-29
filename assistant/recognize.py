from speak import play_wav
from fuzzywuzzy import fuzz
import glob_var

sys_alias= ('наливатор', 'наливать')

command_dic = {
    "help": ('список команд', 'команды', 'что ты умеешь', 'твои навыки', 'навыки'),
    # "about": ('расскажи о себе', 'что ты такое', 'ты кто', 'о себе'),
    "volup": ('громче', 'добавь громкость', 'сделай громче', 'добавь звук'),
    "voldown": ('тише', 'убавь громкость', 'сделай тише', 'убавь звук'),
    "volset": ('установи уровень громкости', 'уровень громкости', 'громкость на'),
    # "tost": ("расскажи тост", "скажи тост", "тост"),
    "spill": ('наливай', 'разливай', 'наливатор', 'налей нам'),
    "shutdown": ('выключись', 'выключайся'),
    "change_voice": ('смени голос', 'смени ассистента')
}

# python 3.9 no support match case
    # match key:
    #     case 'help':
    #         # f_help()
    #         print('f_help()')
    #     case 'about':
    #         # f_about()
    #         print('f_about()')
    #     case 'volup':
    #         # f_volup()
    #         print('f_volup()')
    #     case 'voldown':
    #         # f_voldown()
    #         print('f_voldown()')
    #     case 'volset':
    #         # f_volset()
    #         print('f_volset()')
    #     case 'tost':
    #         # f_tost()
    #         print('f_tost()')
    #     case _:
    #         print('Нет данных')

def recognize_command(cmd: str):
    similarity_percent = 80
    command = 'no_data'
    for c, v in command_dic.items():
        for x in v:
            similarity = fuzz.ratio(cmd, x)
            # print(f"{cmd:}\nСовпадение команды: {similarity}% | Ключ: {c}")
            if similarity >= similarity_percent:
                command = c
                return command
    return command

def name_recognize(name: str):
    words = name.split()
    stat = False
    for item in sys_alias:
        similarity = fuzz.ratio(item, words[0])
        if similarity > 80:
            stat = True
    return stat
