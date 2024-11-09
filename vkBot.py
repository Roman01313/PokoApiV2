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

try:
    req = Request("https://pokeapi.co/api/v2/pokemon/", headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    count = json.load(response.read())["count"]

    req = Request(f"https://pokeapi.co/api/v2/pokemon/?limit={count}", headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    pokemons = json.loads(response.read())["results"]
except:
    print("Error001")

for event in longpoll.listen():
    pass