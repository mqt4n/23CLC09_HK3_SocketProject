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
		temp = BOX(file['file_name'], curX, curY, file['size'], file['typeData'])
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
		if len(box[num].fileName) >= 10:
			temp = box[num].fileName[0:7] + '...'
			draw_text(temp, box[num].posX + 20, box[num].posY + 10, 10, box[num].colorText)
		else: 
			draw_text(box[num].fileName, box[num].posX + 20, box[num].posY + 10, 10, box[num].colorText)

def writeToFile(name):
	global countNumFileToInput
	with open("input.txt", 'a') as f:
		if countNumFileToInput == 0:
			f.write(name)
			countNumFileToInput += 1
		else:
			f.write('\n')
			f.write(name)
			countNumFileToInput += 1

def checkMousePressedOnBox(box):
	posMouseX = get_mouse_x()
	posMouseY = get_mouse_y()
	for num in range(len(box)):
		if check_collision_point_rec((posMouseX, posMouseY), (box[num].posX, box[num].posY, BOX_WIDTH, BOX_HEIGHT)):
			box[num].colorBox = WHITE
			box[num].colorText = BLACK
			if is_mouse_button_pressed(0):
				writeToFile(box[num].fileName)
		else: 
			box[num].colorBox = BLACK
			box[num].colorText = WHITE

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

def functForInputBox(textBox, mouseOnText, text, frameCounter):
	draw_text("ENTER NAME OF FILE!", WIDTHFORBOX + 20, 30, 23, RED)
	draw_rectangle_rec(textBox, LIGHTGRAY)
	draw_text(text, WIDTHFORBOX + 25, 105, 30, BLACK)
	if mouseOnText == True:
		if frameCounter%30 <= 4:
			draw_text('_', WIDTHFORBOX + 26 + measure_text(text, 30), 112, 30, MAROON)
		draw_rectangle_lines_ex(textBox, 2, RED)
	else: draw_rectangle_lines_ex(textBox, 2, BLACK)

def makeConsoleWindow(fileName):
	box = []
	makeBoxInf(box, fileName)

	# window console
	set_config_flags(FLAG_WINDOW_RESIZABLE);
	init_window(SCREENWIDTH, SCREENHEIGHT, "Client")
	set_trace_log_level(LOG_NONE)
	set_target_fps(60)	

	text = ''
	frameCounter = 0
	mouseOnText = False
	textBox = (WIDTHFORBOX + 20, 100, 250, 40)
	texture = load_texture("wall.png")
	image = load_image_from_texture(texture)
	curWidth = SCREENWIDTH
	curHeight = SCREENHEIGHT

	while not window_should_close():
		curWidth = get_screen_width()
		curHeight = get_screen_height()
		texture = resizeImage(image, curWidth, curHeight)
		checkMousePressedOnBox(box)
		if mouseOnText == True:
			frameCounter += 1
		else: frameCounter = 0	
		if check_collision_point_rec((get_mouse_x(), get_mouse_y()), textBox):
			mouseOnText = True
		else:
			mouseOnText = False
		if mouseOnText == True:
			set_mouse_cursor(2)
			key = get_char_pressed()
			while key > 0:
				if key >= 32 and key <= 125:
					text += chr(key)
				key = get_char_pressed()
			if is_key_pressed(259):
				text = text[:-1]
			if is_key_pressed(257):
				writeToFile(text)
				text = ''
		else:	
			set_mouse_cursor(0)
		if globalVariable.endProgram == True:
			break
		begin_drawing()
		clear_background(SCREEN_COLOR)
		draw_texture_v(texture, [0, 0], WHITE)
		functForMakeFrame()
		functForInputBox(textBox, mouseOnText, text, frameCounter)
		functForPrintAnnoun()
		printBoxFileSV(box)
		end_drawing()
	
	close_window()
