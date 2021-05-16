import json
import requests
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

ids = [237, 115, 140, 117, 192]
names = []
weights = []
positions = []
base_info = []


def insert_into_base(tup):
    cursor.execute("INSERT INTO goats (name, weight, position) VALUES (?,?,?)", tup)
    conn.commit()


headers = {
    'x-rapidapi-key': "f418586041msh50fd9f881c4617dp151248jsn2472ee9def72",
    'x-rapidapi-host': "free-nba.p.rapidapi.com"
}

for Id in ids:
    url = f'https://free-nba.p.rapidapi.com/players/{Id}'

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        info = response.json()
        names.append(info["first_name"] + ' ' + info["last_name"])
        weights.append(round(info["weight_pounds"] * 0.453592))
        positions.append(info['position'])


url2 = 'https://free-nba.p.rapidapi.com/players/237'
data = requests.request("GET", url2, headers=headers).json()

with open('basket.json', 'w') as file:
    file.write(json.dumps(data, indent=4))


conn = sqlite3.connect('Basketball.sqlite')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE goats
               (name varchar(50),
                weight int,
                position char(5));""")

conn.commit()

for i in range(len(names)):
    insert_into_base((names[i], weights[i], positions[i]))

conn.close()

x = np.arange(len(names))
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(x, weights, width, label='Men')

ax.set_ylabel('Weight in KG')
ax.set_title('Weights of NBA players')
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=9.5)

ax.bar_label(rects1, padding=3)

plt.show()
