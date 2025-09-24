import requests
import os
from dotenv import load_dotenv, find_dotenv
import re
import json

EMAIL, PASS, DC_WEBHOOK_URL, DC_USER_IDS = None, None, None, None

def get_line(text):
    for line in text:
        if re.search(r'<span id="lblSluzbaNazev".*>.*</span>', line):
            return line

def create_ping(sluzba):
    people = sluzba.split(", ")
    ping_str = ""
    
    for person in people:
        if DC_USER_IDS[person] != 0:
            ping_str += f"<@{DC_USER_IDS[person]}> "

    return ping_str

def read_secret(name):
    path = f"/run/secrets/{name}"
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return None

if find_dotenv() != '':
    load_dotenv()
    EMAIL = os.getenv("EMAIL")
    PASS = os.getenv("PASS")
    DC_WEBHOOK_URL = os.getenv("DC_WEBHOOK_URL")
    DC_USER_IDS = os.getenv("DC_USER_IDS")
else:
    EMAIL = read_secret("EMAIL")
    PASS = read_secret("PASS")
    DC_WEBHOOK_URL = read_secret("DC_WEBHOOK_URL")
    DC_USER_IDS = read_secret("DC_USER_IDS")

login_url = "https://aplikace.skolaonline.cz/SOL/Prihlaseni.aspx"
kalendar_url = "https://aplikace.skolaonline.cz/SOL/App/Kalendar/KZK001_KalendarTyden.aspx"

s = requests.Session()

s.post(login_url, data={"JmenoUzivatele": EMAIL, "HesloUzivatele": PASS, "btnLogin": "Přihlásit do aplikace"})

kalendar = s.get(kalendar_url)

sluzba_unparsed = get_line(kalendar.text.splitlines())

sluzba = re.search(r'>(.*?)</span>', sluzba_unparsed).group(1)

print(sluzba)

DC_USER_IDS = json.loads(DC_USER_IDS)

s.post(DC_WEBHOOK_URL, json={
  "content": None,
  "embeds": [
    {
      "title": sluzba,
      "color": 1288824,
      "description": create_ping(sluzba)
    }
  ],
  "attachments": []
})