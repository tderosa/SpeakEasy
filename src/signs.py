def FUhandler(ext_fingers):
	if ext_fingers == [2] or ext_fingers == [0,2]:
		return True
	return False

def ILYhandler(ext_fingers):
	if ext_fingers == [0,1,4]:
		return True
	return False

def Bhandler(ext_fingers):
	if ext_fingers == [1,2,3,4] or ext_fingers == [0,1,2,3,4,5]:
		return True
	return False

def checkSigns(ext_fingers, movement):
	code = ""
	message = ""
	if FUhandler(ext_fingers):
		code = "fu"
		message = "Screw you"
	elif ILYhandler(ext_fingers):
		code = "ily"
		message = "I love you"
	elif Bhandler(ext_fingers):
		code = "b"
		if movement:
			message = "Blue"
		else:
			message = "B"
	return (code, message)

