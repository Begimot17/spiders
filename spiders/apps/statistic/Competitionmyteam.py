import requests
import json
from datetime import datetime

url = 'http://spiders.espressoresearch.com/sandbox/json?filter%5Bstatuses%5D%5Bunassigned%5D%5Btitle%5D=Unassigned&filter%5Bstatuses%5D%5Bunassigned%5D%5Blabel%5D=btn-primary&filter%5Bstatuses%5D%5Bunassigned%5D%5Bactive%5D=0&filter%5Bstatuses%5D%5Bopen%5D%5Btitle%5D=Open&filter%5Bstatuses%5D%5Bopen%5D%5Blabel%5D=btn-success&filter%5Bstatuses%5D%5Bopen%5D%5Bactive%5D=0&filter%5Bstatuses%5D%5Bin_progress%5D%5Btitle%5D=In+progress&filter%5Bstatuses%5D%5Bin_progress%5D%5Blabel%5D=btn-default&filter%5Bstatuses%5D%5Bin_progress%5D%5Bactive%5D=0&filter%5Bstatuses%5D%5Bqa%5D%5Btitle%5D=Waiting+for+QA&filter%5Bstatuses%5D%5Bqa%5D%5Blabel%5D=btn-danger&filter%5Bstatuses%5D%5Bqa%5D%5Bactive%5D=0&filter%5Bstatuses%5D%5Bcant_implement%5D%5Btitle%5D=Can%27t+implement&filter%5Bstatuses%5D%5Bcant_implement%5D%5Blabel%5D=btn-warning&filter%5Bstatuses%5D%5Bcant_implement%5D%5Bactive%5D=0&filter%5Bstatuses%5D%5Bdone%5D%5Btitle%5D=Done&filter%5Bstatuses%5D%5Bdone%5D%5Blabel%5D=btn-default&filter%5Bstatuses%5D%5Bdone%5D%5Bactive%5D=0&filter%5Bworkflow_alert_filter_mask%5D=0'
headers = {"Host": "spiders.espressoresearch.com",
           "X-Requested-With": "XMLHttpRequest",
           "Cookie": "_ga=GA1.2.1556227278.1642414774; remember_82e5d2c56bdd0811318f0cf078b78bfc=eyJpdiI6IkVxSWZQWEpHczl5c2hHZjl6c29TWVE9PSIsInZhbHVlIjoidXRlWWNsb1pRWVJJSFNrUVc3XC8xYk5OdlZnbWx2QzdjWmJ0NE9ZYTBvVlQzRFFHSHMwZnR3d3dVT1ludW5BTzNnTThDYVBJM0JRWWNzZ2l6VU1XcGhcL1ByQlIxNFpBeEpvM01pd2hDUXc0OD0iLCJtYWMiOiJiNjkzZTZhYWE1MGIzY2M5ZGZlOWM4MWE3N2ZjZDAyNGIyMjYwZWE4MjZlZGFmNzI3NWIwMTQ1ZTA2MWFiZjJjIn0%3D; _fbp=fb.1.1642674508063.1528221733; _mgt_visid=70638707; _hjSessionUser_1266088=eyJpZCI6ImJmNGE0MjdjLWFiNGYtNTZiZi05NjJiLThhYjk3ZDMxODhmZCIsImNyZWF0ZWQiOjE2NDI2NzQ1MDgzODYsImV4aXN0aW5nIjpmYWxzZX0=; __atuvc=1%7C3; _gid=GA1.2.587024358.1644231259; laravel_session=eyJpdiI6IjBWOGRNRHpvek1zdTFWNUVQKzM4cnc9PSIsInZhbHVlIjoidWRERTUzWVRqOEpYSVF0dmRcL1Q5eVZwRFZ2T25wODY2OWlqTlVBS1pmT05aSDN6dng1M2Vqb0JyZzJcL2ltZlNQXC95T2xKK25HU2tmak96OVBDN2NoZ1E9PSIsIm1hYyI6Ijg1ZmE5YTYyMjkzYjQ1MGM1YWQ4MGRmMTBjYmM5MTFlZjU3NTUxOGJlMzQ4YmIxYWViYjE1MjcwNzZmNTUyZDUifQ%3D%3D"}


class Player(object):
    def __init__(self, key):
        """Constructor"""
        self.done_source=0
        self.done_fix=0
        self.key=key
        self.fix=0
        self.minute = 0
        self.new=0
        self.closed=0
        self.in_progress=0
        self.open=0
        self.done =0
        self.name=None
        self.all=0


pl_keys = [1321, 1319, 1320, 1688, 1542, 1135, 1182, 1186, 1128]
players = []
statuses = ["done", "open", "in_progress", "closed","started_date"]
post = {"rowCount": 100000}
post_index = 0


def add_to_post(value, type):
    global post, post_index
    search = {f"searchPhrase[{post_index}][value]": f"{value}",
              f"searchPhrase[{post_index}][name]": f"f[{type}][]"}
    post = {**post, **search}
    post_index += 1


def initial_post():
    for st in statuses:
        add_to_post(st, "status")
    for pl in players:
        add_to_post(pl.key, "users")


def get_json():
    initial_post()
    response = requests.post(url, headers=headers, data=post)
    return json.loads(response.text)


def search_player(key):
    for pl in players:
        if pl.key == key:
            return pl


def add_point(key, status, source_type, name, started_date,date):
    if started_date>date:
        pl = search_player(key)
        if pl.name == None:
            pl.name = name
        if status == "Done":
            if source_type == 1:
                pl.minute+=60
                pl.done_source+=1
            elif source_type == 2:
                pl.done_fix+=1
                pl.minute+=35
            pl.done += 1
        elif status == "Open":
            pl.open += 1
        elif status == "In progress":
            pl.in_progress += 1
        elif status == "Closed":
            pl.closed += 1
        if source_type == 1:
            pl.new += 1
        elif source_type == 2:
            pl.fix += 1
        pl.all += 1


def loading(date,filter_id):
    for a in get_json()["rows"]:
        status = a['status']
        if filter_id==2 and a['done_at']==None:
            continue
        else:
            if filter_id==2 :
                filter_date=a['done_at']
            else:
                filter_date = a['started_at']
            if a["sources"]:
                source_type = a["sources"][0]["type"]
            if a["user"]:
                name = a["user"]["name"]
                key = a["user"]["id"]
                if filter_date==None:
                    filter_date='2022-01-01 08:00:01'
                started = datetime.strptime(filter_date, '%Y-%m-%d %H:%M:%S')
            add_point(key, status, source_type, name,started,date)


def main(filter_id=0,date=datetime.strptime('2000-01-01 08:00:00', '%Y-%m-%d %H:%M:%S')):
    global  players
    players = [Player(key=x) for x in pl_keys]
    loading(date,filter_id)
    # for pl in players:
    #     print(f"{pl.name}   {pl.key}\n")
    #     print(f"done-{pl.done}  open-{pl.open}  in_progress-{pl.in_progress}  closed-{pl.closed} ")
    #     print(f"new source-{pl.new} fix-{pl.fix}")
    #     print(f"all-{pl.all}\n\n")
    return players



