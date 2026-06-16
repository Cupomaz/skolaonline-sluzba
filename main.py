import requests
import os
import re

EMAIL, PASS, DC_WEBHOOK_URL = None, None, None

def get_line(text):
    for line in text:
        if re.search(r'<span id="lblSluzbaNazev".*>.*</span>', line):
            return line
    return None

EMAIL = os.getenv("EMAIL")
PASS = os.getenv("PASS")
DC_WEBHOOK_URL = os.getenv("DC_WEBHOOK_URL")

login_url = "https://aplikace.skolaonline.cz/SOL/Prihlaseni.aspx"
kalendar_url = "https://aplikace.skolaonline.cz/SOL/App/Kalendar/KZK001_KalendarTyden.aspx"

s = requests.Session()

s.post(login_url, data={"JmenoUzivatele": EMAIL, "HesloUzivatele": PASS, "btnLogin": "Přihlásit do aplikace"})

kalendar = s.get(kalendar_url)

sluzba_unparsed = get_line(kalendar.text.splitlines())

if sluzba_unparsed is None:
    s.post(DC_WEBHOOK_URL, json={
      "content": "Služba není definována",
      "embeds": [],
      "attachments": []
    })
else:
    sluzba = re.search(r'>(.*?)</span>', sluzba_unparsed).group(1)
    sluzba = re.sub(r'</?b>', '', sluzba)

    print(sluzba)

    s.post(DC_WEBHOOK_URL, json={
      "content": None,
      "embeds": [
        {
          "title": sluzba,
          "color": 1288824,
        }
      ],
      "attachments": []
    })