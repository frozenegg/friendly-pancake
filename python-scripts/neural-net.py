#! /usr/bin/env python3

print('Hi, I am a chess bot!')

def main():
    done = False
    user_input = ''
    while not done:
        user_input = input('Please input move: ')
        if user_input=='E':
            done = True
        print('Your input was: '+user_input)

if __name__=='__main__':
    main()
