#!/usr/bin/python3.6
import chess,os,json,requests
import chess_feeder
import numpy
from keras.models import model_from_json

class chessGame:
    gameid = "";
    token = "";
    model = None;
    def __init__(self,gameid,token):
        self.gameid = gameid;
        self.token = str(token);
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        #load weights into new model
        self.model.load_weights("model.h5")
        print("Loaded model from disk")

    def make_move(self):
        print("moving");
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
            activations = numpy.array([chess_feeder.get_activations(board)]);
            predictions = self.model.predict(activations);
            ind = 0;
            bst_move = "";
            bst_cost = -1e9;
            for c in range(ord('a'),ord('h') + 1):
                for i in range(ord('1'),ord('8') + 1):
                    for c2 in range(ord('a'),ord('h') + 1):
                        for j in range(ord('1'), ord('8') + 1):
                            if (c,i) != (c2,j) and ((chess.Move.from_uci(str(str(chr(c)) + str(chr(i)) + str(chr(c2)) + str(chr(j)))) in board.legal_moves and bst_cost <= predictions[0][ind])):
                                bst_move = str(str(chr(c)) + str(chr(i)) + str(chr(c2)) + str(chr(j)));
                                bst_cost = predictions[0][ind];
                            ind = ind + 1;
            move = bst_move;
            if(black == True):
                tmp = "";
                for c in move:
                    if ord('0') <= ord(c) and ord(c) <= ord('9'):
                        tmp = tmp + (chr((9 - (ord(c) - ord('0'))) + ord('0')));
                    else:
                        tmp = tmp + c;
                move = tmp;
            
            print(move);        
            resp = requests.post("https://lichess.org/api/bot/game/" + self.gameid + "/move/" + move,headers={"Accept": "application/json","Authorization":"Bearer " + self.token});
            print(str(resp.content));
            return True;
        return False;
