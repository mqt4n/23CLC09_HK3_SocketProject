from pyray import *
import globalVariable

SCREENWIDTH = 800
SCREENHEIGHT = 500
WIDTHFORBOX = 500
HEIGHTFORANNOUN = 200
SCREEN_COLOR = GRAY
BOX_WIDTH = 80
BOX_HEIGHT = 30
DISTANCE_BOX = 15

NUM_FILE_IN_WIDTH = int((WIDTHFORBOX-DISTANCE_BOX) / (BOX_WIDTH+DISTANCE_BOX))
DISTANCE_SIDE = int((WIDTHFORBOX - (NUM_FILE_IN_WIDTH*BOX_WIDTH + (NUM_FILE_IN_WIDTH-1) * DISTANCE_BOX))/2)
countNumFileToInput = 0
ENTER_BUTTON = GREEN

class BOX:
	colorBox = BLACK
	colorText = WHITE
	def __init__(self, f, x, y, s, t):
		self.fileName = f
		self.posX = x
		self.posY = y
		self.size = s
		self.typeSize = t

def makeBoxInf(box, name):
	countFile = 0
	curX = DISTANCE_SIDE
	curY = DISTANCE_BOX * 2
	for file in name:
		temp = BOX(file['filename'], curX, curY, file['size'], file['typeData'])
		box.append(temp)
		countFile += 1
		curX += BOX_WIDTH + DISTANCE_BOX
		if countFile % NUM_FILE_IN_WIDTH == 0:
			curX = DISTANCE_SIDE
			curY += BOX_HEIGHT + DISTANCE_BOX

def printBoxFileSV(box):
	draw_text("FILE FROM SEVER", int(WIDTHFORBOX/(3.5)), 5, 25, RED)
	for num in range(len(box)):
		draw_rectangle(box[num].posX, box[num].posY, BOX_WIDTH, BOX_HEIGHT, box[num].colorBox)
		draw_rectangle_lines_ex((box[num].posX, box[num].posY, BOX_WIDTH, BOX_HEIGHT), 2, WHITE)
		if len(box[num].fileName) >= 10:
			temp = box[num].fileName[0:7] + '...'
			draw_text(temp, box[num].posX + 20, box[num].posY + 10, 10, box[num].colorText)
		else: 
			draw_text(box[num].fileName, box[num].posX + 20, box[num].posY + 10, 10, box[num].colorText)

def writeToFile(textName, textMod):
	global countNumFileToInput
	with open("input.txt", 'a') as f:
		if textName != '' and textMod != '':
			if countNumFileToInput == 0:
				f.write(textName + ' ' + textMod)
				countNumFileToInput += 1
			else:
				f.write('\n' + textName + ' ' + textMod)
				countNumFileToInput += 1

def checkMousePressedOnBox(box):
	posMouseX = get_mouse_x()
	posMouseY = get_mouse_y()
	for num in range(len(box)):
		if check_collision_point_rec((posMouseX, posMouseY), (box[num].posX, box[num].posY, BOX_WIDTH, BOX_HEIGHT)):
			box[num].colorBox = WHITE
			box[num].colorText = BLACK
			if is_mouse_button_pressed(0):
				return box[num].fileName, True
		else: 
			box[num].colorBox = BLACK
			box[num].colorText = WHITE
	return '', False

def resizeImage(image, width, height):
	image_resize(image, width, height)
	texture = load_texture_from_image(image)
	return texture

def functForMakeFrame():
	draw_rectangle(0, SCREENHEIGHT - HEIGHTFORANNOUN, SCREENWIDTH, 3, BLACK)
	draw_rectangle(WIDTHFORBOX, 0, 3, SCREENHEIGHT - HEIGHTFORANNOUN, BLACK)

def functForPrintAnnoun():
	draw_text("NOTIFICATION", DISTANCE_BOX, SCREENHEIGHT - HEIGHTFORANNOUN + 5, 20, RED)
	if globalVariable.downloading == False:
		draw_text(globalVariable.announFirst, DISTANCE_BOX, SCREENHEIGHT - HEIGHTFORANNOUN + 10, 15, RED)
	else:	
		draw_text(globalVariable.announSecond, DISTANCE_BOX, SCREENHEIGHT - HEIGHTFORANNOUN + 10, 15, RED)

def functForInputBoxName(textBoxName, mouseOnTextName, textName, frameCounterName):
	draw_text("ENTER NAME OF FILE!", WIDTHFORBOX + 20, 20, 23, RED)
	draw_rectangle_rec(textBoxName, LIGHTGRAY)
	draw_text(textName, WIDTHFORBOX + 25, 60, 30, BLACK)
	if mouseOnTextName == True:
		if frameCounterName % 30 <= 4:
			draw_text('_', WIDTHFORBOX + 26 + measure_text(textName, 30), 60, 30, MAROON)
		draw_rectangle_lines_ex(textBoxName, 2, RED)
	else: draw_rectangle_lines_ex(textBoxName, 2, BLACK)

