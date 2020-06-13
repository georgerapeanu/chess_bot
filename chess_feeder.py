#!/usr/bin/python3.6
import chess,os,json

def get_activations(board):
    activations = [];
    for x in str(board).replace('\n','').replace(' ',''):
        activations.append(1 if x == 'R' else 0);
        activations.append(1 if x == 'N' else 0);
        activations.append(1 if x == 'B' else 0);
        activations.append(1 if x == 'Q' else 0);
        activations.append(1 if x == 'K' else 0);
        activations.append(1 if x == 'P' else 0);
        activations.append(1 if x == 'r' else 0);
        activations.append(1 if x == 'n' else 0);
        activations.append(1 if x == 'b' else 0);
        activations.append(1 if x == 'q' else 0);
        activations.append(1 if x == 'k' else 0);
        activations.append(1 if x == 'p' else 0);
    return activations

def get_output_activations(move):
    activations = []
    for c in range(ord('a'),ord('h') + 1):
        for i in range(ord('1'),ord('8') + 1):
            for c2 in range(ord('a'),ord('h') + 1):
                for j in range(ord('1'), ord('8') + 1):
                    activations.append(1 if move == str(str(chr(c)) + str(chr(i)) + str(chr(c2)) + str(chr(j))) else 0)
    return activations;

def feed_games(games):
    inputs = [];
    outputs = [];
    
    for game in games:
        print("processing " + game['id'])
        moves = str(game['moves']).split(' ');
        if(len(moves) == 1 and moves[0] == ''):
            moves = [];
        if len(moves) == 0:
            continue;
        board = chess.Board();
        if('user' in game['players']['black'] and game['players']['black']['user']['name'] == "georgerapeanu"):
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
        
        for i in range(0,len(moves),2):
            inputs.append(get_activations(board))
            outputs.append(get_output_activations(str(board.parse_san(moves[i]))));
            board.push(board.parse_san(moves[i]));
            if(i + 1 < len(moves)):
                board.push(board.parse_san(moves[i + 1]));

    return (inputs,outputs);
            
