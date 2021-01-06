#!/usr/bin/env python3

import grpc
import minesweeper_pb2
import minesweeper_pb2_grpc

def main():
    
    channel = grpc.insecure_channel('minesweeper:1989')
    stub = minesweeper_pb2_grpc.MinesweeperStub(channel)
    print("Requesting board ID...")
    start_Game = minesweeper_pb2.NewGameRequest()
    board_ID = stub.NewGame(start_Game)
    print(board_ID)
    board_Info = stub.StartLevel(board_ID)
    board_Array = [ ["?"] * board_Info.Columns for i in range(board_Info.Rows)]

    def tile_Click(r, c):

        click_Tile = minesweeper_pb2.Position(row=r,column=c)
        click_Request = minesweeper_pb2.ClickRequest(levelID=board_ID.levelID, tile=click_Tile)
        click_Response = stub.Click(click_Request)
        if click_Response.value:
            board_Array[r][c] = click_Response.value
        else:
            board_Array[r][c] = " "
        return click_Response

    def bruteforce():
        for row in range(board_Info.Rows):
            for col in range(board_Info.Columns):
                if not tile_Click(row, col):
                    print("Hit a mine!")
                    board_Array[row][col] = "X"
                    return                

    bruteforce()

    for row in board_Array:
        print(*row)

if __name__ == '__main__':
        main()