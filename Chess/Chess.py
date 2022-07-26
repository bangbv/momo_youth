import pygame as pg
import ChessEngine, ChessAI
import time
import sys
import pandas as pd
import threading

sys.setrecursionlimit(10**8)

pg.init()

global GAMEOVER
GAMEOVER = False
WIDTH = HEIGHT = 512
MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT = 250, HEIGHT
DIMENSION = 8
SQUARE_SIZE = HEIGHT / DIMENSION
MAX_FPS = 15
PIECES = {}
PIECES_NAME = ['bR','bN','bB','bQ','bK','bB','bN','bR','bP','wR','wN','wB','wQ','wK','wB','wN','wR','wP']

def loadImages():
	for piece_name in PIECES_NAME:
		PIECES[piece_name] = pg.transform.scale(pg.image.load(f"Pieces/{piece_name}.png"), (SQUARE_SIZE, SQUARE_SIZE))

def main(count):
	global GAMEOVER, playerOne, playerTwo
	playerOne = False
	playerTwo = False
	AITrain1 = AITrain2 = None
	if playerOne == False:
		AITrain1 = pd.read_excel(input("Enter AI 1 file path: "))
		if playerTwo == False:
			AITrain2 = pd.read_excel(input("Enter AI 2 file path: "))
	elif playerTwo == False:
		AITrain1 = pd.read_excel(input("Enter AI 1 file path: "))
	screen = pg.display.set_mode((WIDTH+MOVE_LOG_PANEL_WIDTH, HEIGHT))
	pg.display.set_caption('Chess')
	clock = pg.time.Clock()
	screen.fill(pg.Color("Black"))
	engine = ChessEngine.GameState()
	promotionTo = ""
	validMoves = engine.getValidMoves()
	moveMade = False
	loadImages()
	running = True
	selected = ()
	clicks = []
	for a in range(1, count+1):
		resetGame()
		running = True
		while running:
			pg.event.pump()
			playerTurn = (engine.whiteToMove == True and playerOne == True) or (engine.whiteToMove == False and playerTwo == True)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = False
				elif event.type == pg.MOUSEBUTTONDOWN:
					if GAMEOVER == False and playerTurn:
						location = pg.mouse.get_pos()
						color = 'w' if engine.whiteToMove else 'b'
						col = int(location[0] // SQUARE_SIZE)
						row = int(location[1] // SQUARE_SIZE)
						if col >= 8:
							selected = ()
							clicks = []
						else:
							if len(clicks) == 0:
								if (engine.whiteToMove == True and 'b' in engine.board[row][col]) or (engine.whiteToMove == False and 'w' in engine.board[row][col]) or engine.board[row][col] == '--':
									selected = ()
									clicks = []
								else:
									if selected == (row, col):
										selected = ()
										clicks = []
									else:
										selected = (row, col)
										clicks.append(selected)
							else:
								if selected == (row, col):
									selected = ()
									clicks = [selected]
								else:
									selected = (row, col)
									clicks.append(selected)
									if (engine.board[row][col][0] == color and clicks[0] != selected) or (not ChessEngine.Move(clicks[0], clicks[1], engine.board) in validMoves and clicks[0] != selected):
										clicks = [clicks[-1]]
								if len(clicks) == 2 and color in engine.board[row][col]:
									clicks[0] = selected
									clicks.remove(clicks[-1])
									selected = ()
								if len(clicks) == 2:
									move = ChessEngine.Move(clicks[0], clicks[1], engine.board)
									for i in range(len(validMoves)):
										if move == validMoves[i]:
											previousScore = ChessAI.scoreBoard(engine, (-1 if engine.whiteToMove == True else 1), validMoves, AITrain1 if (playerOne and playerTwo == False) else AITrain1 if engine.whiteToMove == True else AITrain2)
											if validMoves[i].pawnPromotion == True:
												drawPromotionMenu(screen, move.endRow, move.endCol, 'w' if move.endRow == 0 else 'b')
												time.sleep(0.5)
												promoted = False
												r, c = -1, -1
												while promoted == False:
													for evt in pg.event.get():
														if evt.type == pg.MOUSEBUTTONDOWN:
															loc = pg.mouse.get_pos()
															c = int(loc[0] // SQUARE_SIZE)
															r = int(loc[1] // SQUARE_SIZE)
														if r == move.endRow and c == move.endCol:
															promotionTo = 'Q'
															promoted = True
														elif r == move.endRow-1 and move.endRow == 7 and c == move.endCol:
															promotionTo = 'R'
															promoted = True
														elif r == move.endRow-2 and move.endRow == 7 and c == move.endCol:
															promotionTo = 'B'
															promoted = True
														elif r == move.endRow-3 and move.endRow == 7 and c == move.endCol:
															promotionTo = 'N'
															promoted = True
														elif r == move.endRow+1 and move.endRow == 0 and c == move.endCol:
															promotionTo = 'R'
															promoted = True
														elif r == move.endRow+2 and move.endRow == 0 and c == move.endCol:
															promotionTo = 'B'
															promoted = True
														elif r == move.endRow+3 and move.endRow == 0 and c == move.endCol:
															promotionTo = 'N'
															promoted = True
												engine.makeMove(validMoves[i], promotionTo)
											else:
												engine.makeMove(validMoves[i])					
											score = ChessAI.scoreBoard(engine, (-1 if engine.whiteToMove == True else 1), validMoves, AITrain1 if (playerOne and playerTwo == False) else AITrain1 if engine.whiteToMove == True else AITrain2)
											print(f"{engine.moveLog[-1].getChessNotation()}: {score}")
											moveMade = True
											animate = True
											selected = ()
											clicks = []
									if moveMade == False:
										selected = ()
										clicks.remove(clicks[-1])
				elif event.type == pg.KEYDOWN:
					keys=pg.key.get_pressed()
					if keys[pg.K_LEFT]:
						engine.undoMove()
						moveMade = True
						animate = False
					if keys[pg.K_RIGHT]:
						if promotionTo != "":
							engine.redoMove(promotionTo)
						else:
							engine.redoMove()
						moveMade = True
					if keys[pg.K_SPACE]:
						resetGame()

			if GAMEOVER == False and playerTurn == False and validMoves != []:
				global AIMove
				AIMove = []
				getMove = threading.Thread(target=getAIMove, name="AIMove", args=(engine, validMoves, AITrain1, AITrain2))
				getMove.start()
				while getMove.is_alive() == True:
					pg.event.pump()
					for event in pg.event.get():
						if event.type == pg.QUIT:
							running = False
							exit()
				if AIMove == []:
					AIMove = ChessAI.randomMove(validMoves)
				else:
					AIMove, string, counter, chosenMove = ChessAI.getNextMove(AIMove, engine)
				engine.makeMove(AIMove)
				engine.getValidMoves()
				score = ChessAI.scoreBoard(engine, (-1 if engine.whiteToMove == True else 1), validMoves, AITrain1 if (playerOne and playerTwo == False) else AITrain1 if engine.whiteToMove == True else AITrain2)
				print(f"\n{engine.moveLog[-1].getChessNotation()}: {score}")
				print(f"Other available moves for {chosenMove}: {string}")
				print(f"Moves generated: {counter}\n")
				moveMade = True
				animate = True
						
			if moveMade == True:
				if animate == True:
					animateMove(screen, engine.moveLog[-1], engine, clock)
				validMoves = engine.getValidMoves()
				moveMade = False
				animate = False

			updateGameState(screen, engine, validMoves, selected)
			clock.tick(MAX_FPS)
			pg.display.flip()
			if engine.checkmate == True:
				GAMEOVER = True
				engine.whiteToMove = not engine.whiteToMove
				screen.fill(pg.Color("grey"))
				screen.blit(PIECES[engine.winner], (WIDTH/2-30, HEIGHT/2-70))
				if engine.winner == "wK":
					text = 'White won!'
					#print(f"[{count}] White won!")
				else:
					text = 'Black won!'
					#print(f"[{count}] Black won!")
				pg.display.update()
				drawText(screen, text, "Black", (WIDTH / 2, HEIGHT / 2 + 50))
				time.sleep(5)
				running = False
			elif engine.stalemate == True:
				GAMEOVER = True
				engine.whiteToMove = not engine.whiteToMove
				screen.fill(pg.Color("Grey"))
				drawText(screen, "Draw - Stalemate")
				#print(f"[{count}] Draw - stalemate")
				time.sleep(5)
				running = False
			elif engine.notEnoughMaterialsToWin == True:
				GAMEOVER = True
				engine.whiteToMove = not engine.whiteToMove
				screen.fill(pg.Color("Grey"))
				drawText(screen, "Draw - Not enough materials to win")
				#print(f"[{count}] Draw - Not enough materials to win")
				time.sleep(5)
				running = False
		with open("MoveLog.txt", "a") as f:
			if engine.checkmate == True:
				if engine.winner == "wK":
					f.write(f"[{count}] White won!\n")
				elif engine.winner == "bK":
					f.write(f"[{count}] Black won!\n")
			elif engine.stalemate == True:
				f.write(f"[{count}] Draw - stalemate\n")
			for m in engine.moveLog:
				f.write(f"{m.getChessNotation()}\n")
			f.close()

def getAIMove(engine, validMoves, AITrain1, AITrain2):
	global AIMove
	AIMove = ChessAI.bestMove(engine, validMoves, AITrain1 if (playerOne and playerTwo == False) else AITrain1 if engine.whiteToMove == True else AITrain2)

def drawText(screen, text, textColor="Black", position=(WIDTH/2, HEIGHT/2), fontsize=32):
	font = pg.font.SysFont('TimesNewRoman', fontsize)
	text = font.render(text, True, pg.Color(textColor))
	textRect = text.get_rect()
	textRect.center = position
	screen.blit(text, textRect)
	pg.display.update()

def highlightSquares(screen, engine, validMoves, selected):
	if selected != ():
		r, c = selected
		if engine.board[r][c][0] == ('w' if engine.whiteToMove else 'b'):
			s = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
			s.set_alpha(131)
			s.fill(pg.Color("yellow"))
			screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
			for move in validMoves:
				if move.startRow == r and move.startCol == c:
					if move.pieceCaptured == '--':
						s.set_alpha(100)
						s.fill(pg.Color("yellow"))
						screen.blit(s, (move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE))
					else:
						s.set_alpha(100)
						s.fill(pg.Color("red"))
						screen.blit(s, (move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE))

def resetGame():
	engine = ChessEngine.GameState()
	validMoves = engine.getValidMoves()
	selected = ()
	clicks = []
	moveMade = False
	animate = False

def highlightLastMove(screen, engine):
	if len(engine.moveLog) > 0:
		move = engine.moveLog[-1]
		s = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
		s.set_alpha(131)
		s.fill(pg.Color("yellow"))
		screen.blit(s, (move.startCol*SQUARE_SIZE, move.startRow*SQUARE_SIZE))
		screen.blit(s, (move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE))

def updateGameState(screen, engine, validMoves, selected):
	drawBoard(screen, engine)
	highlightLastMove(screen, engine)
	highlightSquares(screen, engine, validMoves, selected)
	drawPieces(screen, engine)
	drawMoveLog(screen, engine)

def drawMoveLog(screen, engine, fontsize=17, textColor="White"):
	font = pg.font.SysFont('TimesNewRoman', fontsize)
	padding = 5
	y = padding
	lineSpacing = 5
	movesPerRow = 2
	moveLogRect = pg.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
	pg.draw.rect(screen, pg.Color("Black"), moveLogRect)
	log = engine.moveLog
	moveTexts = [i.getChessNotation() for i in log]
	if len(moveTexts) > 0:
		for i in range(0, len(moveTexts)):
			t = f"{(i+1)-i//2}. {moveTexts[i]}  -  {'...' if len(moveTexts) <= i+1 else moveTexts[i+1]}"
			text = font.render(t, True, pg.Color(textColor))
			if i%(movesPerRow*2) != 0 and i%2 == 0:
				textLocation = moveLogRect.move(padding + MOVE_LOG_PANEL_WIDTH / 2, y)
				screen.blit(text, textLocation)
				pg.display.update()
				y += text.get_height() + lineSpacing
			if i%(movesPerRow*2) == 0:
				textLocation = moveLogRect.move(padding, y)
				screen.blit(text, textLocation)
				pg.display.update()

def drawBoard(screen, engine):
	global playerOne, playerTwo
	colors = [pg.Color("white"), pg.Color((200, 200, 200))]
	for row in range(DIMENSION):
		for column in range(DIMENSION):
			color = colors[((row+column)%2)]
			pg.draw.rect(screen, color, pg.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, engine):
	for row in range(DIMENSION):
		for column in range(DIMENSION):
			piece = engine.board[row][column]
			if piece != '--':
				screen.blit(PIECES[piece], pg.Rect(column*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPromotionMenu(screen, row, col, pieceColor):
	if row == 0:
		rows = [0, 1, 2, 3]
		color = pg.Color(232, 235, 239)
	elif row == 7:
		rows = [7, 6, 5, 4]
		color = pg.Color(125, 135, 150)
	for r in rows:
		pg.draw.rect(screen, color, pg.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE*4))
		pg.draw.rect(screen, (0,0,0), pg.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE*4), 1, 5)
		screen.blit(PIECES[f'{pieceColor}Q'], pg.Rect(col*SQUARE_SIZE, rows[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
		screen.blit(PIECES[f'{pieceColor}R'], pg.Rect(col*SQUARE_SIZE, rows[1]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
		screen.blit(PIECES[f'{pieceColor}B'], pg.Rect(col*SQUARE_SIZE, rows[2]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
		screen.blit(PIECES[f'{pieceColor}N'], pg.Rect(col*SQUARE_SIZE, rows[3]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
	pg.display.flip()

def animateMove(screen, move, engine, clock):
	colors = [pg.Color("white"), pg.Color((200, 200, 200))]
	dR = move.endRow - move.startRow
	dC = move.endCol - move.startCol
	framePerSquare = 10
	frameCount = (abs(dR) + abs(dC)) * framePerSquare
	for frame in range(frameCount+1):
		r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
		drawBoard(screen, engine)
		drawPieces(screen, engine)
		color = colors[(move.endRow + move.endCol) % 2]
		endSquare = pg.Rect(move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
		pg.draw.rect(screen, color, endSquare)
		if move.pieceCaptured != '--':
			if move.enpassantMove == True:
				endSquare = pg.Rect(move.endCol*SQUARE_SIZE, move.startRow*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
			screen.blit(PIECES[move.pieceCaptured], endSquare)
		screen.blit(PIECES[move.pieceMoved], pg.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
		pg.display.flip()

if __name__ == "__main__":
	i = 1
	main(i)