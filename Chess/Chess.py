import copy
import math
import random
import re
import string
import time

import chess
import chess.engine
import chess.polyglot

# the chess board
board = chess.Board()


# class wrapping all the game functions
class Game:

    # makes a move using stockfish
    @staticmethod
    def fishMove(fish, limit):
        move = fish.play(board, chess.engine.Limit(time=limit), info=chess.engine.Info.SCORE)
        fishScore = move.info['score'].relative.score()
        if isinstance(fishScore, int):
            print(f"Stockfish analysis score: {move.info['score'].relative.score() / 100}")
        else:
            print("Stockfish analysis score: Checkmate")
        print(f"Stockfish moving: {move.move}")
        board.push(move.move)

    # displays the board
    @staticmethod
    def displayBoard():
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
    def turn():

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
            Game.turn()

        # turn second coordinates into squares
        if re.fullmatch("[a-h][1-8]", playerMove[1]):
            targetCoordinates = chess.parse_square(playerMove[1])
        else:
            print("Ill-formatted move.")
            Game.turn()

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
            Game.turn()


# class representing a position stored in the transposition table
class Node:
    def __init__(self, type=None, best=None, score=None, pv=None, depth=None):
        self.nodeType = type
        self.bestMove = best
        self.nodeScore = score
        self.PV = pv
        self.nodeDepth = depth


