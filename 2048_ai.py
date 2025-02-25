#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import math

from ailib import ailib, to_c_board, from_c_index

# Enable multithreading?
MULTITHREAD = True

def print_board(m):
    for row in m:
        for c in row:
            print('%8d' % c, end=' ')
        print()

def to_val(m):
    return [[from_c_index(c) for c in row] for row in m]

def _to_score(c):
    if c <= 1:
        return 0
    return (c-1) * (2**c)

def to_score(m):
    return [[_to_score(c) for c in row] for row in m]

if MULTITHREAD:
    from multiprocessing.pool import ThreadPool
    pool = ThreadPool(4)
    def score_toplevel_move(args):
        return ailib.score_toplevel_move(*args)

    def find_best_move(m):
        board = to_c_board(m)

        print_board(to_val(m))

        scores = pool.map(score_toplevel_move, [(board, move) for move in range(4)])
        bestmove, bestscore = max(enumerate(scores), key=lambda x:x[1])
        if bestscore == 0:
            return -1
        return bestmove
else:
    def find_best_move(m):
        board = to_c_board(m)
        return ailib.find_best_move(board)

def movename(move):
    return ['up', 'down', 'left', 'right'][move]

def power_of_two_exponent(n):
    if n <= 0:
        return 0
    exponent = math.log2(n)
    if exponent.is_integer():
        return int(exponent)

def main():
    # Parse the command line argument
    parser = argparse.ArgumentParser(description="Use AI to find the best move for a given 4x4 board")
    parser.add_argument('-b', '--board', help="The current 4x4 board as a flat list of 16 integers", required=True, type=int, nargs=16)
    args = parser.parse_args()

    # print(args.board)

    args.board = [power_of_two_exponent(i) for i in args.board]
    # print(args.board)

    # Reshape the 16 integers into a 4x4 matrix
    board = [args.board[i:i+4] for i in range(0, 16, 4)]

    print("Current board:")
    print_board(board)

    print('-------------------')
    # Find the best move
    best_move = find_best_move(board)

    # Print the best move
    # if best_move == -1:
    #     print("No valid moves available.")
    # else:
    #     print(f"The best move is: {movename(best_move)}")

    return best_move


if __name__ == '__main__':
    result = main()
    print(result)
