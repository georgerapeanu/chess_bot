#!/usr/bin/python3
import requests, json, os

def get_games(user,path,token):

    if os.path.isdir(path) == False:
        print("ERROR game directory doesn't exist")
        return ;
  
    os.chdir(path);

    url = "https://www.lichess.org/api/games/user/" + user

    resp = requests.get(
        url,
        params = {},
        headers={"Accept": "application/x-ndjson","Authorization":"Bearer " + token}
    )

    ndjson = resp.content.decode().split('\n');

    for json_obj in ndjson:
        if(json_obj):
            game = json.loads(json_obj);
            if (game['variant'] == "fromPosition") or ("aiLevel" in game['players']['white']) or ("aiLevel" in game['players']['black']):
                continue;
            game_str = json.dumps(game, ensure_ascii = False, indent = 4)
            open(game['id'] + ".json","w").write(game_str);


