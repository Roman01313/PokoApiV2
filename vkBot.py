from pyexpat.errors import messages
from random import randrange, random
from time import perf_counter

import vk_api
from setuptools.extern import names
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


req = Request("https://pokeapi.co/api/v2/pokemon/", headers={'User-Agent': 'Mozilla/5.0'})#
response = urlopen(req)
count = json.loads(response.read())["count"]

req = Request(f"https://pokeapi.co/api/v2/pokemon/?limit={count}", headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(req)
pokemons = json.loads(response.read())["results"]



for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.text:
        for el in pokemons:
            if (event.text).lower() == el['name']:
                req = Request(el['url'], headers={'User-Agent': 'Mozilla/5.0'})
                response = urlopen(req)
                abilities = json.loads(response.read())['abilities']
                for ability in abilities: #abilitie is dict
                    ability_name = ability['ability']['name']
                    url =  ability['ability']['url']
                    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    response = urlopen(req)
                    ability_info = json.loads(response.read())['effect_changes']

                    for group_name in ability_info:
                        print(group_name['version_group']['name'])
                        for effect in ability_info:
                            for effect_lang in effect['effect_entries']:
                                if effect_lang["language"]['name'] == "en":
                                    # print(effect_lang['effect'])
                                    pass
                                    # vk.messages.send(user_id=event.user_id,
                                    #                  message=f"Name: {el['name']},\n"
                                    #                         f" Ability: {ability_name},\n"
                                    #                         f"Group_name:{group_name['version_group']['name']}"
                                    #                         f" Effect: {effect_lang['effect']}",
                                    #                 random_id=randrange(1,10000))



            # url = next((url for url, value in el.items() if value == event.text), None)
            # print(url)
