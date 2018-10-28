#!/usr/bin/env python3
import chess.uci
import pyautogui
import time
import mss
import mss.tools
import os
import pickle
import random
import sys

os.chdir('/Users/Pey/Documents/Tools')

engine = chess.uci.popen_engine('/Users/Pey/Downloads/stockfish/Mac/stockfish-9-bmi2')
engine.uci()

PIECES = ('n', 'q', 'r', 'k')

board = chess.Board()

UPPERLEFT = (160, 170)

BOTTOMLEFT = (160, 730)

UPPERRIGHT = (730, 160)

BOTTOMRIGHT = (730, 730)

BLOCK_SIZE = 70

TURN = True

COLOR = True

tournament = 0

blunder_count = 0

def successChance(_range):
    return 0 == random.randrange(_range)

def rollChance(_range):
    return random.randrange(_range)

def getSquareNum(mv):
    letter = ord(mv[0]) - 97
    num = int(mv[1]) - 1
    return letter + num * 8

def MakeMoveLocally(move):
    board.push(chess.Move.from_uci(move))
            
def MakeMoveGraphically(move):
    fromMv = move[:2]
    toMv = move[2:]

    x1 = BOTTOMLEFT[0] + ((ord(fromMv[0]) - 96) * BLOCK_SIZE - BLOCK_SIZE // 2)
    y1 = BOTTOMLEFT[1] - ((int(fromMv[1])) * BLOCK_SIZE - BLOCK_SIZE // 2)
    x2 = BOTTOMLEFT[0] + ((ord(toMv[0]) - 96) * BLOCK_SIZE - BLOCK_SIZE // 2)
    y2 = BOTTOMLEFT[1] - ((int(toMv[1])) * BLOCK_SIZE - BLOCK_SIZE // 2)

    pyautogui.click(x1, y1)
    pyautogui.click(x2, y2)

def takeScreenShotOfNotationList(top, left, bot, right):
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": right - left, "height": bot - top}
        output = 'notation.png'
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

def readNotationList():
    top = 189
    left = 759
    bot = 476
    right = 940
    if tournament:
        top = 266
        left = 717
        bot = 475
        right = 944
    takeScreenShotOfNotationList(top, left, bot, right)
    file = 'notation.png'
    res = os.popen('ImageToString.py -f "{}" -p 6'.format(file)).read()
    return res

def is_in_dictionary(key):
    with open(DICTIONARY_PATH, 'rb') as fp:
        dictionary = pickle.load(fp)
    return key in dictionary

def get_from_dictionary(key):
    with open(DICTIONARY_PATH, 'rb') as fp:
        dictionary = pickle.load(fp)
    return dictionary[key]

def put_to_dictionary(key, value):
    with open(DICTIONARY_PATH, 'rb') as fp:
        dictionary = pickle.load(fp)
    dictionary[key] = value
    with open(DICTIONARY_PATH, 'wb+') as fp:
        pickle.dump(dictionary, fp)

def get_last_notation():
    notationList = readNotationList()
    n = notationList.split('\n')[-2]
    n = n.split(' ')
    while len(n[-1]) == 0 or n[-1] == '-':
        del n[-1]
    print("Last notation of opponent: {}".format(n[-1]))
    return n[-1]

def isBlackTurn():
    notationList = readNotationList().replace('-', '')
    n = notationList.split('\n')[-2]
    n = n.split(' ')
    print(n)
    return len(n) <= 2

def isMyTurn():
    if COLOR:
        return not isBlackTurn()
    else:
        return isBlackTurn()

def capitalPieces(move):
    res = list()
    for i in range(len(move)):
        if move[i] in PIECES:
            res.append(move[i].upper())
        else:
            res.append(move[i])
    return ''.join(res)
    

def main():
    global COLOR
    x = pyautogui.prompt("Are you white? (y/n): ")
    pyautogui.click(x=495, y=752, clicks=2)

    if x.lower() == 'y':
        COLOR = True
    else:
        COLOR = False

    if COLOR:
        engine.position(board)
        engine.go()
        print(board)
        MakeMoveGraphically(str(engine.bestmove))
        MakeMoveLocally(str(engine.bestmove))

    try:
        while True:

            if isMyTurn():
                opponent = get_last_notation()
                try:
                    board.push_san(opponent)
                except:
                    if opponent == '-':
 #                       os.popen("say Please Enter Correct Notation")
                        opponent = capitalPieces(pyautogui.prompt("Enter Actual Opponent Move: "))
                        
                        pyautogui.click(x=495, y=752, clicks=2)
                        board.push_san(opponent)
                    else:
                        key = opponent
 #                       os.popen("say Please Enter Correct Notation")
                        opponent = capitalPieces(pyautogui.prompt("Enter Actual Opponent Move: "))
                        pyautogui.click(x=495, y=752, clicks=2)
                        board.push_san(opponent)

                engine.position(board)
                engine.go()
                print(board)
                if not engine.bestmove:
                    print("Check Mate")
                    break
                if False: # successChance(4) and blunder_count != 2:
                    gen = list(board.legal_moves)
                    roll = rollChance(len(gen))
                    try:
                        MakeMoveGraphically(str(gen[roll]))
                    except:
                        print("error here")
                        raise Exception
                    MakeMoveLocally(str(gen[roll]))
                    print("Blundered On Purpose: {}".format(gen[roll]))
                    blunder_count += 1
                else:
                    print("Made Best Move:  {}".format(str(engine.bestmove)))
                    MakeMoveGraphically(str(engine.bestmove))
                    MakeMoveLocally(str(engine.bestmove))
            
    except:
        print("CheckMate?")

if __name__ == '__main__':
    while True:
        ch = pyautogui.confirm(text='Click Start To Start Playing', title='Chess AI By Pey', buttons=['Start', 'Cancel'])
        if ch == 'Start':
            tournament = True if pyautogui.prompt("is this a tournament? (y/n): ").lower() == 'y' else False
            main()
        else:
            print("Thank you for using Chess AI")
            break
