#!/usr/bin/python3.6
import chess,os,json,requests
import chess_feeder

class chessGame:
    gameid = "";
    token = "";
    
    def __init__(self,gameid,token):
        self.gameid = gameid;
        self.token = token;

    def make_move(self):
        board = chess.Board();
        resp = requests.get("https://lichess.org/game/export/" + self.gameid,headers={"Accept": "application/json","Authorization":"Bearer " + self.token});
        ndjson = resp.content.decode();
        game = json.loads(ndjson);
        moves = str(game['moves']).split(' ');
        if(len(moves) == 1 and moves[0] == ''):
            moves = [];
        board = chess.Board();
        black = False;
        if('user' in game['players']['black'] and game['players']['black']['user']['name'] == "georgerapeanu_bot"):
            if len(moves) == 0:
                return False;
            black = True
            moves[0] = board.parse_san(moves[0]);
            tmp_moves = [];
            for move in moves:
                tmp_move = "";
                for c in str(move):
                    if ord('0') <= ord(c) and ord(c) <= ord('9'):
                        tmp_move = tmp_move + (chr((9 - (ord(c) - ord('0'))) + ord('0')));
                    else:
                        tmp_move = tmp_move + c;
                tmp_moves.append(tmp_move);
            moves = tmp_moves[::];
            
            fen = board.fen();
            new_fen = "";
            i = 0;
            while(fen[i] != ' '):
                new_fen = new_fen + (fen[i]);
                i = i + 1;
            new_fen = new_fen + (fen[i]);
            i = i + 1;
            new_fen = new_fen + ('b');
            i = i + 1;
            while(i < len(fen)):
                new_fen = new_fen + (fen[i]);
                i = i + 1;
            board = chess.Board(new_fen);
            board.push(chess.Move.from_uci(moves[0]));
            moves = moves[1::];
        
        for i in range(0,len(moves)):
            board.push(board.parse_san(moves[i]));
        if(len(moves) % 2 == 0):
            activations = chess_feeder.get_activations(board);
            ##to add nn
            print("please move")
            print(str(board));
            move = str(input())
            if(black == True):
                tmp = "";
                for x in move:
                    if ord('0') <= ord(c) and ord(c) <= ord('9'):
                        tmp = tmp + (chr((9 - (ord(c) - ord('0'))) + ord('0')));
                    else:
                        tmp = tmp + c;
                move = tmp;
                    
            resp = requests.post("https://lichess.org/api/bot/game/" + self.gameid + "/move/" + move,headers={"Accept": "application/json","Authorization":"Bearer " + self.token});
            print(str(resp.content));
            return True;
        return False;