# class wrapping all the AI variables and functions
# noinspection SpellCheckingInspection
class AI:
    # the number of moves a current search has explored
    movesExplored = 0
    quiesceExplored = 0

    # amount of transposed moves
    movesTransposed = 0

    # transposition tables
    transpoTable = {}
    pawnTranspoTable = {}

    # number of cut nodes and alpha/beta specific cuts
    cutNodes = 0
    alphaCuts = 0
    betaCuts = 0

    # base values for all the pieces
    # white gets a positive value, black a negitive
    pieceScores = {'P': 100, 'N': 320, 'B': 300, 'R': 500, 'Q': 900, 'K': 20000, 'p': -100, 'n': -320, 'b': -300,
                   'r': -500, 'q': -900, 'k': -20000}

    # piece square tables
    blackPawnSquareTable = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [50, 50, 50, 50, 50, 50, 50, 50],
                            [10, 10, 20, 30, 30, 20, 10, 10],
                            [5, 5, 10, 25, 25, 10, 5, 5],
                            [0, 0, 0, 20, 20, 0, 0, 0],
                            [-5, -5, 10, 0, 0, 10, -5, -5],
                            [5, 10, 5, -20, -20, 5, 10, 5],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
    whitePawnSquareTable = blackPawnSquareTable.copy()
    whitePawnSquareTable.reverse()
    blackKnightSquareTable = [[-50, -40, -30, -30, -30, -30, -40, -50],
                              [-40, -20, 0, 0, 0, 0, -20, -40],
                              [-30, 0, 10, 15, 15, 10, 0, -30],
                              [-30, 5, 15, 20, 20, 15, 5, -30],
                              [-30, 0, 15, 20, 20, 15, 0, -30],
                              [-30, 5, 10, 15, 15, 10, 5, -30],
                              [-40, -20, 0, 5, 5, 0, -20, -40],
                              [-50, -10, -30, -30, -30, -30, -10, -50]]
    whiteKnightSquareTable = blackKnightSquareTable.copy()
    whiteKnightSquareTable.reverse()
    blackBishopSquareTable = [[-20, -10, -10, -10, -10, -10, -10, -20],
                              [-10, 0, 0, 0, 0, 0, 0, -10],
                              [-10, 0, 5, 10, 10, 5, 0, -10],
                              [-10, 5, 5, 10, 10, 5, 5, -10],
                              [-10, 0, 10, 10, 10, 10, 0, -10],
                              [-10, 10, 10, 10, 10, 10, 10, -10],
                              [-10, 5, 0, 0, 0, 0, 5, -10],
                              [-20, -10, -10, -10, -10, -10, -10, -20]]
    whiteBishopSquareTable = blackBishopSquareTable.copy()
    whiteBishopSquareTable.reverse()
    blackRookSquareTable = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [5, 10, 10, 10, 10, 10, 10, 5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [-5, 0, 0, 0, 0, 0, 0, -5],
                            [0, 0, 0, 5, 5, 5, 0, 0]]
    whiteRookSquareTable = blackRookSquareTable.copy()
    whiteRookSquareTable.reverse()
    blackQueenSquareTable = [[-20, -10, -10, -5, -5, -10, -10, -20],
                             [-10, 0, 0, 0, 0, 0, 0, -10],
                             [-10, 0, 5, 5, 5, 5, 0, -10],
                             [-5, 0, 5, 5, 5, 5, 0, -5],
                             [0, 0, 5, 5, 5, 5, 0, -5],
                             [-10, 5, 5, 5, 5, 5, 0, -10],
                             [-10, 0, 5, 0, 0, 0, 0, -10],
                             [-20, -10, -10, -5, -5, -10, -10, -20]]
    whiteQueenSquareTable = blackQueenSquareTable.copy()
    whiteQueenSquareTable.reverse()
    blackKingSquareTable = [[-30, -40, -40, -50, -50, -40, -40, -30],
                            [-30, -40, -40, -50, -50, -40, -40, -30],
                            [-30, -40, -40, -50, -50, -40, -40, -30],
                            [-30, -40, -40, -50, -50, -40, -40, -30],
                            [-20, -30, -30, -40, -40, -30, -30, -20],
                            [-10, -20, -20, -20, -20, -20, -20, -10],
                            [20, 20, 0, 0, 0, 0, 20, 20],
                            [20, 30, 10, 0, 0, 10, 30, 20]]
    whiteKingSquareTable = blackKingSquareTable.copy()
    whiteKingSquareTable.reverse()

    # statically evaluates and gives a score to the current board
    @staticmethod
    def evaluateBoard(board):
        # evaluates pawn structure
        def pawnStructure():
            pawnScore = 0
            whitePawns = board.pieces(chess.PAWN, chess.WHITE)
            blackPawns = board.pieces(chess.PAWN, chess.BLACK)
            combined = whitePawns.union(blackPawns)

            if combined.mask in AI.pawnTranspoTable.keys():
                return AI.pawnTranspoTable[combined.mask]

            for square in whitePawns:
                # isolated pawns
                file = chess.square_file(square)
                if file == 0:
                    if whitePawns.isdisjoint(chess.BB_FILES[file + 1]):
                        pawnScore -= 5
                elif file == 7:
                    if whitePawns.isdisjoint(chess.BB_FILES[file - 1]):
                        pawnScore -= 5
                elif whitePawns.isdisjoint(chess.BB_FILES[file + 1]) and whitePawns.isdisjoint(
                        chess.BB_FILES[file - 1]):
                    pawnScore -= 5

                # defended pawns
                if len(board.attackers(chess.WHITE, square).intersection(whitePawns)) > 0:
                    pawnScore += 10

                # passed pawns
                if blackPawns.isdisjoint(chess.BB_FILES[file]):
                    pawnScore += 15

            for square in blackPawns:
                # isolated pawns
                file = chess.square_file(square)
                if file == 0:
                    if blackPawns.isdisjoint(chess.BB_FILES[file + 1]):
                        pawnScore += 5
                elif file == 7:
                    if blackPawns.isdisjoint(chess.BB_FILES[file - 1]):
                        pawnScore += 5
                elif blackPawns.isdisjoint(chess.BB_FILES[file + 1]) and blackPawns.isdisjoint(
                        chess.BB_FILES[file - 1]):
                    pawnScore += 5

                # defended pawns
                if len(board.attackers(chess.BLACK, square).intersection(blackPawns)) > 0:
                    pawnScore -= 10

                # passed pawns
                if whitePawns.isdisjoint(chess.BB_FILES[file]):
                    pawnScore -= 15

            # find doubled pawns
            for file in chess.BB_FILES:
                fileSet = chess.SquareSet(file)
                whiteInter = fileSet.intersection(whitePawns)
                blackInter = fileSet.intersection(blackPawns)

                if len(whiteInter) > 1:
                    pawnScore -= 20

                if len(blackInter) > 1:
                    pawnScore += 20

            AI.pawnTranspoTable[combined.mask] = pawnScore
            return pawnScore

        # set the score to zero
        score = 0

        # returns a value if the current board state is a finished game
        if board.is_game_over():
            # if the game ended in checkmate, return infinity if white won, and negative infinity if black won
            if board.outcome().termination == chess.Termination.CHECKMATE:
                if board.outcome().winner:
                    return math.inf
                else:
                    return -math.inf
            # if the game ended from any kind of stalemate, return a zero
            else:
                return 0

        # get a dictionary of all the pieces with their squares as keys
        pieces = board.piece_map()

        # loop through the dictionary and add all the piece values together
        for square in pieces.keys():
            if pieces[square].color:
                if pieces[square].piece_type == chess.PAWN:
                    score += AI.pieceScores[pieces[square].symbol()] + \
                             AI.whitePawnSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.KNIGHT:
                    score += AI.pieceScores[pieces[square].symbol()] + \
                             AI.whiteKnightSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.BISHOP:
                    score += AI.pieceScores[pieces[square].symbol()] + \
                             AI.whiteBishopSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.ROOK:
                    score += AI.pieceScores[pieces[square].symbol()] + \
                             AI.whiteRookSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.QUEEN:
                    score += AI.pieceScores[pieces[square].symbol()] + \
                             AI.whiteQueenSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.KING:
                    score += AI.pieceScores[pieces[square].symbol()] + \
                             AI.whiteKingSquareTable[chess.square_rank(square)][chess.square_file(square)]
            else:
                if pieces[square].piece_type == chess.PAWN:
                    score += AI.pieceScores[pieces[square].symbol()] - \
                             AI.blackPawnSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.KNIGHT:
                    score += AI.pieceScores[pieces[square].symbol()] - \
                             AI.blackKnightSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.BISHOP:
                    score += AI.pieceScores[pieces[square].symbol()] - \
                             AI.blackBishopSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.ROOK:
                    score += AI.pieceScores[pieces[square].symbol()] - \
                             AI.blackRookSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.QUEEN:
                    score += AI.pieceScores[pieces[square].symbol()] - \
                             AI.blackQueenSquareTable[chess.square_rank(square)][chess.square_file(square)]
                elif pieces[square].piece_type == chess.KING:
                    score += AI.pieceScores[pieces[square].symbol()] - \
                             AI.blackKingSquareTable[chess.square_rank(square)][chess.square_file(square)]

        # add bonus for bishop pair
        if len(board.pieces(chess.BISHOP, chess.WHITE)) == 2:
            score += 25
        if len(board.pieces(chess.BISHOP, chess.BLACK)) == 2:
            score -= 25

        # add pawn structure bonus
        score += pawnStructure()

        return score

    @staticmethod
    def moveOrder(moves, board, PV, depth, node):
        def MVVLVA(move):
            if board.is_en_passant(move):
                return abs(AI.pieceScores[board.piece_at(board.peek().to_square).symbol()]) - abs(
                    AI.pieceScores[board.piece_at(move.from_square).symbol()])
            return abs(AI.pieceScores[board.piece_at(move.to_square).symbol()]) - abs(
                AI.pieceScores[board.piece_at(move.from_square).symbol()])

        orderedMoves = []

        if PV[-depth] != 0 and chess.Move.from_uci(PV[-depth]) in moves:
            orderedMoves.append(chess.Move.from_uci(PV[-depth]))
        elif node.bestMove != None:
            orderedMoves.append(node.bestMove)

        regicide = []
        attackers = []
        checks = []
        captures = []
        zeroing = []
        castling = []
        other = []

        queens = board.pieces(chess.QUEEN, not board.turn)

        if len(queens) != 0:
            for royalty in queens:
                if board.is_attacked_by(board.turn, royalty):
                    for assassin in board.attacks(royalty):
                        murder = chess.Move(assassin, royalty)
                        if board.is_legal(murder):
                            regicide.append(murder)
                            moves.remove(murder)

        lastMove = board.pop()
        if board.is_capture(lastMove):
            board.push(lastMove)
            if board.is_attacked_by(board.turn, board.peek().to_square):
                for retaliation in board.attackers(board.turn, board.peek().to_square):
                    if board.is_legal(chess.Move(retaliation, board.peek().to_square)) and chess.Move(retaliation,
                                                                                                      board.peek().to_square) not in regicide:
                        MAD = chess.Move(retaliation, board.peek().to_square)
                        attackers.append(MAD)
                        moves.remove(MAD)
        else:
            board.push(lastMove)

        for move in moves:
            if board.is_capture(move):
                captures.append(move)
            elif board.gives_check(move):
                checks.append(move)
            elif board.is_zeroing(move):
                zeroing.append(move)
            elif board.is_castling(move):
                castling.append(move)
            else:
                other.append(move)

        captures.sort(key=MVVLVA, reverse=True)
        attackers.sort(key=MVVLVA, reverse=True)
        regicide.sort(key=MVVLVA, reverse=True)

        orderedMoves.extend(regicide)
        orderedMoves.extend(attackers)
        orderedMoves.extend(captures)
        orderedMoves.extend(checks)
        orderedMoves.extend(zeroing)
        orderedMoves.extend(castling)
        orderedMoves.extend(other)

        return orderedMoves

    @staticmethod
    def quiesce(alpha, beta, Qdepth):
        if Qdepth <= 0:
            if board.turn:
                return AI.evaluateBoard(board)
            return -AI.evaluateBoard(board)

        # transposition lookup
        hash = chess.polyglot.zobrist_hash(board)
        if hash in AI.transpoTable.keys():
            node = AI.transpoTable[hash]
            if node.nodeType == 1:
                AI.movesTransposed += 1
                return node.nodeScore
        else:
            node = Node(1)
            AI.transpoTable[hash] = node

        if board.turn:
            standPat = AI.evaluateBoard(board)
            node.nodeScore = standPat
        else:
            standPat = -AI.evaluateBoard(board)
            node.nodeScore = standPat

        if standPat >= beta:
            node.nodeType = 2
            return beta
        if standPat > alpha:
            alpha = standPat

        captures = [move for move in board.legal_moves if board.is_capture(move)]

        if captures != []:
            for move in captures:
                board.push(move)
                AI.quiesceExplored += 1
                AI.movesExplored += 1
                score = -AI.quiesce(-beta, -alpha, Qdepth - 1)
                board.pop()

                if score >= beta:
                    node.nodeType = 2
                    return beta
                if score > alpha:
                    node.nodeScore = score
                    alpha = score
            return alpha
        else:
            return standPat

    @staticmethod
    def minimax(depth, isMaximizer, alpha, beta, PV, currentLine, finalDepth, searchDepth):
        if depth <= 0:
            # do a Qsearch if we are at the final depth
            if finalDepth:
                if board.turn:
                    return AI.quiesce(alpha, beta, 3), currentLine
                else:
                    return -AI.quiesce(alpha, beta, 3), currentLine
            return AI.evaluateBoard(board), currentLine

        # transposition lookup
        hash = chess.polyglot.zobrist_hash(board)
        if hash in AI.transpoTable.keys():
            node = AI.transpoTable[hash]
            if node.nodeDepth == searchDepth:
                if node.nodeType == 1:
                    AI.movesTransposed += 1
                    return node.nodeScore, node.PV
                elif node.nodeType == 2:
                    alpha = max(node.nodeScore, alpha)
                elif node.nodeType == 3:
                    beta = min(node.nodeScore, beta)
            else:
                node.nodeDepth = searchDepth
        else:
            if board.turn:
                node = Node(1, depth=searchDepth, score=-math.inf)
            else:
                node = Node(1, depth=searchDepth, score=math.inf)
            AI.transpoTable[hash] = node

        moveList = AI.moveOrder(list(board.legal_moves), board, PV, depth, node)

        # if it is whites turn
        if isMaximizer:
            # initial max score
            maxScore = -math.inf

            # loop through all the legal moves, make the move, score it, then undo the move
            for move in moveList:
                currentLine[-depth] = chess.Move.uci(move)
                board.push(move)
                AI.movesExplored += 1
                depth -= 1
                score, PVreturn = AI.minimax(depth, False, alpha, beta, PV, currentLine, finalDepth, searchDepth)
                depth += 1
                if score > maxScore:
                    maxScore = score
                    node.nodeScore = score
                    node.bestMove = move
                    node.PV = copy.copy(PVreturn)
                alpha = max(score, alpha)
                board.pop()
                if maxScore >= beta:
                    AI.cutNodes += 1
                    AI.betaCuts += 1
                    node.nodeType = 2
                    break
            return maxScore, node.PV

        # if it is blacks turn
        else:
            # initial min score
            minScore = math.inf

            # loop through all the legal moves, make the move, score it, then undo the move
            for move in moveList:
                currentLine[-depth] = chess.Move.uci(move)
                board.push(move)
                AI.movesExplored += 1
                depth -= 1
                score, PVreturn = AI.minimax(depth, True, alpha, beta, PV, currentLine, finalDepth, searchDepth)
                depth += 1
                if score < minScore:
                    minScore = score
                    node.nodeScore = score
                    node.bestMove = move
                    node.PV = copy.copy(PVreturn)
                beta = min(score, beta)
                board.pop()
                if minScore <= alpha:
                    AI.cutNodes += 1
                    AI.alphaCuts += 1
                    node.nodeType = 3
                    break
            return minScore, node.PV

    # starts the minimax algorithm and actually keeps track of and makes the best move
    @staticmethod
    def go(depth, alpha, beta):

        bestScore = math.inf
        bestMove = None
        PV = []
        finalDepth = False
        deep = 1
        aspMisses = 0
        misses = []

        # prepare the move list
        # for redundancy if we need to grab a random move
        moveListRaw = list(board.legal_moves)

        # iterative deepening loop
        while not finalDepth:
            currentLine = [0 for x in range(deep)]

            # sets final depth flag
            if deep == depth:
                finalDepth = True

            if len(PV) != deep:
                PV.append(0)

            # perform minimax search
            bestScore, PV = AI.minimax(deep, False, alpha, beta, PV, currentLine, finalDepth, deep)
            # If there is checkmate, there will be no best move, so an error will be raised
            # in that case, just pick a random one
            try:
                bestMove = chess.Move.from_uci(PV[0])
            except:
                bestMove = random.choice(moveListRaw)

            # check to see if we found mate
            if bestScore == math.inf or bestScore == -math.inf:
                break

            # set the aspiration window
            # search was outside the window, need to redo the search
            if bestScore <= alpha or bestScore >= beta:
                alpha = -math.inf
                beta = math.inf
                finalDepth = False
                aspMisses += 1
                misses.append(deep)
            # the search didn't fall outside the window, we can move on to the next depth
            else:
                alpha = bestScore - 50 * (aspMisses + 1)
                beta = bestScore + 50 * (aspMisses + 1)
                deep += 1
            # best move and best score need to be reset at the end of each loop
            # the move list will also need to be sorted
            # otherwise the next iteration will have out of date data comparing to new data
            if not finalDepth:
                bestScore = math.inf
                bestMove = None

        print("Total moves explored: ", AI.movesExplored)
        print(f"Total Quiescence Moves Searched: {AI.quiesceExplored}")
        print("Moves transposed: ", AI.movesTransposed)
        print(f"Moving: {bestMove} with a score of {bestScore / 100}")
        print(f"Cut nodes: {AI.cutNodes}, Alpha cuts: {AI.alphaCuts}, Beta cuts: {AI.betaCuts}")
        print(f"Aspiration Window Misses: {aspMisses}, at depth(s): {misses}")
        print(f"PV: {PV}")
        AI.quiesceExplored = 0
        AI.movesTransposed = 0
        AI.cutNodes = 0
        AI.alphaCuts = 0
        AI.betaCuts = 0
        AI.transpoTable.clear()
        board.push(bestMove)


