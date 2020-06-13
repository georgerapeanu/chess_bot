#!/usr/bin/python3
import requests, json, os

def get_games(user,token):

    url = "https://www.lichess.org/api/games/user/" + user

    resp = requests.get(
        url,
        params = {"max":"100"},
        headers={"Accept": "application/x-ndjson","Authorization":"Bearer " + token}
    )

    ndjson = resp.content.decode().split('\n');
    
    games = []
    for json_obj in ndjson:
        if(json_obj):
            game = json.loads(json_obj);
            if (game['variant'] != "standard") or ("aiLevel" in game['players']['white']) or ("aiLevel" in game['players']['black']) or ("georgerapeanu_bot" in game['players']['black']) or ("georgerapeanu_bot" in game['players']['white']):
                continue;
            games.append(game);
    return games;

