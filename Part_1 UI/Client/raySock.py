from pyray import *
import globalVariable

SCREENWIDTH = 800
SCREENHEIGHT = 500
WIDTHFORBOX = 300
HEIGHTFORANNOUN = 250
SCREEN_COLOR = WHITE
BOX_WIDTH = 80
BOX_HEIGHT = 30
DISTANCE = 15

NUM_FILE_IN_WIDTH = int(WIDTHFORBOX / (BOX_WIDTH+DISTANCE))
DISTANCE_SIDE = (SCREENWIDTH - WIDTHFORBOX) + int((WIDTHFORBOX - (NUM_FILE_IN_WIDTH*BOX_WIDTH + (NUM_FILE_IN_WIDTH-1) * DISTANCE))/2)
countNumFileToInput = 0

class BOX:
	colorBox = BLACK
	colorText = WHITE
	def __init__(self, f, x, y, s, t, pos):
		self.fileName = f
		self.posX = x
		self.posY = y
		self.size = s
		self.typeSize = t
		self.pos = pos

def makeBoxInf(box, name):
	countFile = 0
	curX = DISTANCE_SIDE
	curY = SCREENHEIGHT - HEIGHTFORANNOUN - 100 + DISTANCE*2
	for file in name:
		temp = BOX(file['file_name'], curX, curY, file['size'], file['typeData'], countFile+1)
		box.append(temp)
		countFile += 1
		curX += BOX_WIDTH + DISTANCE
		if countFile % NUM_FILE_IN_WIDTH == 0:
			curX = DISTANCE_SIDE
			curY += BOX_HEIGHT + DISTANCE

def printBoxFileSV(box):
	draw_text('OR YOU CAN CHOOSE HERE: ', SCREENWIDTH-WIDTHFORBOX + 10, SCREENHEIGHT-HEIGHTFORANNOUN - 100, 20, RED)
	for num in range(len(box)):
		draw_rectangle(box[num].posX, box[num].posY, BOX_WIDTH, BOX_HEIGHT, box[num].colorBox)
		draw_text(str(box[num].pos), box[num].posX + 37, box[num].posY + 9, 15, box[num].colorText)

def printNameOfFileFromSever(box):
	draw_text("FILE FROM SEVER", DISTANCE, 5, 25, RED)
	temp = '\n'
	for file in box:
		if (file.pos-1) % 4 == 0:
			temp += '\n' + str(file.pos) + '. ' + file.fileName + '\t\t\t'
		else: 
			temp += str(file.pos) + '. ' + file.fileName + '\t\t\t'
	draw_text(temp, DISTANCE, 5, 15, WHITE)

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

def functForMakeFrame():
	draw_rectangle(SCREENWIDTH - WIDTHFORBOX, 0, 3, SCREENHEIGHT, BLACK)
	draw_rectangle(0, SCREENHEIGHT-HEIGHTFORANNOUN, SCREENWIDTH - WIDTHFORBOX, 3, BLACK)

def functForPrintAnnoun():
	draw_text("NOTIFICATION", DISTANCE, SCREENHEIGHT - HEIGHTFORANNOUN + 5, 20, RED)
	if globalVariable.downloading == False:
		draw_text(globalVariable.announFirst, DISTANCE, SCREENHEIGHT - HEIGHTFORANNOUN + 10, 15, WHITE)
	else:	
		draw_text(globalVariable.announSecond, DISTANCE, SCREENHEIGHT - HEIGHTFORANNOUN + 10, 15, WHITE)

def functForInputBox(textBox, mouseOnText, text, frameCounter):
	draw_text("ENTER NAME OF FILE!", SCREENWIDTH-WIDTHFORBOX + 20, 30, 23, RED)
	draw_rectangle_rec(textBox, LIGHTGRAY)
	draw_text(text, SCREENWIDTH-WIDTHFORBOX + 25, 75, 30, BLACK)
	if mouseOnText == True:
		if frameCounter%30 <= 4:
			draw_text('_', SCREENWIDTH-WIDTHFORBOX + 26 + measure_text(text, 30), 80, 30, MAROON)
		draw_rectangle_lines_ex(textBox, 2, RED)
	else: draw_rectangle_lines_ex(textBox, 2, BLACK)

def makeConsoleWindow(fileName) : 
	box = [] 
	makeBoxInf(box, fileName)

	# window console
	init_window(SCREENWIDTH, SCREENHEIGHT, "Client")
	set_trace_log_level(LOG_NONE)
	set_target_fps(60)	

	text = ''
	frameCounter = 0
	mouseOnText = False
	textBox = (SCREENWIDTH-WIDTHFORBOX + 20, 70, 250, 40)
	texture = load_texture("wall.png")
	image = load_image_from_texture(texture)
	image_resize(image, SCREENWIDTH, SCREENHEIGHT)
	texture = load_texture_from_image(image)

	print(f"List of file from server: " ) 
	for file in fileName:
		print(f"File name: {file['file_name']} | Size: {file['size']} {file['typeData']}")
	
	while not window_should_close() :
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
			if is_key_pressed(257) and text != '':
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
		printNameOfFileFromSever(box)
		printBoxFileSV(box)
		end_drawing()
	globalVariable.endProgram = True
	close_window()
