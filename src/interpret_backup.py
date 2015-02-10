from sys import stdin, path
import sys
path.insert(0, "../lib")

import io
import math
from BaseHTTPServer import *
from SimpleHTTPServer import SimpleHTTPRequestHandler
from collections import defaultdict

from Leap import *
from signs import *

g_message = ""

class SignListener(Listener):
	def __init__(self):
		Listener.__init__(self)
		self.i = 0
		self.prevMessage = ""
		self.prevCode = ""

	def on_frame(self, controller):
		self.i += 1
		if self.i % 5 == 0:
			f = [0]*5
			average = Vector()
			for i in range(0,5):
				frame = controller.frame(i)
				frameList = frame.fingers.extended()
				for j in range(len(frameList)):
					f[frameList[j].type()] += 1

			ret = []
			for k in range(len(f)):
				if f[k] > 3:
					ret.append(k)

			avgMotion = getAvgMotion(controller)
			m = False
			if avgMotion > .99:
				m = True

			code, message = checkSigns(ret, m)
			if not message == self.prevMessage and not code == self.prevCode:
				print message
				if message != "":
					# mFile = open("../text/output.txt", "w")
					# mFile.write(message)
					# mFile.close()
					g_message = message


				self.prevMessage = message
				self.prevCode = code

def main():
	listener = SignListener()
	controller = Controller()
	controller.add_listener(listener)

	# controller.config.set("head_mounted_display_mode", True)

	# while True:
	# 	x = stdin.readline()
	# 	if not x:
	# 		print "Quitting"
	# 		return 0
	# 		# # print "thumb " + str(getDir(0, controller))
	# 		# # print "pointer " + str(getDir(1, controller))
	# 		# # print "middle " + str(getDir(2, controller))
	# 		# # print "ring " + str(getDir(3, controller))
	# 		# # print "pinky " + str(getDir(4, controller))
	# 		# # print transformHand(controller)
	# 		# extended_fingers = controller.frame().fingers.extended()
	# 		# for finger in extended_fingers:
	# 		# 	print finger.type()
	# 		# print

	HandlerClass = MyRequestHandler
	ServerClass  = HTTPServer
	Protocol     = "HTTP/1.0"

	if sys.argv[1:]:
	    port = int(sys.argv[1])
	else:
	    port = 8000
	server_address = ('127.0.0.1', port)

	HandlerClass.protocol_version = Protocol
	httpd = ServerClass(server_address, HandlerClass)

	sa = httpd.socket.getsockname()
	print "Serving HTTP on", sa[0], "port", sa[1], "..."
	httpd.serve_forever()

class MyRequestHandler (BaseHTTPRequestHandler) :

    def do_GET(self) :

        if self.path == "/me" :
            #send response code:
            self.send_response(200)
            #send headers:
            self.send_header("Content-type:", "text/html")
            # send a blank line to end headers:
            self.wfile.write("\n")

            #send response:
            json.dump(me, self.wfile)


def getAvgMotion(controller):
	frame = controller.frame()
	hands = frame.hands
	motions = []
	for i in range(0,20):
		motions.append(hands.rightmost.rotation_probability(controller.frame(5)))
	avg = sum(motions) / 20
	return avg


def getDir(finger, controller):
	count = 0
	average = Vector()
	frame = controller.frame()
	finger_to_average = frame.fingers[finger]
	for i in range(0,4):
	    finger_from_frame = controller.frame(i).finger(finger_to_average.id)
	    if(finger_from_frame.is_valid):
	        average = average + finger_from_frame.tip_position
	        count += 1
	average = average/count
	return average

def transformHand(controller):
	frame = controller.frame()
	positions = defaultdict(list)
	directions = defaultdict(list)
	for hand in frame.hands:
	    hand_x_basis = hand.basis.x_basis
	    hand_y_basis = hand.basis.y_basis
	    hand_z_basis = hand.basis.z_basis
	    hand_origin = hand.palm_position
	    hand_transform = Matrix(hand_x_basis, hand_y_basis, hand_z_basis, hand_origin)
	    hand_transform = hand_transform.rigid_inverse()

	    for finger in hand.fingers:
	        transformed_position = hand_transform.transform_point(finger.tip_position)
	        transformed_direction = hand_transform.transform_direction(finger.direction)
	        positions[hand.id].append(transformed_direction.to_tuple())
	        directions[hand.id].append(transformed_direction.to_tuple())

	return positions, directions


if __name__ == '__main__':
	main()