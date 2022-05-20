import sqlite3 as sl
from bs4 import BeautifulSoup as bs

conn = sl.connect("apps/db.sqlite3")

INSERT_SQL = "INSERT INTO PLAYERINFO (name, id, birthday, residency) VALUES('{}', '{}', '{}', '{}')"
SELECT_SQL = "SELECT * FROM PLAYERINFO WHERE name='{}'"

f = open("playerinfo.xml", "r", encoding="utf-8")
soup = bs(markup=f, features="xml")
playerlist = soup.find_all("player")
for player in playerlist:
    id = player["id"]
    realname = player.realname.text
    birthday = player.birthday.text
    residency = player.residency.text
    res = conn.execute(SELECT_SQL.format(realname))
    if len(list(res)) == 0:
        conn.execute(INSERT_SQL.format(realname, id, birthday, residency))
        print(id)

conn.commit()
