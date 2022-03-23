import time

from AI import *
import chess
import chess.engine
import chess.polyglot
from Game import *


if __name__ == "__main__":

    # the chess board
    board = chess.Board()
    # test positions
    #board.set_epd("3r2k1/p2r1p1p/1p2p1p1/q4n2/3P4/PQ5P/1P1RNPP1/3R2K1 b - - bm Nxd4; id \"position 02\";")
    board.set_fen("r1b1k2r/1p4pp/p4p2/8/3pP1nB/5P2/1q1KQ1PP/2r2B1R w kq - 0 29")

    # set this to true if you want to use an opening book
    opening = False

    #board.push(chess.Move.from_uci("d2d4"))
    Game.displayBoard(board)
    print(f"Current board evaluation: {AI.evaluateBoard(board) / 100}")

    # stockfish engine for playing the AI against
    # this exists because I don't want to have to play full
    # games against it myself to test how good it is
    # stockfish will also give me a more repeatable performance
    stockfish = chess.engine.SimpleEngine.popen_uci("C:\\Users\\Hughe\\Desktop\\arena_3.5.1\\Engines\\stockfish_14_win_x64_avx2\\stockfish_14_x64_avx2.exe")
    stockfish.configure({"UCI_LimitStrength": True, "UCI_Elo": 1350})

    # game loop
    while not board.is_game_over():
        if board.turn:
            #Game.turn(board)
            Game.fishMove(stockfish, 5, board)

        else:
            print("Black to move")
            if opening:
                try:
                    with chess.polyglot.open_reader("C:\\Users\\Hughe\\Desktop\\VSCode Projects\\Chess-Engine\\Chess\\Opening Books\\codekiddy.bin") as reader:
                        move = reader.choice(board).move
                        print(f"Moving {move} from opening book")
                        board.push(move)
                except IndexError:
                    print("Reached end of opening book\nStarting AI")
                    opening = False
            if not opening:
                start = time.time()
                AI.go(5, board, -math.inf, math.inf)
                end = time.time()
                print(f"Time spent searching: {end - start} seconds")
                print(f"Nodes per second: {AI.movesExplored / (end - start)}")
                AI.movesExplored = 0
        Game.displayBoard(board)
        print(f"Current board evaluation: {AI.evaluateBoard(board) / 100}")
        print(f"Current board FEN: {board.fen()}")

    # show who won
    if board.outcome().termination == chess.Termination.CHECKMATE:
        if board.outcome().winner:
            print("Checkmate.  White wins.")
        else:
            print("Checkmate.  Black wins.")

    else:
        print("Stalemate.  Its a draw.")
