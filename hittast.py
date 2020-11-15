import requests
from bs4 import BeautifulSoup
import re
import json
import requests
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import locale

locale.setlocale(locale.LC_ALL, 'is_IS')

original_url = "https://www.covid.is/tolulegar-upplysingar"
r = requests.get(original_url)
soup = BeautifulSoup(r.text, "html.parser")
 
infogram_url = f'https://e.infogram.com/{soup.find("div",{"class":"infogram-embed"})["data-id"]}'
r = requests.get(infogram_url)
soup = BeautifulSoup(r.text, "html.parser")
 
 
for s in soup.findAll("script"):
  if s is not None and s.string is not None and "window.infographicData" in s.string:
    script = s.string
    extract = re.search(r".*window\.infographicData=(.*);$", script)
    data = json.loads(extract.group(1))
 
entities = data["elements"]["content"]["content"]["entities"]
 
for key in entities.keys():
  if "chartData" in entities[key]["props"]:
    if entities[key]["props"]["chartData"]["data"][0][0][1]=='Utan sóttkvíar við greiningu':
      last_three = entities[key]["props"]["chartData"]["data"][0][-7:]
      last_three_val = [int(e[1]) for e in last_three]

avg_utan = sum(last_three_val)/7

if avg_utan > 10:
  print ("Ekkert fundarboð")
else:
  with open('requestURL.txt', 'r') as file:
    request_string = file.read()

  with open('address.txt', 'r') as file:
    email = file.read()

  morgun = datetime.now()+timedelta(days=2)
  form_morg = morgun.strftime("%A %d %B")
  
  body = "Hæ hæ, það eru að meðaltali "+ locale.str(round(avg_utan,1  )) + " á dag að greinast utan sóttkvíar síðustu 7 daga. "\
    "Svo nú er mál að hittast, hvernig hljómar "+form_morg+" (í hádeginu)?  kveðja, Smári"

  payload = {
      "emailaddress": email,
      "emailsubject": "Kominn tími á hitting!",
      "emailbody": body
  }
  response = requests.post(request_string, json = payload)
  print(response.status_code)