def functForInputBoxMod(textBoxMod, mouseOnTextMod, textMod, frameCounterMod):
	draw_text("ENTER MOD OF FILE!", WIDTHFORBOX + 20, 110, 23, RED)
	draw_rectangle_rec(textBoxMod, LIGHTGRAY)
	draw_text(textMod, WIDTHFORBOX + 25, 150, 30, BLACK)
	if mouseOnTextMod == True:
		if frameCounterMod%30 <= 4:
			draw_text('_', WIDTHFORBOX + 26 + measure_text(textMod, 30), 150, 30, MAROON)
		draw_rectangle_lines_ex(textBoxMod, 2, RED)
	else: draw_rectangle_lines_ex(textBoxMod, 2, BLACK)

def functForCheckBoxName(textName, textBoxName, mouseOnTextName, frameCounterName):
	if mouseOnTextName == True:
		frameCounterName += 1
	else: frameCounterName = 0	
	if check_collision_point_rec((get_mouse_x(), get_mouse_y()), textBoxName):
		mouseOnTextName = True
	else:
		mouseOnTextName = False
	if mouseOnTextName == True:
		set_mouse_cursor(2)
		key = get_char_pressed()
		while key > 0:
			if key >= 32 and key <= 125:
				textName += chr(key)
			key = get_char_pressed()
		if is_key_pressed(259):
			textName = textName[:-1]
	else:	
		set_mouse_cursor(0)
	return textName, mouseOnTextName, frameCounterName

def functForCheckBoxMod(textMod, textBoxMod, mouseOnTextMod, frameCounterMod):
	if mouseOnTextMod == True:
		frameCounterMod += 1
	else: frameCounterMod = 0	
	if check_collision_point_rec((get_mouse_x(), get_mouse_y()), textBoxMod):
		mouseOnTextMod = True
	else:
		mouseOnTextMod = False
	if mouseOnTextMod == True:
		set_mouse_cursor(2)
		key = get_char_pressed()
		while key > 0:
			if key >= 32 and key <= 125:
				textMod += chr(key)
			key = get_char_pressed()
		if is_key_pressed(259):
			textMod = textMod[:-1]
	else:	
		set_mouse_cursor(0)
	return textMod, mouseOnTextMod, frameCounterMod


def functForCheckEnterButton(textName, textMod, enterButton):
	global ENTER_BUTTON
	if check_collision_point_rec((get_mouse_x(), get_mouse_y()), enterButton):
		ENTER_BUTTON = RED
		if is_mouse_button_pressed(0):
			writeToFile(textName, textMod)
			textName = ''
			textMod = ''
			return textName, textMod		
	else: 
		ENTER_BUTTON = GREEN
	return textName, textMod

def secondWindow(boxName, boxMod, checkPressBox, criticalMod, highMod, normalMod):
	if is_mouse_button_pressed(0):
		posX = get_mouse_x()
		posY = get_mouse_y()
		if check_collision_point_rec((posX, posY), criticalMod):
			boxMod = 'CRITICAL'
			writeToFile(boxName, boxMod)
			return '', '', False
		elif check_collision_point_rec((posX, posY), highMod):
			boxMod = 'HIGH'
			writeToFile(boxName, boxMod)
			return '', '', False
		elif check_collision_point_rec((posX, posY), normalMod):
			boxMod = 'NORMAL'
			writeToFile(boxName, boxMod)
			return '', '', False
	return boxName, boxMod, checkPressBox

def drawBackLayer(texture, textBoxName, textBoxMod, enterButton, box):
	draw_texture_v(texture, [0, 0], WHITE)
	functForMakeFrame()
	draw_text("FILE FROM SEVER", int(WIDTHFORBOX/(3.5)), 5, 25, RED)
	draw_text("NOTIFICATION", DISTANCE_BOX, SCREENHEIGHT - HEIGHTFORANNOUN + 5, 20, RED)
	draw_text("ENTER NAME OF FILE!", WIDTHFORBOX + 20, 20, 23, RED)
	draw_rectangle_rec(textBoxName, LIGHTGRAY)
	draw_rectangle_lines_ex(textBoxName, 2, RED)
	draw_text("ENTER MOD OF FILE!", WIDTHFORBOX + 20, 110, 23, RED)
	draw_rectangle_rec(textBoxMod, LIGHTGRAY)
	draw_rectangle_lines_ex(textBoxMod, 2, RED)
	draw_rectangle_rec(enterButton, ENTER_BUTTON)
	draw_rectangle_lines_ex(enterButton, 2, RED)
	draw_text("ENTER", WIDTHFORBOX + 80, 225, 33, BLACK)	
	printBoxFileSV(box)

