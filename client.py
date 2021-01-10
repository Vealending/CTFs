#!/usr/bin/env python3

import grpc
import minesweeper_pb2
import minesweeper_pb2_grpc
import random
import time

def main():

    channel = grpc.insecure_channel('minesweeper:1989')
    stub = minesweeper_pb2_grpc.MinesweeperStub(channel)

    next_Game_ID = ""
    level = 1

    while True:

        print("Requesting new board...")

        if not next_Game_ID:
            start_Game = minesweeper_pb2.NewGameRequest()
            board_ID = stub.NewGame(start_Game)
        else:
            board_ID = minesweeper_pb2.StartLevelRequest(levelID=next_Game_ID)
            level += 1
        print("Level", level)
        print(board_ID)
        board_Info = stub.StartLevel(board_ID)
        print(board_Info)
        mines_Amount = board_Info.Mines
        mines_Response = []
        board_Array = [ ["#"] * board_Info.Columns for i in range(board_Info.Rows) ]
        temp_Array = []

        def tile_Click(r, c):

            click_Tile = minesweeper_pb2.Position(row=r,column=c)
            click_Request = minesweeper_pb2.ClickRequest(levelID=board_ID.levelID, tile=click_Tile)
            click_Response = stub.Click(click_Request)
            if click_Response.value:
                board_Array[r][c] = click_Response.value
            elif not click_Response.error:
                board_Array[r][c] = "-"
            return click_Response

        def send_Mines():

            mine_Solve = minesweeper_pb2.SolveLevelRequest(levelID=board_ID.levelID, mines=mines_Response)
            level_Response = stub.SolveLevel(mine_Solve)
            next_Game_ID = level_Response.nextLevelID
            print("Flag:", level_Response.flag)
            return next_Game_ID

        def board_Check(board, temp):
            if temp == board:
                print("Stale... clicking something")
                click_Random()
            temp = board

        def get_Unchecked():

            unchecked_Array = []

            for row in range(board_Info.Rows):
                for col in range(board_Info.Columns):
                    if board_Array[row][col] == "#":
                        unchecked_Array.append([row, col])
            
            return unchecked_Array


        def print_Board(board):

            print("---------------------------------")
            for row in board:
                print(*row)

        def click_Random():
            
            unchecked = get_Unchecked()
            rand = random.choice(unchecked)
            print(rand)

            tile_Click(rand[0], rand[-1])

        def get_Surr_Squares(r, c):

            surr_Squares = []

            if not r == 0 and not c == 0: #topleft
                surr_Squares.append([r - 1, c - 1])
            if not r == 0: #top
                surr_Squares.append([r - 1, c])
            if not r == 0 and not c == board_Info.Columns - 1: #topright
                surr_Squares.append([r - 1, c + 1])
            if not c == 0: #left
                surr_Squares.append([r, c - 1])
            if not c == board_Info.Columns - 1: #right
                surr_Squares.append([r, c + 1])
            if not r == board_Info.Rows - 1 and not c == 0: #bottomleft
                surr_Squares.append([r + 1, c - 1])
            if not r == board_Info.Rows - 1: #bottom
                surr_Squares.append([r + 1, c])
            if not r == board_Info.Rows - 1 and not c == board_Info.Columns - 1: #bottomright
                surr_Squares.append([r + 1, c + 1])

            return surr_Squares

        def open_Safe():

            safe_Squares = []

            for row in range(board_Info.Rows):
                for col in range(board_Info.Columns):
                    if board_Array[row][col] == "-":
                        safe_Squares = get_Surr_Squares(row, col)
                    for s in safe_Squares:
                        if board_Array[s[0]][s[-1]] == "#":
                            tile_Click(s[0], s[-1])

        def mine_Check():

            squares_To_Check = []
            surr_Squares = []
            square_Value = 0
            unchecked = 0
            unchecked_Total = 0
            flagged = 0

            for row in range(board_Info.Rows): # get all non-empty squares
                for col in range(board_Info.Columns):
                    if not board_Array[row][col] == "-" and not board_Array[row][col] == "F":
                        squares_To_Check.append([row, col])

            for s in squares_To_Check:

                square_Value = board_Array[s[0]][s[-1]]
                surr_Squares = get_Surr_Squares(s[0],s[-1])
                unchecked = 0
                flagged = 0

                for surr in surr_Squares:
                    if board_Array[surr[0]][surr[-1]] == "F":
                        flagged += 1
                    elif board_Array[surr[0]][surr[-1]] == "#":
                        unchecked += 1

                if isinstance(square_Value, int): 

                    if int(square_Value) == flagged: #rule 2
                        for surr in surr_Squares:
                            if board_Array[surr[0]][surr[-1]] == "#": 
                                tile_Click(surr[0], surr[-1])

                    elif int(square_Value) == unchecked + flagged: #rule 1
                        for surr in surr_Squares:
                            if board_Array[surr[0]][surr[-1]] == "#": 
                                board_Array[surr[0]][surr[-1]] = "F"
                                mines_Response.append(minesweeper_pb2.Position(row=surr[0], column=surr[-1]))

                    if len(surr_Squares) < 6: #border check
                        if int(square_Value) == 1:

                            print("Edge 1 check activated :O")

                            row = surr[0]
                            col = surr[0]
                            try:
                                if board_Array[row - 1][col] == "-" and board_Array[row + 1][col] == "#" and isinstance(board_Array[row][col + 1], int):
                                    print("clicked", row + 1, col + 2)
                                    tile_Click(row + 1, col + 2)
                            except IndexError:
                                pass
                            try:
                                if board_Array[row - 1][col] == "-" and board_Array[row + 1][col] == "#" and isinstance(board_Array[row][col - 1], int):
                                    print("clicked", row + 1, col - 2)
                                    tile_Click(row + 1, col - 2)
                            except IndexError:
                                pass
                            try:
                                if board_Array[row][col - 1] == "-" and board_Array[row][col + 1] == "#" and isinstance(board_Array[row + 1][col], int):
                                    print("clicked", row + 2, col + 1)
                                    tile_Click(row + 2, col + 1)
                            except IndexError:
                                pass
                            try:
                                if board_Array[row][col - 1] == "-" and board_Array[row][col + 1] == "#" and isinstance(board_Array[row - 1][col], int):
                                    print("clicked", row - 2, col + 1)
                                    tile_Click(row - 2, col + 1)
                            except IndexError:
                                pass

            for row in range(board_Info.Rows):
                for col in range(board_Info.Columns):
                    if board_Array[row][col] == "#":
                        unchecked_Total += 1

            if unchecked_Total == mines_Amount - len(mines_Response):
                for row in range(board_Info.Rows):
                    for col in range(board_Info.Columns):
                        if board_Array[row][col] == "#":
                            board_Array[row][col] = "F"
                            mines_Response.append(minesweeper_pb2.Position(row=row, column=col))

        tile_Click(0,0)

        while len(mines_Response) != mines_Amount:

            open_Safe()
            mine_Check()
            print_Board(board_Array)
            time.sleep(0.1)

        next_Game_ID = send_Mines()

if __name__ == '__main__':
        main()
