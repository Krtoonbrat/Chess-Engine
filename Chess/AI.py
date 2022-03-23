import copy
import math
import random

import chess
import chess.polyglot
from Node import *
from sortedcontainers import SortedKeyList


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

    # killer moves
    killer = {}

    # number of cut nodes and alpha/beta specific cuts
    cutNodes = 0
    alphaCuts = 0
    betaCuts = 0

    # base values for all the pieces
    # white gets a positive value, black a negative
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

        # give the AI a slap for moving the queen too early
        if board.fullmove_number < 8 and board.piece_type_at(chess.D1) is not chess.QUEEN:
            score -= 15
        if board.fullmove_number < 8 and board.piece_type_at(chess.D8) is not chess.QUEEN:
            score += 15

        # space advantages
        # the basic idea is to reward each side for being able to move to central squares safely
        files = chess.SquareSet(chess.BB_FILE_C | chess.BB_FILE_D | chess.BB_FILE_E | chess.BB_FILE_F)

        # white
        whiteSpace = chess.SquareSet((files & chess.BB_RANK_2) | (files & chess.BB_RANK_3) | (files & chess.BB_RANK_4))
        whiteSafeCount = 0
        for square in whiteSpace:
            if not board.is_attacked_by(chess.BLACK, square):
                whiteSafeCount += 1
        score += whiteSafeCount * 5

        # black
        blackSpace = chess.SquareSet((files & chess.BB_RANK_7) | (files & chess.BB_RANK_6) | (files & chess.BB_RANK_5))
        blackSafeCount = 0
        for square in blackSpace:
            if not board.is_attacked_by(chess.WHITE, square):
                blackSafeCount += 1
        score -= blackSafeCount * 5

        return score

    @staticmethod
    def moveOrder(moves, board, PV, depth, node):
        # Most Valuable Victim Least Valuable Attacker function
        def MVVLVA(move):
            if board.is_en_passant(move):
                return -(abs(AI.pieceScores[board.piece_at(board.peek().to_square).symbol()]) - abs(
                    AI.pieceScores[board.piece_at(move.from_square).symbol()]))
            return -(abs(AI.pieceScores[board.piece_at(move.to_square).symbol()]) - abs(
                AI.pieceScores[board.piece_at(move.from_square).symbol()]))

        orderedMoves = []

        if PV[-depth] != 0 and chess.Move.from_uci(PV[-depth]) in moves:
            orderedMoves.append(chess.Move.from_uci(PV[-depth]))
            moves.remove(orderedMoves[0])
        if node.bestMove is not None and node.bestMove not in orderedMoves:
            orderedMoves.append(node.bestMove)
            moves.remove(node.bestMove)

        attackers = SortedKeyList(key=MVVLVA)
        lCaptures = SortedKeyList(key=MVVLVA)
        wCaptures = SortedKeyList(key=MVVLVA)
        eCaptures = SortedKeyList(key=MVVLVA)
        checks = []
        killers = []
        other = []

        # I wrapped this in a try except for when board.pop()
        # throws an error for there being no moves in the stack.
        # This only happens when either the board is loaded from a FEN, or
        # when it is the very first move of the game
        try:
            lastMove = board.pop()
            if board.is_capture(lastMove):
                board.push(lastMove)
                if board.is_attacked_by(board.turn, board.peek().to_square):
                    for retaliation in board.attackers(board.turn, board.peek().to_square):
                        MAD = chess.Move(retaliation, board.peek().to_square)
                        if board.is_legal(MAD) and MAD not in orderedMoves:
                            attackers.add(MAD)
                            moves.remove(MAD)
            else:
                board.push(lastMove)
        except:
            pass

        for move in moves:
            if board.is_capture(move):
                if MVVLVA(move) < -20:
                    wCaptures.add(move)
                elif MVVLVA(move) > 20:
                    lCaptures.add(move)
                else:
                    eCaptures.add(move)
            elif int(str(move.from_square) + str(move.to_square)) in AI.killer[board.ply()]:
                killers.append(move)
            elif board.gives_check(move):
                checks.append(move)
            else:
                other.append(move)

        orderedMoves.extend(attackers)
        orderedMoves.extend(wCaptures)
        orderedMoves.extend(eCaptures)
        orderedMoves.extend(checks)
        orderedMoves.extend(killers)
        orderedMoves.extend(lCaptures)
        orderedMoves.extend(other)

        return orderedMoves

    @staticmethod
    def quiesce(board, alpha, beta, Qdepth):
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
                score = -AI.quiesce(board, -beta, -alpha, Qdepth - 1)
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
    def minimax(depth, isMaximizer, board,  alpha, beta, PV, currentLine, finalDepth, searchDepth):
        if depth <= 0:
            # do a Qsearch if we are at the final depth
            if finalDepth:
                if board.turn:
                    return AI.quiesce(board, alpha, beta, 3), currentLine
                else:
                    return -AI.quiesce(board, alpha, beta, 3), currentLine
            return AI.evaluateBoard(board), currentLine

        # create an index for killer moves if there isn't one already
        if board.ply() not in AI.killer.keys():
            AI.killer[board.ply()] = set()

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
                score, PVreturn = AI.minimax(depth, False, board, alpha, beta, PV, currentLine, finalDepth, searchDepth)
                depth += 1
                if score > maxScore:
                    maxScore = score
                    node.nodeScore = score
                    node.bestMove = move
                    node.PV = copy.copy(PVreturn)
                alpha = max(score, alpha)
                board.pop()
                if maxScore >= beta:
                    AI.killer[board.ply()].add(int(str(move.from_square) + str(move.to_square)))
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
                score, PVreturn = AI.minimax(depth, True, board, alpha, beta, PV, currentLine, finalDepth, searchDepth)
                depth += 1
                if score < minScore:
                    minScore = score
                    node.nodeScore = score
                    node.bestMove = move
                    node.PV = copy.copy(PVreturn)
                beta = min(score, beta)
                board.pop()
                if minScore <= alpha:
                    AI.killer[board.ply()].add(int(str(move.from_square) + str(move.to_square)))
                    AI.cutNodes += 1
                    AI.alphaCuts += 1
                    node.nodeType = 3
                    break
            return minScore, node.PV

    # starts the minimax algorithm and actually keeps track of and makes the best move
    @staticmethod
    def go(depth, board, alpha, beta):

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
            bestScore, PV = AI.minimax(deep, False, board, alpha, beta, PV, currentLine, finalDepth, deep)
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
        del AI.killer[board.ply()]
        # if the AI finds a mate in one, there will only be one killer set to delete
        if board.ply() + 1 in AI.killer.keys():
            del AI.killer[board.ply() + 1]
        board.push(bestMove)