if __name__ == "__main__":

    opening = False

    #board.push(chess.Move.from_uci("d2d4"))
    Game.displayBoard()
    print(f"Current board evaluation: {AI.evaluateBoard(board) / 100}")

    # stockfish engine for playing the AI against
    # this exists because I don't want to have to play full
    # games against it myself to test how good it is
    # stockfish will also give me a more repeatable performance
    stockfish = chess.engine.SimpleEngine.popen_uci("")
    stockfish.configure({"UCI_LimitStrength": True, "UCI_Elo": 1350})

    # game loop
    while not board.is_game_over():
        if board.turn:
            #Game.turn()
            Game.fishMove(stockfish, 1)

        else:
            print("Black to move")
            if opening:
                try:
                    with chess.polyglot.open_reader("OPENING BOOK GOES HERE") as reader:
                        move = reader.choice(board).move
                        print(f"Moving {move} from opening book")
                        board.push(move)
                except IndexError:
                    print("Reached end of opening book\nStarting AI")
                    opening = False
            if not opening:
                start = time.time()
                AI.go(5, -math.inf, math.inf)
                end = time.time()
                print(f"Time spent searching: {end - start} seconds")
                print(f"Nodes per second: {AI.movesExplored / (end - start)}")
                AI.movesExplored = 0
        Game.displayBoard()
        print(f"Current board evaluation: {AI.evaluateBoard(board) / 100}")

    # show who won
    if board.outcome().termination == chess.Termination.CHECKMATE:
        if board.outcome().winner:
            print("Checkmate.  White wins.")
        else:
            print("Checkmate.  Black wins.")

    else:
        print("Stalemate.  Its a draw.")
