from random import randrange, random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import os
from urllib.request import Request, urlopen
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

name = ''
ability_name = ''

req = Request("https://pokeapi.co/api/v2/pokemon/", headers={'User-Agent': 'Mozilla/5.0'})#
response = urlopen(req)
count = json.loads(response.read())["count"]

req = Request(f"https://pokeapi.co/api/v2/pokemon/?limit={count}", headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(req)
pokemons = json.loads(response.read())["results"]


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.text:
        for pokemon in pokemons:
            if (event.text).lower() == pokemon['name']:
                print(pokemon['url'])
                req = Request(pokemon['url'], headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(req)
                desc = json.loads(response.read())
                message = f"Имя:{desc['name']}\nРост:{desc['height']}\nВес:{desc['weight']}"
                
                vk.messages.send(user_id=event.user_id, message=message, random_id=randrange(1,10000))





'''def get_data_from(url, key):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})  #
    response = urlopen(req)
    data = json.loads(response.read())[key]
    return data'''

'''for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.text:
        for pokemon in pokemons:
            if (event.text).lower() == pokemon['name']:
                name = pokemon['name']
                abilitys = get_data_from(pokemon['url'], 'abilities')
                # vk.messages.send(user_id=event.user_id, message=name, random_id=randrange(0,10000))
                for ability in abilitys:
                    ability_name = ability['ability']['name']
                    print(ability_name)
                    effects_desc = get_data_from(ability['ability']['url'], 'effect_changes')
                    vk.messages.send(user_id=event.user_id,
                                     message=f'Name: {name}, '
                                     f'Ability:   {ability_name}',
                                     random_id=randrange(0, 10000))'''
        # for el in pokemons:
        #     if (event.text).lower() == el['name']:
        #         req = Request(el['url'], headers={'User-Agent': 'Mozilla/5.0'})
        #         response = urlopen(req)
        #         abilities = json.loads(response.read())['abilities']
        #         for ability in abilities: #abilitie is dict
        #             ability_name = ability['ability']['name']
        #             url =  ability['ability']['url']
        #             req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        #             response = urlopen(req)
        #             ability_info = json.loads(response.read())['effect_changes']
        #
        #             for group_name in ability_info:
        #                 print(group_name['version_group']['name'])
        #                 for effect in ability_info:
        #                     for effect_lang in effect['effect_entries']:
        #                         if effect_lang["language"]['name'] == "en":
        #                             vk.messages.send(user_id=event.user_id,
        #                                              message=f"Name: {el['name']},\n"
        #                                                     f" Ability: {ability_name},\n"
        #                                                     f"Group_name:{group_name['version_group']['name']}"
        #                                                     f" Effect: {effect_lang['effect']}",
        #                                             random_id=randrange(1,10000))



            # url = next((url for url, value in el.items() if value == event.text), None)
            # print(url)