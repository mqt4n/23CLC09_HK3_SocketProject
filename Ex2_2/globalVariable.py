# global variable in both file
def init():
	global announFirst
	global announSecond
	global downloading
	global endProgram

	announFirst = '\nThe file has been downloaded will not be downloaded again.' + '\nPlease check your output folder before.'
	announSecond = ''
	downloading = False
	endProgram = False