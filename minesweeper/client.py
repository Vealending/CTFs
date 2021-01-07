#!/usr/bin/env python3

import grpc
import minesweeper_pb2
import minesweeper_pb2_grpc

def main():

    channel = grpc.insecure_channel('minesweeper:1989')
    stub = minesweeper_pb2_grpc.MinesweeperStub(channel)

    next_Game_ID = ""

    while True:

        print("Requesting new board...")
        print(next_Game_ID)

        if not next_Game_ID:
            start_Game = minesweeper_pb2.NewGameRequest()
            board_ID = stub.NewGame(start_Game)
            print("1st level")
        else:
            board_ID = minesweeper_pb2.StartLevelRequest(levelID=next_Game_ID)
            print("2nd level")
        print(board_ID)
        board_Info = stub.StartLevel(board_ID)
        print(board_Info)
        mines_Amount = board_Info.Mines
        mines_Response = []
        board_Array = [ ["#"] * board_Info.Columns for i in range(board_Info.Rows) ]
        probability_Array = [ [0] * board_Info.Columns for i in range(board_Info.Rows) ]

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

            squares_To_Check = []
            safe_Squares = []

            for row in range(board_Info.Rows):
                for col in range(board_Info.Columns):
                    if board_Array[row][col] == "-":
                        squares_To_Check = get_Surr_Squares(row, col)
                    for s in squares_To_Check:
                        tile_Click(s[0], s[-1])

        def corner_check(r, c):

            safe_amount = 0
            surr_Squares = get_Surr_Squares(r, c)

            if len(surr_Squares) == 8:
                for s in surr_Squares:
                    if board_Array[s[0]][s[-1]] == "-":
                        safe_amount += 1
                if safe_amount >= 4:
                    for s in surr_Squares:
                        if board_Array[s[0]][s[-1]] == "#":
                            board_Array[s[0]][s[-1]] = "F"
                            mines_Response.append(minesweeper_pb2.Position(row=s[0],column=s[-1]))

        def mine_Check():

            squares_To_Check = []
            surr_Squares = []
            square_Value = 0
            flagged = 0
            unknown = 0

            for row in range(board_Info.Rows): #get all non-emtpy squares
                for col in range(board_Info.Columns):
                    if not board_Array[row][col] == "-":
                        squares_To_Check.append([row, col])

            for s in squares_To_Check:
                square_Value = board_Array[s[0]][s[-1]]

                corner_check(s[0], s[-1])

                surr_Squares = get_Surr_Squares(s[0],s[-1])
                flagged = 0
                unknown = 0

                for surr in surr_Squares: #find flagged squares surrounding the square
                    if board_Array[surr[0]][surr[-1]] == "F":
                        flagged += 1
                    elif board_Array[surr[0]][surr[-1]] == "#":
                        unknown += 1

                if isinstance(square_Value, int): 
                    if int(square_Value) == flagged:
                        print("Match!", s)
                        print(surr_Squares)
                        for sq in surr_Squares:
                            if board_Array[sq[0]][sq[-1]] == "#": 
                                print("clicked something idno")
                                tile_Click(sq[0], sq[-1])
                                #idno
                    elif int(square_Value) == flagged + unknown
                        print("Match!", s)
                        print(surr_Squares)
                        for sq in surr_Squares:
                            if board_Array[sq[0]][sq[-1]] == "#": 
                                print("clicked something idno")
                                tile_Click(sq[0], sq[-1])
                                #idno


        for row in board_Array:
            print(*row)

        tile_Click(0,0)
        open_Safe()
        mine_Check()

        print("---------------------------------")

        for row in board_Array:
            print(*row)

        if len(mines_Response) == mines_Amount:
                next_Game_ID = send_Mines()

if __name__ == '__main__':
        main()
