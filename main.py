#!/usr/bin/python3.6
import chessGame;
import time;

def __main__():
    print("gameid");
    gameid = str(input()).replace('\n','');
    print("token");
    token = str(input()).replace('\n','');
    game = chessGame.chessGame(gameid,token);
    while(True):
        game.make_move();
        time.sleep(5);

__main__();
