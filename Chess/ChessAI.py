import random
import sys
import ChessEngine
import pandas as pd
from ChessEngine import Move
import copy

sys.setrecursionlimit(10**8)

pieceScore = {'P': 1, 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 0}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

#White openings
Queens_gambit_white = ['d2d4', 'c2c4', 'b1c3']
Four_knights_white = ['e2e4', 'g1f3', 'b1c3']

#Black openings
Queens_gambit_black = ['e7e6', 'd7d5', 'g8f6']
Sicilian_black = ['c7c5', 'e7e6', 'b8c6', 'g8f6']
Four_knights_black = ['e7e5', 'b8c6', 'g8f6']

whiteOpeningsName = [
	'Queens_gambit_white',
	'Four_knights_white'
]
blackOpeningsName = [
	'Sicilian_black',
	'Four_knights_black',
	'Queens_gambit_black'
]
whiteOpenings = [
	Queens_gambit_white,
	Four_knights_white
]
blackOpenings = [
	Sicilian_black,
	Four_knights_black,
	Queens_gambit_black
]
chosenOpenings = []

ranksToRows = {'1':7,'2':6,'3':5,'4':4,
			'5':3,'6':2,'7':1,'8':0}
rowsToRanks = {v:k for k,v in ranksToRows.items()}
filesToCols = {'a':0,'b':1,'c':2,'d':3,
			'e':4,'f':5,'g':6,'h':7}
colsToFiles = {v: k for k,v in filesToCols.items()}

def generateOpening(engine, opening):
	#exec(f"global {opening}; opening = {opening}")
	for move_ind in range(len(opening)):
		opening[move_ind] = moveFromNotation(engine, opening[move_ind])
	return opening

def moveFromNotation(engine, notation):
	start = notation[:2]
	end = notation[2:]
	start_col = filesToCols[start[0]]
	start_row = ranksToRows[start[-1]]
	end_col = filesToCols[end[0]]
	end_row = ranksToRows[end[-1]]
	return Move((start_row, start_col), (end_row, end_col), engine.board)

def randomMove(validMoves):
	return validMoves[random.randint(0, len(validMoves)-1)]

def minMaxNoRecursionMove(engine, validMoves):
	turnMultiplier = 1 if engine.whiteToMove == True else -1
	oppMinMaxScore = CHECKMATE
	bestMove = None
	random.shuffle(validMoves)
	for playerMove in validMoves:
		engine.makeMove(playerMove)
		if engine.checkmate == True:
			oppMaxScore = -CHECKMATE
		elif engine.stalemate == True:
			oppMaxScore = STALEMATE
		else:
			oppMaxScore = -CHECKMATE
			for oppMove in engine.getValidMoves():
				engine.makeMove(oppMove)
				engine.getValidMoves()
				if engine.checkmate == True:
					score = CHECKMATE
				elif engine.stalemate == True:
					score = STALEMATE
				else:
					score = scoreMaterial(engine) * -turnMultiplier
					if score > oppMaxScore:
						oppMaxScore = score
				engine.undoMove()
		if oppMaxScore < oppMinMaxScore:
			oppMinMaxScore = oppMaxScore
			bestMove = playerMove
		engine.undoMove()
	return bestMove

def bestMove(engine, validMoves, AI):
	global nextMove, counter, pieceScore, openings, openingsName, engine_copy, turn
	turn = (1 if engine.whiteToMove == True else -1)
	engine_copy = engine
	pieceScoreKeys = list(pieceScore.keys())
	for i in range(6):
		pieceScore[pieceScoreKeys[i]] = float(AI.iat[i, 1])
	nextMove = []
	counter = 0

	if type(whiteOpenings[0][0]) == str:
		openings = whiteOpenings + blackOpenings
		openingsName = whiteOpeningsName + blackOpeningsName
		for i in range(len(openingsName)):
			exec(f"global {openingsName[i]}, engine_copy, openingsName; {openingsName[i]} = generateOpening(engine_copy, {openingsName[i]})")

	if engine.whiteToMove == True:
		if len(engine.moveLog) == 0:
			validMoves = [m[i] for m in whiteOpenings for i in range(len(m))]
	else:
		if len(engine.moveLog) == 1:
			validMoves = [m[i] for m in blackOpenings for i in range(len(m))]

	#minMaxNoRecursionMove(engine, validMoves)
	#minMaxMove(engine, validMoves, whiteToMove, DEPTH)
	#negaMaxMove(engine, validMoves, (1 if engine.whiteToMove == True else -1), DEPTH)
	negaMaxAlphaBetaMove(copy.copy(engine), validMoves, -CHECKMATE, CHECKMATE, turn, AI, DEPTH)
	return nextMove

def minMaxMove(engine, validMoves, whiteToMove, depth):
	global nextMove, counter
	counter += 1
	if depth == 0:
		return scoreBoard(engine)
	random.shuffle(validMoves)
	if whiteToMove == True:
		maxScore = -CHECKMATE
		for move in validMoves:
			engine.makeMove(move)
			nextMoves = engine.getValidMoves()
			score = minMaxMove(engine, nextMoves, False, depth-1)
			if score > maxScore:
				maxScore = score
				if depth == DEPTH:
					nextMove = move
			engine.undoMove()
		return maxScore
	else:
		minScore = CHECKMATE
		for move in validMoves:
			engine.makeMove(move)
			nextMoves = engine.getValidMoves()
			score = minMaxMove(engine, nextMoves, True, depth-1)
			if score < minScore:
				minScore = score
				if depth == DEPTH:
					nextMove = move
			engine.undoMove()
		return minScore

