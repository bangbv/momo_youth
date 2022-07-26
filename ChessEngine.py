import numpy as np
import sys
import pandas as pd

sys.setrecursionlimit(10**8)

class GameState():
	def __init__(self):
		self.board = np.array([
			['bR','bN','bB','bQ','bK','bB','bN','bR'],
			['bP','bP','bP','bP','bP','bP','bP','bP'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['--','--','--','--','--','--','--','--'],
			['wP','wP','wP','wP','wP','wP','wP','wP'],
			['wR','wN','wB','wQ','wK','wB','wN','wR']
		])
		self.draw = [
			['wK', 'bK'], 

			['wK', 'bK', 'bN', 'bN'], 
			['wK', 'bK', 'wN', 'wN'], 
			['wK', 'bK', 'bN', 'wN'], 
			['wK', 'bK', 'wN', 'bN'], 

			['wK', 'bK', 'bN', 'wB'], 
			['wK', 'bK', 'wN', 'bB'], 
			['wK', 'bK', 'wN', 'wB'], 
			['wK', 'bK', 'bN', 'bB'], 

			['wK', 'bK', 'bN'], 
			['wK', 'bK', 'wN'], 

			['wK', 'bK', 'wB'],
			['wK', 'bK', 'bB']
		]
		self.whiteToMove = True
		self.moveLog = []
		self.undoneMoves = []
		self.whiteKingLocation = (7, 4)
		self.blackKingLocation = (0, 4)
		self.checkmate = False
		self.stalemate = False
		self.notEnoughMaterialsToWin = False
		self.winner = ""
		self.inCheck = False
		self.checks = []
		self.pins = []
		self.enpassantPossible = ()
		self.enpassantPossibleLog = [self.enpassantPossible]
		self.currentCastelingRight = CastleRights(True, True, True, True)
		self.castleRightLog = [CastleRights(self.currentCastelingRight.wks, self.currentCastelingRight.bks, 
									self.currentCastelingRight.wqs, self.currentCastelingRight.bqs)]

	def makeMove(self, move, promotionTo = 'Q'):
		self.board[move.startRow][move.startCol] = '--'
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.moveLog.append(move)
		self.whiteToMove = not self.whiteToMove

		if move.pieceMoved == 'wK':
			self.whiteKingLocation = (move.endRow, move.endCol)
		if move.pieceMoved == 'bK':
			self.blackKingLocation = (move.endRow, move.endCol)

		if move.pawnPromotion == True:
			self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotionTo

		if move.enpassantMove == True:
			self.board[move.startRow][move.endCol] = '--'
			
		if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
			self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
		else:
			self.enpassantPossible = ()

		if move.castleMove == True:
			if move.endCol - move.startCol == 2:
				self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
				self.board[move.endRow][move.endCol+1] = '--'
			else:
				self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
				self.board[move.endRow][move.endCol-2] = '--'

		self.updateCastleRights(move)
		self.castleRightLog.append(CastleRights(self.currentCastelingRight.wks, self.currentCastelingRight.bks, 
									self.currentCastelingRight.wqs, self.currentCastelingRight.bqs))

		self.enpassantPossibleLog.append(self.enpassantPossible)

	def undoMove(self):
		if len(self.moveLog) != 0:
			move = self.moveLog.pop()
			self.undoneMoves.append(move)
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.whiteToMove = not self.whiteToMove

			if move.pieceMoved == 'wK':
				self.whiteKingLocation = (move.startRow, move.startCol)
			if move.pieceMoved == 'bK':
				self.blackKingLocation = (move.startRow, move.startCol)

			if move.enpassantMove == True:
				self.board[move.endRow][move.endCol] = '--'
				self.board[move.startRow][move.endCol] = move.pieceCaptured
				
			self.enpassantPossibleLog.pop()
			self.enpassantPossible = self.enpassantPossibleLog[-1]

			self.castleRightLog.pop()
			self.currentCastelingRight = self.castleRightLog[-1]

			if move.castleMove == True:
				if move.endCol - move.startCol == 2:
					self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
					self.board[move.endRow][move.endCol-1] = '--'
				else:
					self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
					self.board[move.endRow][move.endCol+1] = '--'

			self.checkmate = False
			self.stalemate = False

	def updateCastleRights(self, move):
		if move.pieceMoved == 'wK':
			self.currentCastelingRight.wks = False
			self.currentCastelingRight.wqs = False
		elif move.pieceMoved == 'bK':
			self.currentCastelingRight.bks = False
			self.currentCastelingRight.bqs = False
		elif move.pieceMoved == 'wR':
			if move.startCol == 0:
				self.currentCastelingRight.wqs = False
			elif move.startCol == 7:
				self.currentCastelingRight.wks = False
		elif move.pieceMoved == 'bR':
			if move.startCol == 0:
				self.currentCastelingRight.bqs = False
			elif move.startCol == 7:
				self.currentCastelingRight.bks = False

		if move.pieceCaptured == 'bR':
			if move.endRow == 0:
				if move.endCol == 0:
					self.currentCastelingRight.bqs = False
				elif move.endCol == 7:
					self.currentCastelingRight.bks = False
		elif move.pieceCaptured == 'wR':
			if move.endRow == 7:
				if move.endCol == 0:
					self.currentCastelingRight.wqs = False
				elif move.endCol == 7:
					self.currentCastelingRight.wks = False

	def redoMove(self, promotionTo=None):
		if len(self.undoneMoves) != 0:
			move = self.undoneMoves.pop()
			self.makeMove(move, promotionTo)

	def getValidMoves(self):
		tempEnpassantPossible = self.enpassantPossible

		moves = []
		self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
		if self.whiteToMove:
			kingRow = self.whiteKingLocation[0]
			kingCol = self.whiteKingLocation[1]
		else:
			kingRow = self.blackKingLocation[0]
			kingCol = self.blackKingLocation[1]
		if self.inCheck == True:
			if len(self.checks) == 1:
				moves = self.getPossibleMoves()
				check = self.checks[0]
				checkRow = check[0]
				checkCol = check[1]
				pieceChecking = self.board[checkRow][checkCol]
				validSquares = []
				if pieceChecking[1] == 'N':
					validSquares = [(checkRow, checkCol)]
				else:
					for i in range(1, 8):
						validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
						validSquares.append(validSquare)
						if validSquare[0] == checkRow and validSquare[1] == checkCol:
							break
				for i in range(len(moves)-1, -1, -1):
					if moves[i].pieceMoved[1] != 'K':
						if not (moves[i].endRow, moves[i].endCol) in validSquares:
							moves.remove(moves[i])
			else:
				self.getKingMoves(kingRow, kingCol, moves)
		else:
			moves = self.getPossibleMoves()
			
		if moves == [] and self.inCheck == True:
			self.checkmate = True
		elif moves == [] and self.inCheck == False:
			self.stalemate = True

		if self.checkmate == True:
			self.winner = "bK" if self.whiteToMove else "wK"

		self.enpassantPossible = tempEnpassantPossible

		piecesLeft = []
		for row in self.board:
			for square in row:
				if square != '--':
					piecesLeft.append(square)
		for pl in self.draw:
			if pl.sort() == piecesLeft.sort() and len(pl) == len(piecesLeft):
				self.notEnoughMaterialsToWin = True
		
		return moves

	def squareUnderAttack(self, r, c):
		self.whiteToMove = not self.whiteToMove
		oppMoves = self.getPossibleMoves()
		self.whiteToMove = not self.whiteToMove
		for move in oppMoves:
			if move.endRow == r and move.endCol == c:
				return True
		return False

	def checkForPinsAndChecks(self):
		pins = []
		checks = []
		inCheck = False
		if self.whiteToMove == True:
			enemyColor = 'b'
			allyColor = 'w'
			startRow = self.whiteKingLocation[0]
			startCol = self.whiteKingLocation[1]
		else:
			enemyColor = 'w'
			allyColor = 'b'
			startRow = self.blackKingLocation[0]
			startCol = self.blackKingLocation[1]

		directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))
		for j in range(len(directions)):
			d = directions[j]
			possiblePin = ()
			for i in range(1, 8):
				endRow = startRow + d[0] * i
				endCol = startCol + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8:
					endPiece = self.board[endRow][endCol]
					if endPiece[0] == allyColor and endPiece[1] != 'K':
						if possiblePin == ():
							possiblePin = (endRow, endCol, d[0], d[1])
						else:
							break
					elif endPiece[0] == enemyColor:
						type = endPiece[1]
						if (0 <= j <= 3 and type == 'R') or \
								(4 <= j <= 7 and type == 'B') or \
								(i == 1 and type == 'P' and \
								(\
									(enemyColor == 'w' and 6 <= j <= 7) or \
									(enemyColor == 'b' and 4 <= j <= 5)\
								)) or \
								(type == 'Q') or \
								(i == 1 and type == 'K'):
							if possiblePin == ():
								inCheck = True
								checks.append((endRow, endCol, d[0], d[1]))
								break
							else:
								pins.append(possiblePin)
								break
						else:
							break
		knightmoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
		for m in knightmoves:
			endRow = startRow + m[0]
			endCol = startCol + m[1]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				endPiece = self.board[endRow][endCol]
				if endPiece[0] == enemyColor and endPiece[1] == 'N':
					inCheck = True
					checks.append((endRow, endCol, m[0], m[1]))
		return inCheck, pins, checks

	def getPossibleMoves(self):
		moves = []
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				turn = self.board[r][c][0]
				if (turn == 'w' and self.whiteToMove == True) or (turn == 'b' and self.whiteToMove == False):
					piece = self.board[r][c][1]
					if piece == 'P':
						self.getPawnMoves(r, c, moves)
					elif piece == 'R':
						self.getRookMoves(r, c, moves)
					elif piece == 'N':
						self.getKnightMoves(r, c, moves)
					elif piece == 'B':
						self.getBishopMoves(r, c, moves)
					elif piece == 'Q':
						self.getQueenMoves(r, c, moves)
					elif piece == 'K':
						self.getKingMoves(r, c, moves)
						self.getCastleMoves(self.whiteKingLocation[0] if self.whiteToMove == True else self.blackKingLocation[0], self.whiteKingLocation[1] if self.whiteToMove == True else self.blackKingLocation[1], moves, ('w' if self.whiteToMove else 'b'))
		return moves

	def getPawnMoves(self, r, c, moves):
		piecePinned = False
		pinDirection = ()
		for i in range(len(self.pins)-1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piecePinned = True
				pinDirection = (self.pins[i][2], self.pins[i][3])
				self.pins.remove(self.pins[i])
				break
			
		kingRow, kingCol = (self.whiteKingLocation if self.whiteToMove == True else self.blackKingLocation)

		if self.whiteToMove == True:
			if self.board[r-1][c] == '--':
				if piecePinned == False or pinDirection == (-1, 0):
					moves.append(Move((r, c), (r-1, c), self.board))
					if r == 6 and self.board[r-2][c] == '--':
						moves.append(Move((r, c), (r-2, c), self.board))
			if c-1 >= 0:
				if piecePinned == False or pinDirection == (-1, -1):
					if self.board[r-1][c-1][0] == 'b':
						moves.append(Move((r, c), (r-1, c-1), self.board))
					elif (r-1, c-1) == self.enpassantPossible:
						attackPiece = blockPiece = False
						if kingRow == r:
							if kingCol < c:
								insideRange = [*range(kingCol+1, c-1)]
								outsideRange = [*range(c+1, 8)]
							else:
								insideRange = [*range(kingCol-1, c, -1)]
								outsideRange = [*range(c-2, -1, -1)]
							for i in insideRange:
								if self.board[r][i] != '--':
									blockPiece = True
							for i in outsideRange:
								square = self.board[r][i]
								if (square[0] == 'b' if self.whiteToMove == True else 'w') and (square[1] == 'R' or square[1] == 'Q'):
									attackPiece = False
								if square[0] != '--':
									blockPiece = True
						if blockPiece == True or attackPiece == False:
							moves.append(Move((r, c), (r-1, c-1), self.board, enpassant=True))
			if c+1 <= 7:
				if piecePinned == False or pinDirection == (-1, 1):
					if self.board[r-1][c+1][0] == 'b':
						moves.append(Move((r, c), (r-1, c+1), self.board))
					elif (r-1, c+1) == self.enpassantPossible:
						attackPiece = blockPiece = False
						if kingRow == r:
							if kingCol < c:
								insideRange = [*range(kingCol+1, c)]
								outsideRange = [*range(c+2, 8)]
							else:
								insideRange = [*range(kingCol-1, c, -1)]
								outsideRange = [*range(c-2, -1, -1)]
							for i in insideRange:
								if self.board[r][i] != '--':
									blockPiece = True
							for i in outsideRange:
								square = self.board[r][i]
								if (square[0] == 'b' if self.whiteToMove == True else 'w') and (square[1] == 'R' or square[1] == 'Q'):
									attackPiece = False
								if square[0] != '--':
									blockPiece = True
						if blockPiece == True or attackPiece == False:
							moves.append(Move((r, c), (r-1, c+1), self.board, enpassant=True))
		else:
			if self.board[r+1][c] == '--':
				if piecePinned == False or pinDirection == (1, 0):
					moves.append(Move((r, c), (r+1, c), self.board))
					if r == 1 and self.board[r+2][c] == '--':
						moves.append(Move((r, c), (r+2, c), self.board))
			if c-1 >= 0:
				if piecePinned == False or pinDirection == (1, -1):
					if self.board[r+1][c-1][0] == 'w':
						moves.append(Move((r, c), (r+1, c-1), self.board))
					elif (r+1, c-1) == self.enpassantPossible:
						attackPiece = blockPiece = False
						if kingRow == r:
							if kingCol < c:
								insideRange = [*range(kingCol+1, c-1)]
								outsideRange = [*range(c+1, 8)]
							else:
								insideRange = [*range(kingCol-1, c, -1)]
								outsideRange = [*range(c-2, -1, -1)]
							for i in insideRange:
								if self.board[r][i] != '--':
									blockPiece = True
							for i in outsideRange:
								square = self.board[r][i]
								if (square[0] == 'b' if self.whiteToMove == True else 'w') and (square[1] == 'R' or square[1] == 'Q'):
									attackPiece = False
								if square[0] != '--':
									blockPiece = True
						if blockPiece == True or attackPiece == False:
							moves.append(Move((r, c), (r+1, c-1), self.board, enpassant=True))
			if c+1 <= 7:
				if piecePinned == False or pinDirection == (1, 1):
					if self.board[r+1][c+1][0] == 'w':
						moves.append(Move((r, c), (r+1, c+1), self.board))
					elif (r+1, c+1) == self.enpassantPossible:
						attackPiece = blockPiece = False
						if kingRow == r:
							if kingCol < c:
								insideRange = [*range(kingCol+1, c)]
								outsideRange = [*range(c+2, 8)]
							else:
								insideRange = [*range(kingCol-1, c, -1)]
								outsideRange = [*range(c-2, -1, -1)]
							for i in insideRange:
								if self.board[r][i] != '--':
									blockPiece = True
							for i in outsideRange:
								square = self.board[r][i]
								if (square[0] == 'b' if self.whiteToMove == True else 'w') and (square[1] == 'R' or square[1] == 'Q'):
									attackPiece = False
								if square[0] != '--':
									blockPiece = True
						if blockPiece == True or attackPiece == False:
							moves.append(Move((r, c), (r+1, c+1), self.board, enpassant=True))
	
	def getRookMoves(self, r, c, moves):
		piecePinned = False
		pinDirection = ()
		for i in range(len(self.pins)-1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piecePinned = True
				pinDirection = (self.pins[i][2], self.pins[i][3])
				if self.board[r][c][1] != 'Q':
					self.pins.remove(self.pins[i])
				break
			
		directions = ((-1,0),(0,-1),(1,0),(0,1))
		enemycolor = 'b' if self.whiteToMove else 'w'
		for d in directions:
			for i in range(1,8):
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8:
					if piecePinned == False or pinDirection == d or pinDirection == (-d[0], -d[1]):
						endPiece = self.board[endRow][endCol]
						if endPiece == '--':
							moves.append(Move((r, c), (endRow, endCol), self.board))
						elif endPiece[0] == enemycolor:
							moves.append(Move((r, c), (endRow, endCol), self.board))
							break
						else:
							break
				else:
					break
			
	def getKnightMoves(self, r, c, moves):
		piecePinned = False
		for i in range(len(self.pins)-1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piecePinned = True
				self.pins.remove(self.pins[i])
				break
			
		knightmoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
		allycolor = 'w' if self.whiteToMove else 'b'
		for m in knightmoves:
			endRow = r + m[0]
			endCol = c + m[1]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				if piecePinned == False:
					endPiece = self.board[endRow][endCol]
					if endPiece[0] != allycolor:
						moves.append(Move((r, c), (endRow, endCol), self.board))

	def getBishopMoves(self, r, c, moves):
		piecePinned = False
		pinDirection = ()
		for i in range(len(self.pins)-1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piecePinned = True
				pinDirection = (self.pins[i][2], self.pins[i][3])
				self.pins.remove(self.pins[i])
				break
			
		directions = ((-1,-1),(1,1),(1,-1),(-1,1))
		enemycolor = 'b' if self.whiteToMove else 'w'
		for d in directions:
			for i in range(1,8):
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8:
					if piecePinned == False or pinDirection == d or pinDirection == (-d[0], -d[1]):
						endPiece = self.board[endRow][endCol]
						if endPiece == '--':
							moves.append(Move((r, c), (endRow, endCol), self.board))
						elif endPiece[0] == enemycolor:
							moves.append(Move((r, c), (endRow, endCol), self.board))
							break
						else:
							break
				else:
					break

	def getQueenMoves(self, r, c, moves):
		piecePinned = False
		pinDirection = ()
		for i in range(len(self.pins)-1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piecePinned = True
				pinDirection = (self.pins[i][2], self.pins[i][3])
				self.pins.remove(self.pins[i])
				break
			
		self.getRookMoves(r, c, moves)
		self.getBishopMoves(r, c, moves)
	
	def getKingMoves(self, r, c, moves):
		rowmoves = (-1, -1, -1, 0, 0, 1, 1, 1)
		colmoves = (-1, 0, 1, -1, 1, -1, 0, 1)
		allyColor = 'w' if self.whiteToMove else 'b'
		for i in range(8):
			endRow = r + rowmoves[i]
			endCol = c + colmoves[i]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				endPiece = self.board[endRow][endCol]
				if endPiece[0] != allyColor:
					if allyColor == 'w':
						self.whiteKingLocation = (endRow, endCol)
					else:
						self.blackKingLocation = (endRow, endCol)
					inCheck, pins, checks = self.checkForPinsAndChecks()
					if inCheck == False:
						moves.append(Move((r, c), (endRow, endCol), self.board))
					if allyColor == 'w':
						self.whiteKingLocation = (r, c)
					else:
						self.blackKingLocation = (r, c)

	def getCastleMoves(self, r, c, moves, allyColor):
		if self.inCheck == True:
			return []
		if (self.whiteToMove == True and self.currentCastelingRight.wks == True) or (self.whiteToMove == False and self.currentCastelingRight.bks == True):
			self.getKingsideCastleMoves(r, c, moves, allyColor)
		if (self.whiteToMove == True and self.currentCastelingRight.wqs == True) or (self.whiteToMove == False and self.currentCastelingRight.bqs == True):
			self.getQueensideCastleMoves(r, c, moves, allyColor)
		return moves
		
	def getKingsideCastleMoves(self, r, c, moves, allyColor):
		if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
			if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
				moves.append(Move((r, c), (r, c+2), self.board, castle=True))

	def getQueensideCastleMoves(self, r, c, moves, allyColor):
		if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
			if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2) and not self.squareUnderAttack(r, c-3):
				moves.append(Move((r, c), (r, c-2), self.board, castle=True))
		
	def getProtections(self, row, col, validMoves, AI):
		protections = 0
		for m in validMoves:
			if m.endCol == col and m.endRow == row:
				protections += float(AI.iat[6,1])
		return protections
	
	def getValidMoveForSquare(self, row, col, validMoves, AI):
		validMovesForSquare = 0
		for m in validMoves:
			if m.startCol == col and m.startRow == row:
				validMovesForSquare += float(AI.iat[7,1])
		return validMovesForSquare

	def getAttacks(self, row, col, validMoves, AI):
		attacks = 0
		for m in validMoves:
			if m.startCol == col and m.startRow == row and m.pieceCaptured == 'w' if self.board[row][col][0] == 'b' else 'b':
				attacks += float(AI.iat[8,1])
		return attacks
	
	def castle(self, validMoves, AI):
		for m in validMoves:
			if m.castleMove == True:
				return float(AI.iat[9,1])
		return 0

	def getPositionAdvantages(self, turn, AI):
		position = 0
		if turn == 'w':
			if self.board[7][3] != 'wQ' and len(self.moveLog) < 10*2:
				position -= float(AI.iat[10,1])
			if self.board[7][4] != 'wK' and len(self.moveLog) < 20*2:
				position -= float(AI.iat[11,1])
			''' if self.board[7][4] != 'wK' and len(self.moveLog) < 4:
				position += 20 ''' #Bongcloud
			if self.board[4][3] == 'wP' or self.board[4][3] == 'wN' or \
				self.board[4][4] == 'wP' or self.board[4][4] == 'wN' or \
				self.board[3][3] == 'wP' or self.board[3][3] == 'wN' or \
				self.board[3][4] == 'wP' or self.board[3][4] == 'wN':
				position += float(AI.iat[12,1])
			if (self.board[7][1] == 'wN' or self.board[7][2] == 'wB' or \
				self.board[7][5] == 'wB' or self.board[7][6] == 'wN') and len(self.moveLog) > 6*2:
				position -= float(AI.iat[13,1])
			if self.board[4][2] == 'wB' or self.board[3][1] == 'wB' or \
				self.board[4][5] == 'wB' or self.board[3][6] == 'wB':
				position += float(AI.iat[14,1])
			if self.board[5][2] == 'wN' or self.board[5][5] == 'wN':
				position += float(AI.iat[15,1])
			if self.board[5][0] == 'wN' or self.board[5][7] == 'wN':
				position -= float(AI.iat[16,1])
		else:
			if self.board[0][3] != 'bQ' and len(self.moveLog) < 10*2:
				position -= float(AI.iat[10,1])
			if self.board[0][4] != 'bK' and len(self.moveLog) < 20*2:
				position -= float(AI.iat[11,1])
			''' if self.board[0][4] != 'bK' and len(self.moveLog) < 4:
				position += 20 ''' #Bongcloud
			if self.board[4][3] == 'bP' or self.board[4][3] == 'bN' or \
				self.board[4][4] == 'bP' or self.board[4][4] == 'bN' or \
				self.board[3][3] == 'bP' or self.board[3][3] == 'bN' or \
				self.board[3][4] == 'bP' or self.board[3][4] == 'bN':
				position += float(AI.iat[12,1])
			if (self.board[0][1] == 'bN' or self.board[0][2] == 'bB' or \
				self.board[0][5] == 'bB' or self.board[0][6] == 'bN') and len(self.moveLog) > 6*2:
				position -= float(AI.iat[13,1])
			if self.board[3][2] == 'bB' or self.board[4][1] == 'bB' or \
				self.board[3][5] == 'bB' or self.board[4][6] == 'bB':
				position += float(AI.iat[14,1])
			if self.board[2][2] == 'bN' or self.board[2][5] == 'bN':
				position += float(AI.iat[15,1])
			if self.board[2][0] == 'bN' or self.board[2][7] == 'bN':
				position -= float(AI.iat[16,1])
		return position

class Move():
	ranksToRows = {'1':7,'2':6,'3':5,'4':4,
				'5':3,'6':2,'7':1,'8':0}
	rowsToRanks = {v:k for k,v in ranksToRows.items()}
	filesToCols = {'a':0,'b':1,'c':2,'d':3,
				'e':4,'f':5,'g':6,'h':7}
	colsToFiles = {v: k for k,v in filesToCols.items()}

	def __init__(self, start, end, board, enpassant=False, castle=False):
		self.startRow = start[0]
		self.startCol = start[1]
		self.endRow = end[0]
		self.endCol = end[1]
		self.pieceMoved = board[self.startRow][self.startCol]
		self.pieceCaptured = board[self.endRow][self.endCol]
		self.pawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
		self.enpassantMove = enpassant
		if self.enpassantMove == True:
			self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'
		self.castleMove = castle
		self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

	def __eq__(self, other):
		if isinstance(other, Move):
			return self.moveID == other.moveID

	def getChessNotation(self):
		if not (abs(self.startCol - self.endCol) == 2 and self.pieceMoved[1] == 'K'):
			if self.pieceCaptured == '--':
				if self.pieceMoved[-1] != 'P':
					return self.pieceMoved[-1] + self.getRankFile(self.endRow, self.endCol)
				else:
					return self.getRankFile(self.endRow, self.endCol)
			else:
				if self.pieceMoved[-1] != 'P':
					return self.pieceMoved[-1] + "x" + self.getRankFile(self.endRow, self.endCol)
				else:
					return self.colsToFiles[self.startCol] + 'x' + self.getRankFile(self.endRow, self.endCol)
		else:
			if self.endCol - self.startCol == 2:
				return "O-O"
			else:
				return "O-O-O"
				

	def getRankFile(self, row, col):
		return self.colsToFiles[col] + self.rowsToRanks[row]

class CastleRights():
	def __init__(self, wks, bks, wqs, bqs):
		self.wks = wks
		self.bks = bks
		self.wqs = wqs
		self.bqs = bqs