from enum import Enum 
import time
import serial

class Status(Enum):
	STOPPED = 'S'
	JOGGINGFORWARD ='F'
	JOGGINGREVERSE= 'R'
	PAUSED = 'P'
	ERROR = 'E'

class ProtcolMessage(Enum):
    ENQ = chr(133)  # <ENQ> in acsii + 128
    NULL = chr(128)  # <Null>: 0 + 128
    ACK = chr(134)  # 6 + 128
    CR = chr(141)  # 13 + 128


class CommandCode(Enum):
    SCAN = "G"
    PAUSE = "P"
    STOP = "S"
    HOME = "H"
    SLEW = '9'
    JOGFORWARD = "F"
    JOGREVERSE = "R"
    FASTERJOG = "Q"
    SLOWERJOG = "Z"
    SCANMODE = "B"
    UNITS = "U"
    BURSTFIRE = "L"
    NEXTPOSITION = "N"
    SHGRETURN = "C"
    SHGALIGN = "K"
    SHGFORWARD = "D"
    SHGREVERSE = "E"
    SHGJOGCRYSTAL = "I"
    SHGJOGPRISM = "J"


class SCU():
	def __init__(self):
		self.unit = "W" #wavenumbers
		self.position = 15000 #Start at 15000
		self.status = "S" #Start as stopped 

	def slew(self, new_position):
		if new_position < self.position:
			self.status = Status.JOGGINGREVERSE
			while new_position != self.position and self.status != Status.STOPPED:
				self.position  -= 1
				time.sleep(.1)
		else:
			self.status = Status.JOGGINGFORWARD
			while new_position != self.position and self.status != Status.STOPPED:
				self.position  += 1
				time.sleep(.1) 
		self.status = Status.STOPPED
	
	def jog_forward(self)
		self.status = Status.JOGGINGFORWARD
		while new_position != self.position and self.status != Status.STOPPED:
				self.position  += 1
				time.sleep(.1) 
		self.status = Status.STOPPED

	def jog_reverse(self)
		self.status = Status.JOGGINGREVERSE
		while new_position != self.position and self.status != Status.STOPPED:
				self.position  -= 1
				time.sleep(.1) 
		self.status = Status.STOPPED

class SerialParser():
	def __init__(self):
		ser = serial.Serial(port="COM1", baudrate=9600,
                    bytesize=serial.EIGHTBITS, stopbits=2, rtscts=True)
		

	def poll(self):
		while True:
			null_count = 0
			ser.flushInput()
			command_buffer = ""
			if null_count == 45:
				ser
			ser.write(ProtcolMessage.ENQ)






