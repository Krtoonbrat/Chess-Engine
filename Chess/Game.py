import re
import string

import chess
import chess.engine


# class wrapping all the game functions
class Game:

    # makes a move using stockfish
    @staticmethod
    def fishMove(fish, limit, board):
        move = fish.play(board, chess.engine.Limit(depth=limit), info=chess.engine.Info.SCORE)
        fishScore = move.info['score'].relative.score()
        if isinstance(fishScore, int):
            print(f"Stockfish analysis score: {move.info['score'].relative.score() / 100}")
        else:
            print("Stockfish analysis score: Checkmate")
        print(f"Stockfish moving: {move.move}")
        board.push(move.move)

    # displays the board
    @staticmethod
    def displayBoard(board):
        letters = string.ascii_lowercase[:8]

        # if it is white's turn, show the board from white's perspective
        if board.turn == chess.WHITE:
            # print dashes for formatting
            print("  " + "-" * 65)

            for row in range(8, 0, -1):
                # first row of lines
                print("  |", end="")
                for space in range(8):
                    print("       |", end="")
                print("")

                # display current row
                print(row, end="")

                # start the board with a vertical line
                print(" |", end="")

                # iterate through each item in the current row
                # if there isnt a piece, 5 spaces are printed
                # if there is a piece, the piece's identifying string is printed
                # and formatted to fit in the center of 5 characters with spaces on either side
                for square in range(8):
                    piece = board.piece_at(chess.square(square, row - 1))
                    if piece is not None:
                        if piece.color:
                            if piece.piece_type == chess.PAWN:
                                print("{0:^7}|".format("wp"), end="")
                            elif piece.piece_type == chess.KNIGHT:
                                print("{0:^7}|".format("wkn"), end="")
                            elif piece.piece_type == chess.BISHOP:
                                print("{0:^7}|".format("wb"), end="")
                            elif piece.piece_type == chess.ROOK:
                                print("{0:^7}|".format("wr"), end="")
                            elif piece.piece_type == chess.QUEEN:
                                print("{0:^7}|".format("wq"), end="")
                            elif piece.piece_type == chess.KING:
                                print("{0:^7}|".format("wk"), end="")
                        else:
                            if piece.piece_type == chess.PAWN:
                                print("{0:^7}|".format("bp"), end="")
                            elif piece.piece_type == chess.KNIGHT:
                                print("{0:^7}|".format("bkn"), end="")
                            elif piece.piece_type == chess.BISHOP:
                                print("{0:^7}|".format("bb"), end="")
                            elif piece.piece_type == chess.ROOK:
                                print("{0:^7}|".format("br"), end="")
                            elif piece.piece_type == chess.QUEEN:
                                print("{0:^7}|".format("bq"), end="")
                            elif piece.piece_type == chess.KING:
                                print("{0:^7}|".format("bk"), end="")
                    else:
                        print("       |", end="")

                # final row of lines
                print("\n  |", end="")
                for space in range(8):
                    print("       |", end="")

                # when the current row is finished printing, go to a new line and print the dashes to complete formatting
                print("\n  ", end="")
                print("-" * 65)

            # after each space in the board is printed, print the letter labels
            # for each column at the bottom
            print("      ", end="")
            for lower in letters:
                print("{}       ".format(lower), end="")

            print("")

        # if it is black's turn, show the board from black's perspective
        else:
            # print dashes for formatting
            print("  " + "-" * 65)

            for row in range(0, 8):
                # first row of lines
                print("  |", end="")
                for space in range(8):
                    print("       |", end="")
                print("")

                # display current row
                print(row + 1, end="")

                # start the board with a vertical line
                print(" |", end="")

                # iterate through each item in the current row
                # if there isnt a piece, 5 spaces are printed
                # if there is a piece, the piece's identifying string is printed
                # and formatted to fit in the center of 5 characters with spaces on either side
                for square in range(8, 0, -1):
                    piece = board.piece_at(chess.square(square - 1, row))
                    if piece is not None:
                        if piece.color:
                            if piece.piece_type == chess.PAWN:
                                print("{0:^7}|".format("wp"), end="")
                            elif piece.piece_type == chess.KNIGHT:
                                print("{0:^7}|".format("wkn"), end="")
                            elif piece.piece_type == chess.BISHOP:
                                print("{0:^7}|".format("wb"), end="")
                            elif piece.piece_type == chess.ROOK:
                                print("{0:^7}|".format("wr"), end="")
                            elif piece.piece_type == chess.QUEEN:
                                print("{0:^7}|".format("wq"), end="")
                            elif piece.piece_type == chess.KING:
                                print("{0:^7}|".format("wk"), end="")
                        else:
                            if piece.piece_type == chess.PAWN:
                                print("{0:^7}|".format("bp"), end="")
                            elif piece.piece_type == chess.KNIGHT:
                                print("{0:^7}|".format("bkn"), end="")
                            elif piece.piece_type == chess.BISHOP:
                                print("{0:^7}|".format("bb"), end="")
                            elif piece.piece_type == chess.ROOK:
                                print("{0:^7}|".format("br"), end="")
                            elif piece.piece_type == chess.QUEEN:
                                print("{0:^7}|".format("bq"), end="")
                            elif piece.piece_type == chess.KING:
                                print("{0:^7}|".format("bk"), end="")
                    else:
                        print("       |", end="")

                # final row of lines
                print("\n  |", end="")
                for space in range(8):
                    print("       |", end="")

                # when the current row is finished printing, go to a new line and print the dashes to complete formatting
                print("\n  ", end="")
                print("-" * 65)

            # after each space in the board is printed, print the letter labels
            # for each column at the bottom
            print("      ", end="")
            for lower in letters[::-1]:
                print("{}       ".format(lower), end="")

            print("")

    # goes through the process of a turn
    @staticmethod
    def turn(board):

        # tell the user whose turn it is
        if board.turn == chess.WHITE:
            print("White to move")
        else:
            print("Black to move")

        # get the player move
        playerMove = input("Your Move? ").lower().split()

        # turn first coordinates into squares
        if re.fullmatch("[a-h][1-8]", playerMove[0]):
            pieceCoordinates = chess.parse_square(playerMove[0])
        else:
            print("Ill-formatted move.")
            Game.turn(board)

        # turn second coordinates into squares
        if re.fullmatch("[a-h][1-8]", playerMove[1]):
            targetCoordinates = chess.parse_square(playerMove[1])
        else:
            print("Ill-formatted move.")
            Game.turn(board)

        # pawn promotion
        while True:
            if board.piece_type_at(pieceCoordinates) == chess.PAWN and (
                    (chess.square_rank(targetCoordinates) == 7 and board.turn == chess.WHITE) or (
                    chess.square_rank(targetCoordinates) == 0 and board.turn == chess.BLACK)):
                promotion = input("Please chose a piece to promote to.  1:Queen, 2:Rook, 3:Knight, 4:Bishop: ")
                if re.fullmatch("[1-4]", promotion):
                    if promotion == '1':
                        move = chess.Move(pieceCoordinates, targetCoordinates, chess.QUEEN)
                    elif promotion == '2':
                        move = chess.Move(pieceCoordinates, targetCoordinates, chess.ROOK)
                    elif promotion == '3':
                        move = chess.Move(pieceCoordinates, targetCoordinates, chess.KNIGHT)
                    elif promotion == '4':
                        move = chess.Move(pieceCoordinates, targetCoordinates, chess.BISHOP)
                    break
            else:
                move = chess.Move(pieceCoordinates, targetCoordinates)
                break

        # check to see if the move is legal
        if move in board.legal_moves:
            board.push(move)
        else:
            print("Illegal move.")
            Game.turn(board)