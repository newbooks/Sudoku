#!/usr/bin/env python
# By Junjun Mao

import sys


class BOARD:
    def __init__(self):
        self.cell = [[0 for j in range(9)] for i in range(9)]
        self.fixed = [[0 for j in range(9)] for i in range(9)]
        return

    def load(self, fname):
        lines=open(fname).readlines()
        for i in range(9):
            line = lines[i]
            for j in range(9):
                self.cell[i][j] = self.fixed[i][j] = int(line[j])
        return

    def write(self):
        for i in range(9):
            for j in range(9):
                print("%2d" % self.cell[i][j], end="")
            print()
        return

    def valid_point(self, coordinate):
        r, c = coordinate
        value = self.cell[r][c]
        if value == 0:
            return True

         # test row
        for i in range(9):
            if value == self.cell[r][i]:
                if i != c:
                    return False

        # test column
        for i in range(9):
            if value == self.cell[i][c]:
                if i != r:
                    return False

        # test box
        k = int(r / 3)
        l = int(c / 3)
        for i in range(3):
            for j in range(3):
                x = k * 3 + i
                y = l * 3 + j
                if value == self.cell[x][y]:
                    if x != r or y != c:
                        return False

        return True

    def valid_all(self):
        for i in range(9):
            for j in range(9):
                if not self.valid_point((i,j)):
                    return False
        return True


if __name__=="__main__":
    if len(sys.argv) < 2:
        print("sokudo.py fname")
        sys.exit(0)

    board = BOARD()
    board.load(sys.argv[1])

    if not board.valid_all():
        print("Input game is not valid.")
        sys.exit(0)

    valid = True
    pointer = 0   # 0 to 80 the cell index
    forward = True
    while 0 <= pointer < 81:
        r = int(pointer / 9)
        c = pointer % 9

        if board.fixed[r][c] == 0:  # skip fixed cell

            while board.cell[r][c] < 9:
                board.cell[r][c] += 1
                if board.valid_point((r, c)):
                    forward = True
                    valid = True
                    break
                else:
                    valid = False

            if not valid:
                board.cell[r][c] = 0
                forward = False

        if forward:
            pointer += 1
        else:
            pointer += -1
        continue

    board.write()