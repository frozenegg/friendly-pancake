#! /usr/bin/env python3

import chess

board = chess.Board()

def main():
    print('Hello! Input \'Exit\' to exit board')
    user_input = ''
    while True:
        print(board)
        user_input = input('Please input move: ')
        if user_input=='Exit':
            exit()
        try:
            chess.Move.from_uci(user_input)
        except ValueError: 
            print('**ERROR**:  Move not possible!')
            continue
        if not chess.Move.from_uci(user_input) in board.legal_moves:
            print('**ERROR**:  Move not legal!')
        else :
            board.push_uci(user_input)

if __name__=='__main__':
    main()
