#!/usr/bin/env python
# By Junjun Mao
# Before simplifying: user 1min45.673s 1m50.403s

import sys


def conflict(test):
    flags=[0 for i in range(9)]
    for i in range(9):    
        if test[i] > 0:
            flags[test[i]-1] += 1
    for i in range(9):
        if flags[i] > 1:
            return True
    return False
    
class BOARD:
    def __init__(self):
        self.unit=[[0 for j in range(9)] for i in range(9)]
        return
    def load(self,fname):
        lines=open(fname).readlines()
        cline = 0
        for j in range(9):
            line = lines[j]
            for i in range(9):
                self.unit[cline][i]= int(line[i])
            cline += 1
        return
    def write(self):
        for i in range(9):
            for j in range(9):
                print("%2d" % self.unit[i][j], end="")
            print()
        return
    def zeros(self):
        count=0
        for rows in self.unit:
            for unit in rows:
                if unit ==0: count += 1
        return count
    
    def copy(self):
        board_copy=BOARD()
        for i in range(9):
            for j in range(9):
                board_copy.unit[i][j]=self.unit[i][j]
        return board_copy   
    def valid(self):
        "board conflicts?"
        #Validify cell
        for i in range(3):
            for j in range(3):
                test=[]
                for k in range(3):
                    for l in range(3):
                        test.append(self.unit[i*3+k][j*3+l])
                if conflict(test):
                    return False
        
        #Validify row
        for i in range(9):
            test=[]
            for j in range(9):
                test.append(self.unit[i][j])
            if conflict(test):
                return False
            
        #Validify column
        for i in range(9):
            test=[]
            for j in range(9):
                test.append(self.unit[j][i])
            if conflict(test):
                return False
        return True
    
def min_cell(board):
    Min = 9 

    # find which cell has the minimum unfilled units.
    flags=[[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3):
        for j in range(3):
            for x in range(3):
                for y in range(3):
                    if board.unit[i*3+x][j*3+y] == 0:
                       flags[i][j]+=1    
    for i in range(3):
        for j in range(3):
            if flags[i][j] < Min and flags[i][j] > 0:
                Min = flags[i][j]
                Min_cell=("cell", i, j)
    
    # find which row has the minimum unfilled units
    flags=[0,0,0,0,0,0,0,0,0]
    for i in range(9):
        for j in range(9):
            if board.unit[i][j] == 0:
                flags[i] += 1
    for i in range(9):
        if flags[i] < Min and flags[i]>0:
            Min = flags[i]
            Min_cell=("row", i)

    # find which column has the minimum unfilled units
    flags=[0,0,0,0,0,0,0,0,0]
    for i in range(9):
        for j in range(9):
            if board.unit[j][i] == 0:
                flags[i] += 1
    for i in range(9):
        if flags[i] < Min and flags[i]>0:
            Min = flags[i]
            Min_cell=("col", i)
             
    return (Min, Min_cell)

def all_perms(str):
    if len(str) <=1:
        yield str
    else:
        for perm in all_perms(str[1:]):
            for i in range(len(perm)+1):
                yield perm[:i] + str[0:1] + perm[i:]


def spawn(board):
    Min, Min_cell = min_cell(board)
    if Min == 0: return([])
    
    root = []
    if Min_cell[0] == "cell":
        for i in range(3):
            for j in range(3):
                root.append(board.unit[Min_cell[1]*3+i][Min_cell[2]*3+j])
    elif Min_cell[0] == "row":
        for i in range(9):
            root.append(board.unit[Min_cell[1]][i])
    elif Min_cell[0] == "col":
        for i in range(9):
            root.append(board.unit[i][Min_cell[1]])
             
    #Get position of fillables (0) and nummers to be filled
    fills=[1,2,3,4,5,6,7,8,9]
    fills_index=[]    
    for i in range(9):
        if root[i] == 0:
            fills_index.append(i)
        else:
            fills.pop(fills.index(root[i]))
    
    # Generate permutations and assign back to the plain array
    spawned = []
    for p in all_perms(fills):
        #print p
        root_copy=[i for i in root]
        board_copy=board.copy()        
        for i in fills_index:
            root_copy[i]=p.pop(0)
        #print root, root_copy
        #Convert it back to board
        if Min_cell[0] == "cell":
            for i in range(3):
                for j in range(3):
                    #print Min_cell[1]*3+i,Min_cell[2]*3+j,root_copy[0], root_copy
                    board_copy.unit[Min_cell[1]*3+i][Min_cell[2]*3+j]=root_copy.pop(0)
        elif Min_cell[0] == "row":
            for i in range(9):
                board_copy.unit[Min_cell[1]][i]=root_copy.pop(0)
        elif Min_cell[0] == "col":
            for i in range(9):
                board_copy.unit[i][Min_cell[1]]=root_copy.pop(0)
        #board_copy.write()
        spawned.append(board_copy)
    return spawned
    
if __name__=="__main__":
    if len(sys.argv) < 2:
        print("sokudo.py fname")
        sys.exit(0)

    Q=[]
    solutions=[]
    
    board=BOARD()
    board.load(sys.argv[1])
    if board.valid():
        Q.append(board)
    else:
        print("Input game is not valid.")
        sys.exit(0)
    
    count = 0
    while len(Q) > 0:
        count += 1
        motherboard=Q.pop()
        zeros=motherboard.zeros()
        if zeros == 0:
            motherboard.write()
            print()
            break

        #print("Cycle %d: Q = %d, to be filled = %d" % (count,len(Q), zeros))
        #motherboard.write()
        raw=spawn(motherboard)
        for new_board in raw:
            #new_board.write()
            #print
            if new_board.valid():
                Q.append(new_board)