def negaMaxMove(engine, validMoves, turnMultiplier, depth):
	global nextMove, counter
	counter += 1
	if depth == 0:
		return turnMultiplier * scoreBoard(engine)
	random.shuffle(validMoves)
	maxScore = -CHECKMATE
	for move in validMoves:
		engine.makeMove(move)
		nextMoves = engine.getValidMoves()
		score = -negaMaxMove(engine, nextMoves, -turnMultiplier, depth-1)
		if score > maxScore:
			maxScore = score
			if depth == DEPTH:
				nextMove = move
		engine.undo()
	return maxScore

def negaMaxAlphaBetaMove(engine, validMoves, alpha, beta, turnMultiplier, AI, depth):
	global nextMove, counter, pieceScore, turn
	counter += 1
	if depth == 0:
		bookMoveScore = 0
		for opening in chosenOpenings:
			for o in opening:
				for nM in nextMove:
					if nM == o:
						bookMoveScore = 0.9
		return turnMultiplier * (scoreBoard(engine, turnMultiplier, validMoves, AI) + (bookMoveScore if turnMultiplier == 1 else -bookMoveScore))
		#return turnMultiplier * scoreMaterial(engine)
	for m in engine.getCastleMoves(engine.whiteKingLocation[0] if engine.whiteToMove == True else engine.blackKingLocation[0], engine.whiteKingLocation[1] if engine.whiteToMove == True else engine.blackKingLocation[1], [], ('w' if engine.whiteToMove else 'b')):
		if (turn == 1 and m.pieceMoved == 'wK') or (turn == -1 and m.pieceMoved == 'bK'):
			validMoves.append(m)
		
	random.shuffle(validMoves)

	#Remove nonsense and really bad moves
	for m in range(len(validMoves)-1, -1, -1):
		move = validMoves[m]
		if move.pieceMoved[1] == 'Q' and len(engine.moveLog) < 10*2:
			validMoves.remove(move)
		if move.pieceMoved[1] == 'K' and move.castleMove == False:
			tmp_validMoves = validMoves.copy()
			for i in range(len(validMoves)-1, -1, -1):
				if tmp_validMoves[i].pieceMoved[1] == 'K':
					tmp_validMoves.remove(tmp_validMoves[i])
			if tmp_validMoves != []:
				validMoves.remove(move)

	maxScore = -CHECKMATE
	for move in validMoves:
		engine.makeMove(move)
		if engine.squareUnderAttack(engine.whiteKingLocation[0] if engine.whiteToMove == False else engine.blackKingLocation[0], engine.whiteKingLocation[1] if engine.whiteToMove == False else engine.blackKingLocation[1]) == False:
			nextMoves = engine.getValidMoves()
			score = -negaMaxAlphaBetaMove(engine, nextMoves, -beta, -alpha, -turnMultiplier, AI, depth-1)
			if score > maxScore:
				maxScore = score
				if depth == DEPTH:
					nextMove.append(move)
			if move.castleMove == True:
				nextMove.append(move)
		engine.undoMove()
		if maxScore > alpha:
			alpha = maxScore
		if alpha >= beta:
			break
	return maxScore
	
def scoreBoard(engine, turnMultiplier, validMoves, AI):
	engine.getValidMoves()
	if engine.checkmate == True:
		if engine.whiteToMove == True:
			return -CHECKMATE
		else:
			return CHECKMATE
	elif engine.stalemate:
		return STALEMATE

	score = 0
	for row in range(len(engine.board)):
		for col in range(len(engine.board[row])):
			square = engine.board[row][col]
			if square != '--':
				if square[0] == 'w':
					score += pieceScore[square[1]]
					score += engine.getProtections(row, col, validMoves, AI)
					score += engine.getAttacks(row, col, validMoves, AI)
					score += engine.getValidMoveForSquare(row, col, validMoves, AI)
					score += engine.castle(validMoves, AI)
					score += float(AI.iat[5,1]) if engine.squareUnderAttack(engine.blackKingLocation[0], engine.blackKingLocation[1]) == True else 0
				elif square[0] == 'b':
					score -= pieceScore[square[1]]
					score -= engine.getProtections(row, col, validMoves, AI)
					score -= engine.getAttacks(row, col, validMoves, AI)
					score -= engine.getValidMoveForSquare(row, col, validMoves, AI)
					score -= engine.castle(validMoves, AI)
					score -= float(AI.iat[5,1]) if engine.squareUnderAttack(engine.blackKingLocation[0], engine.blackKingLocation[1]) == True else 0
	score += engine.getPositionAdvantages('w', AI)
	score -= engine.getPositionAdvantages('b', AI)
	return score

def scoreMaterial(engine):
	score = 0
	for row in engine.board:
		for square in row:
			if square[0] == 'w':
				score += pieceScore[square[1]]
			elif square[0] == 'b':
				score -= pieceScore[square[1]]
	return score

def getNextMove(nextMove, engine):
	global counter, openings, chosenOpenings, turn
	string = ""
	scores = []
	castleMoves = []
	for i in nextMove:
		if i.castleMove == True and ((i.pieceMoved == 'wK' and turn == 1) or (i.pieceMoved == 'bK' and turn == -1)):
			castleMoves.append(i)
	if castleMoves != []:
		random.shuffle(castleMoves)
		nextMove = castleMoves
	if len(engine.moveLog) < 2:
		random.shuffle(nextMove)
	for m in nextMove[:-1]:
		string += m.getChessNotation() + (", " if m != nextMove[-2] else "")
	chosenMove = nextMove[-1]
	chosenOpenings = []
	for i in openings:
		for j in i:
			if chosenMove == j:
				chosenOpenings.append(i)
	return chosenMove, string, counter, chosenMove.getChessNotation()