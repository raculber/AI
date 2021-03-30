#!/usr/bin/env python
# coding: utf-8

import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt


def ret_img(b, chess, n=4):
    cv = np.zeros_like(b)
    for x in range(n):
        for y in range(n):
            if chess[x,y]==1:
                cv[x*128:(x+1)*128:,y*128:(y+1)*128:,:] = bb
                break
    cv = cv2.addWeighted(cv,0.5,b,0.5,0)
    return cv

"""
Problem: Place N queens on chessboard such that no two queens are in same row, column, and diagonal.
"""

# make a chessboard of 8x8 or 4x4 initially having no queen.
# 0 = queen absent at the block
# 1 = queen present
"""You are responsible for editing this function"""
def isSafe(chess, row, col,n=4):
    """YOUR CODE STARTS HERE"""
    """Verify if row is safe"""
    for x in range(n):
        if chess[row][x] == 1:
            return False

    """Verify if diagonals are safe"""
    i = row
    j = col 
    while i >= 0 and j >= 0:
        if chess[i][j] == 1:
            return False
        i -= 1
        j -= 1
    i = row
    j = col 
    while j >= 0 and i < n:
        if chess[i][j] == 1:
            return False
        i += 1
        j -= 1
    """YOUR CODE ENDS HERE"""
    return True
    raise NotImplementedError("Function isSafe NOT IMPLEMENTED")

"""You are responsible for editing this function"""
def dfs(chess, curr_column, n=4):
    global counter
    
    if curr_column > n-1:
        return

    for row in range(0, n):
        counter += 1
        """YOUR CODE STARTS HERE"""

        """Clear all the previous rows"""
        for r in range(0, row+1):
            chess[r][curr_column] = 0


        """HINT: when array confuse you just do array.shape"""
        """print('row column', row, curr_column)"""
        if isSafe(chess, row, curr_column, n):
            chess[row][curr_column] = 1
            dfs(chess, curr_column+1, n=4)
            if curr_column == n-1:
                """DO NOT edit this section"""
                print('moves:', counter)
                img = ret_img(b, chess, n)
                cv2.imwrite(os.path.join(path,str(counter)+".png"), img)
                # plt.imshow(img)
                print(chess)
                """"DO NOT edit this section"""

        """YOUR CODE ENDS HERE"""
    return chess
    raise NotImplementedError("Function isSafe NOT IMPLEMENTED")


if __name__ == "__main__":

    arg = sys.argv
    n = 4
    if len(arg) > 1:
        n = arg[1]
    path = str(n)+"Queen"
    assert int(n) == 4 or int(n) == 8, "Number of Queens should be 4 or 8"
    b = cv2.imread(os.path.join("res", "1024px-Chess_Board.svg.png"))
    bb = cv2.imread(os.path.join("res", "bb.png"))
    # bb = cv2.cvtColor(bb,cv2.COLOR_BGR2RGB)
    bb = cv2.resize(bb, (128, 128))
    if not os.path.exists(path):
        os.makedirs(path)
    elif path == "4Queen":
        b = b[:512, :512, :]
    counter = 0
    # Creating an empty chess board
    chess = np.full((int(n),int(n)), 0)

    #start putting queens one by one
    chess = dfs(chess, 0, int(n))
    img = ret_img(b, chess, int(n))
    plt.imshow(img)