def drawFrontLayer(criticalMod, highMod, normalMod):
	draw_rectangle(int(SCREENWIDTH/5), int(SCREENHEIGHT/4), 500, 200, BLACK)
	draw_rectangle_lines_ex((int(SCREENWIDTH/5), int(SCREENHEIGHT/4), 500, 200), 2, WHITE)

	posX = get_mouse_x()
	posY = get_mouse_y()

	if check_collision_point_rec((posX, posY), criticalMod):
		draw_rectangle_rec(criticalMod, WHITE)
		draw_rectangle_lines_ex(criticalMod, 2, BLACK)
		draw_text('CRITICAL', 220, 215, 18, BLACK)
	else:
		draw_rectangle_rec(criticalMod, BLACK)
		draw_rectangle_lines_ex(criticalMod, 2, WHITE)
		draw_text('CRITICAL', 220, 215, 18, WHITE)

	if check_collision_point_rec((posX, posY), highMod):
		draw_rectangle_rec(highMod, WHITE)
		draw_rectangle_lines_ex(highMod, 2, BLACK)
		draw_text('HIGH', 390, 215, 18, BLACK)
	else:
		draw_rectangle_rec(highMod, BLACK)
		draw_rectangle_lines_ex(highMod, 2, WHITE)
		draw_text('HIGH', 390, 215, 18, WHITE)

	if check_collision_point_rec((posX, posY), normalMod):
		draw_rectangle_rec(normalMod, WHITE)
		draw_rectangle_lines_ex(normalMod, 2, BLACK)
		draw_text('NORMAL', 525, 215, 18, BLACK)
	else:
		draw_rectangle_rec(normalMod, BLACK)
		draw_rectangle_lines_ex(normalMod, 2, WHITE)
		draw_text('NORMAL', 525, 215, 18, WHITE)


def makeConsoleWindow(fileName):
	box = []
	makeBoxInf(box, fileName)

	# window console
	set_config_flags(FLAG_WINDOW_RESIZABLE);
	init_window(SCREENWIDTH, SCREENHEIGHT, "Client")
	set_trace_log_level(LOG_NONE)
	set_target_fps(60)	

	boxMod = ''
	boxName = ''
	textMod = ''
	textName = ''
	frameCounterName = 0
	frameCounterMod = 0
	checkPressBox = False
	mouseOnTextName = False
	mouseOnTextMod = False
	criticalMod = (210, 200, 100, 45)
	highMod = (360, 200, 100, 45)
	normalMod = (510, 200, 100, 45)
	enterButton = (WIDTHFORBOX + 65, 220, 150, 40)
	textBoxName = (WIDTHFORBOX + 20, 50, 250, 40)
	textBoxMod = (WIDTHFORBOX + 20, 140, 250, 40)
	texture = load_texture("wall.png")
	image = load_image_from_texture(texture)
	curWidth = SCREENWIDTH
	curHeight = SCREENHEIGHT	

	while not window_should_close():
		# if globalVariable.downloading == True:
		# 	print('True')
		# 	print(globalVariable.announSecond + '\n')

		if globalVariable.endProgram == True:
			break
		
		curWidth = get_screen_width()
		curHeight = get_screen_height()
		texture = resizeImage(image, curWidth, curHeight)
		
		if checkPressBox == False:
			boxName, checkPressBox = checkMousePressedOnBox(box)
			textName, mouseOnTextName, frameCounterName = functForCheckBoxName(textName, textBoxName, mouseOnTextName, frameCounterName)
			textMod, mouseOnTextMod, frameCounterMod = functForCheckBoxMod(textMod, textBoxMod, mouseOnTextMod, frameCounterMod)
			textName, textMod = functForCheckEnterButton(textName, textMod, enterButton)
			
			begin_drawing()

			draw_texture_v(texture, [0, 0], WHITE)
			functForMakeFrame()
			functForInputBoxName(textBoxName, mouseOnTextName, textName, frameCounterName)
			functForInputBoxMod(textBoxMod, mouseOnTextMod, textMod, frameCounterMod)
			draw_rectangle_rec(enterButton, ENTER_BUTTON)
			draw_rectangle_lines_ex(enterButton, 2, RED)
			draw_text("ENTER", WIDTHFORBOX + 80, 225, 33, BLACK)
			functForPrintAnnoun()
			printBoxFileSV(box)

			end_drawing()
		else:
			boxName, boxMod, checkPressBox = secondWindow(boxName, boxMod, checkPressBox, criticalMod, highMod, normalMod)
			begin_drawing()

			drawBackLayer(texture, textBoxName, textBoxMod, enterButton, box)
			drawFrontLayer(criticalMod, highMod, normalMod)

			end_drawing()

	close_window()